import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import math
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import re
import statistics



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

rent = pd.DataFrame()
rent_mean_df = pd.DataFrame(columns=["District, Mean rent"])


price_pattern = r'^\d+\.?\d*'
def process_rent_csvs(file_path):
    global rent
    global rent_mean_df

    id_df = file_path.rstrip("_offers.csv")
    df = pd.read_csv(file_path).iloc[:,  [0, 1, 3, 4, 5, 8]]
    df.columns = ["ID", "Количество комнат","Метро","Адрес","Площадь, м2", "Цена"]
    df["Price"] = df["Цена"].astype(str).apply(lambda x: re.search(price_pattern, x).group() if re.search(price_pattern, x) else '')
    df["Количество комнат"] = df["Количество комнат"].astype(str).str[:1]
    df["Цена"] = df["Цена"].astype(str).str[:41]

    df["Price_Numeric"] = pd.to_numeric(df["Price"], errors='coerce')
    
    df["Районы"] = id_df
    rent = pd.concat([rent, df])

    rent_mean = round(statistics.mean(df["Price_Numeric"]), 3)
    new_data = pd.DataFrame({"District": [id_df], "Mean rent": [rent_mean]})
    rent_mean_df = pd.concat([rent_mean_df, new_data], ignore_index=True)

districts_csv = [
    "СЗАО_offers.csv", "ЦАО_offers.csv",
    "САО_offers.csv", "СВАО_offers.csv",
    "ВАО_offers.csv", "ЮВАО_offers.csv",
    "ЮАО_offers.csv", "ЮЗАО_offers.csv",
    "ЗАО_offers.csv"
]

districts_data_search = {}

for i, file_name in enumerate(districts_csv):
    df_name = file_name.split('_')[0] + '_rent'
    districts_data_search[df_name] = process_rent_csvs(file_name)
rent_means_df = rent_mean_df.iloc[:, [1, 2]]
rent_mean_df = rent_mean_df.sort_values(by="Mean rent", ascending=False)


malls_by_district = {1: ["ЦАО", 27], 2: ["ЮАО",48], 3: ["САО", 26], 4: ["ВАО", 27], 5: ["ЗАО", 24], 6: ["СВАО", 24], 7: ["ЮВАО",22], 8:["СЗАО",17], 9: ["ЮЗАО", 29]}
malls_df = pd.DataFrame.from_dict(malls_by_district, orient='index', columns=['District', 'Number of Malls'])
malls_df = malls_df.sort_values(by='Number of Malls', ascending=False)
#print(malls_df)


app = dash.Dash(__name__, external_stylesheets=["assets/style.css"])

app.layout = html.Div(
    style={
        "display": "grid",
        "grid-template-columns": "20vw 30vw", 
        "gap": "20px", 
        "height": "auto", 
        "width": "fit-content",
        #"margin": "0 auto", # Center the entire grid on the page
        "padding": "20px", # Padding around the whole grid
        "box-sizing": "border-box" # Ensure padding is included in total width
    },
    children=[
        html.H1("Лучшие районы г. Москва для молодых специалистов",
                style={'grid-column': '1 / -1', 'margin-bottom': '20px'}), # Header spans all columns
        html.Div(
            style={
                'grid-column': '1', 
                'display': 'flex',
                'flex-direction': 'column', 
                'gap': '20px', 
                'width': '20vw',
                'box-sizing': 'border-box'
            },
            children=[
                dcc.Graph(
                    id="scatter-plot",
                    figure=px.scatter(
                        sorted_density,
                        x="Density",
                        y="District",
                        color="Density",
                        color_continuous_scale=color_scale,
                        title="Плотность населения по районам",
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
                    style={
                        'height': "180vh",
                        'width': "20vw", 
                        'border': '3px solid #ccc',
                        'padding': '5px',
                        'display': 'block'
                    }
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="air-plot",
                            figure=px.bar(
                                air,
                                x="Number",
                                y="Number", 
                                title="Количество лесов и парков по районам",
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
                            style={
                                'height': "80vh",
                                'width': "20vw", 
                                'border': '3px solid #ccc',
                                'padding': '5px',
                                'display': 'block'
                            }
                        ),
                        html.Div(id='clicked-districts', style={'marginTop': '20px', 'border': '1px solid #eee', 'padding': '10px'})
                    ],
                    style={'height': "auto", "width": "20vw", 'box-sizing': 'border-box'} # This Div's width must match column width
                ),
            ]
        ),

        # Column 2 Container
        html.Div(
            style={
                'grid-column': '2', # Place this div in the second grid column
                'display': 'flex',
                'flex-direction': 'column',
                'gap': '20px', # Space between items in this column
                'width': '50vw',
                'box-sizing': 'border-box'
            },
            children=[
                html.Div(
                    [
                        dcc.Graph(
                            id="rent-plot",
                            figure = px.box(
                                rent_mean_df,
                                x="District",
                                y="Mean rent",
                                title="Средняя стоимость аренды по округам",
                                hover_data={"District":False, "Mean rent":True},
                                ).update_layout(
                                    yaxis={
                                        'automargin': True,
                                        'showticklabels': True,
                                        'tickmode': 'linear',
                                        'tick0': 70000,
                                        'dtick': 5000,
                                        'ticklen': 5,
                                    }
                                )
                        )
                    ],
                    style={
                        'height': "50vh",
                        'width': "30vw",
                        'border': '3px solid #ccc',
                        'padding': '5px',
                        'display': 'block'
                    }
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="malls-plot",
                            figure = px.scatter(
                                malls_df,
                                x="District",
                                y="Number of Malls",
                                title="Количество торговых центров по округам",
                                hover_data={"District":True, "Number of Malls":True},
                                size='Number of Malls',
                                color='Number of Malls',
                                color_continuous_scale=color_scale,
                                ).update_layout(
                                    yaxis={
                                        'automargin': True,
                                        'showticklabels': True,
                                    }
                                )
                        )
                    ],
                    style={
                        'height': "50vh",
                        'width': "30vw", # Keep original width (matches column width)
                        'border': '3px solid #ccc',
                        'padding': '5px',
                        'display': 'block'
                    }
                )
            ]
        )
        
    ]
)

@app.callback(
    dash.Output('clicked-districts', 'children'),
    dash.Input('air-plot', 'clickData'))
def display_clicked_districts(clickData):
    if clickData is not None:
        clicked_bar_index = clickData['points'][0]['pointIndex']
        districts_info = air.iloc[clicked_bar_index]
        districts_list = districts_info['District'] if isinstance(districts_info['District'], list) else [districts_info['District']]

        return html.Div([
            html.H3(f"Районы с {air['Number'].iloc[clicked_bar_index]} источниками воздуха:"),
            html.Ul([html.Li(district) for district in districts_list])
        ])
    return html.P("Нажмите на столбец, чтобы увидеть список районов.")

if __name__ == "__main__":
    app.run(debug=True)