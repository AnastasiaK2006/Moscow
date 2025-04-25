import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import math
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import re



pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
area = pd.DataFrame(pd.read_csv("Площадь.csv", sep=';'))
population = pd.DataFrame(pd.read_csv("Население.csv", sep=';'))

population_2024 = population.iloc[:, [0, -2]]
area = area.iloc[:, [0, 1]]
population_2024.columns = ["District", "Population"]
area.columns = ["District", "Area in ha"]
den = pd.merge(population_2024, area, on="District", how="inner")
den["Area in ha"] = pd.to_numeric(den["Area in ha"].str.replace(r",\s*", ".", regex=True))
column_density = (den["Population"] / (den["Area in ha"] * 0.01))

den['Density'] = column_density
sorted_density = den.sort_values(by="Density").iloc[:, [0, -1]]
density_mean = sorted_density["Density"].sum() / len(sorted_density["Density"])
summ = 0
for i in sorted_density["Density"]:
    summ += (density_mean - i) ** 2
standart_deviation = math.sqrt(summ / len(sorted_density["Density"]))


def assign_color(x):
    if x <= density_mean + standart_deviation and x >= density_mean - standart_deviation:
        color = "#89cdf0"
    elif x < density_mean - standart_deviation and x >= density_mean - 2 * standart_deviation:
        color = "#61b546"
    elif x < density_mean - 2 * standart_deviation:
        color = "#6092cd"
    elif x > density_mean + standart_deviation and x <= density_mean + 2 * standart_deviation:
        color = "#f4a522"
    elif x > density_mean + 2 * standart_deviation:
        color = "#aa4498"
    return color


den["Color"] = den["Density"].apply(assign_color)
color_map_districts = dict(zip(den["District"], den["Color"]))

air_sources = pd.DataFrame(pd.read_csv("air.csv")).iloc[:, [0, 1]]
air_sources.columns = ["District", "Number"]
sorted_airs = air_sources.sort_values(by="Number")
air = sorted_airs.groupby("Number")["District"].apply(list).reset_index()
color_scale = ["#6092cd", "#89cdf0", "#61b546", "#f4a522", "#aa4498"]


price_pattern = r'^\d+\.?\d*\.?'

rent = pd.DataFrame(pd.read_csv("offers.csv")).iloc[:, [0, 1, 3, 4, 5, 6, 7]]
rent.columns = ["ID", "Количество комнат","Метро","Адрес","Площадь, м2","Дом","Цена"]
rent["Price"] = ""
for i in range(len(rent.iloc[:, 6])):
    rent["Price"][i] = re.search(price_pattern, rent.iloc[:, 6][i]).group()

print(rent.head())



app = dash.Dash(__name__, external_stylesheets=["assets/style.css"])
app.layout = html.Div(
    style={"height": "auto", "width": "100vw"},
    children=[
        html.H1("Лучшие районы г. Москва для молодых специалистов"),
        dcc.Graph(
            id="scatter-plot",
            figure=px.scatter(
                sorted_density,
                x="Density",
                y="District",
                color="Density",
                color_continuous_scale=color_scale,
                title="Плотность населения",
            ).update_layout(
                yaxis={
                    'categoryorder': 'total ascending',
                    'automargin': True,
                    'showticklabels': True,
                    'tickmode': 'linear',
                    'tick0': 0,
                    'dtick': 1,
                },
            ),
            style={'height': "180vh", "width": "20vw", 'border': '3px solid #ccc', 'padding': '5px', 'display': 'inline-block'}
        ),
        html.Div(
            [
                dcc.Graph(
                    id="air-plot",
                    figure=px.bar(
                        air,
                        x="Number",
                        y="Number",
                        title="Количество лесов и парков",
                        hover_data={'Number': True, 'District': False},
                        color=air['Number'],
                        color_continuous_scale=color_scale,
                    ).update_layout(
                        yaxis={
                            'categoryorder': 'total ascending',
                            'automargin': True,
                            'tickmode': 'linear',
                            'tick0': 0,
                            'dtick': 1,
                        },
                        clickmode='event+select'
                    ),
                    style={'height': "80vh", "width": "20vw", 'border': '3px solid #ccc', 'padding': '5px', 'display': 'inline-block'}
                ),
                html.Div(id='clicked-districts', style={'marginTop': '20px', 'border': '1px solid #eee', 'padding': '10px'})
            ]
        )
    ]
)

@app.callback(
    Output('clicked-districts', 'children'),
    Input('air-plot', 'clickData'))
def display_clicked_districts(clickData):
    if clickData is not None:
        clicked_bar_index = clickData['points'][0]['pointIndex']
        districts = air.iloc[clicked_bar_index]['District']
        return html.Div([
            html.H3(f"Районы с {air['Number'].iloc[clicked_bar_index]} источниками воздуха:"),
            html.Ul([html.Li(district) for district in districts])
        ])
    return html.P("Нажмите на столбец, чтобы увидеть список районов.")

if __name__ == "__main__":
    app.run(debug=True)