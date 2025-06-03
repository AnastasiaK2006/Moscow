import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import math
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import re
import statistics


districts_by_admin_okrug = {
    "ЦАО": [
        "Арбат", "Басманный", "Замоскворечье", "Красносельский", "Мещанский",
        "Пресненский", "Таганский", "Тверской", "Хамовники", "Якиманка"
    ],
    "САО": [
        "Аэропорт", "Беговой", "Бескудниковский", "Войковский", "Головинский",
        "Дегунино Восточное", "Дегунино Западное", "Дмитровский", "Коптево",
        "Левобережный", "Молжаниновский", "Савёловский", "Сокол",
        "Тимирязевский", "Ховрино", "Хорошёвский"
    ],
    "СВАО": [
        "Алексеевский", "Алтуфьевский", "Бабушкинский", "Бибирево", "Бутырский",
        "Лианозово", "Лосиноостровский", "Марфино", "Марьина роща",
        "Медведково Северное", "Медведково Южное", "Останкинский", "Отрадное",
        "Ростокино", "Свиблово", "Северный", "Ярославский"
    ],
    "ВАО": [
        "Богородское", "Вешняки", "Восточный", "Гольяново", "Ивановское",
        "Измайлово Восточное", "Измайлово", "Измайлово Северное",
        "Косино-Ухтомский", "Метрогородок", "Новогиреево", "Новокосино",
        "Перово", "Преображенское", "Соколиная гора", "Сокольники"
    ],
    "ЮВАО": [
        "Выхино-Жулебино", "Капотня", "Кузьминки", "Лефортово", "Люблино",
        "Марьино", "Некрасовка", "Нижегородский", "Печатники", "Рязанский",
        "Текстильщики", "Южнопортовый"
    ],
    "ЮАО": [
        "Бирюлёво Восточное", "Бирюлёво Западное", "Братеево", "Даниловский",
        "Донской", "Зябликово", "Москворечье-Сабурово", "Нагатино-Садовники",
        "Нагатинский затон", "Нагорный", "Орехово-Борисово Северное",
        "Орехово-Борисово Южное", "Царицыно", "Чертаново Северное",
        "Чертаново Центральное", "Чертаново Южное"
    ],
    "ЮЗАО": [
        "Академический", "Бутово Северное", "Бутово Южное", "Гагаринский",
        "Зюзино", "Коньково", "Котловка", "Ломоносовский", "Обручевский",
        "Тёплый Стан", "Черёмушки", "Ясенево"
    ],
    "ЗАО": [
        "Внуково", "Дорогомилово", "Крылатское", "Кунцево", "Можайский",
        "Ново-Переделкино", "Очаково-Матвеевское", "Проспект Вернадского",
        "Раменки", "Солнцево", "Тропарёво-Никулино", "Филёвский парк",
        "Фили-Давыдково"
    ],
    "СЗАО": [
        "Куркино", "Митино", "Покровское-Стрешнево", "Строгино",
        "Тушино Северное", "Тушино Южное", "Хорошёво-Мневники", "Щукино"
    ]
}

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
den['Density'] = round(column_density, 0)
sorted_density = den.sort_values(by="Density").iloc[:, [0, -1]]
density_mean = sorted_density["Density"].sum() / len(sorted_density["Density"])
summ = 0
for i in sorted_density["Density"]:
    summ += (density_mean - i) ** 2
standart_deviation_density = int(math.sqrt(summ / len(sorted_density["Density"])))
print("Standart deviation density:", standart_deviation_density)
#sorted_density_mean = sorted_density.loc[(sorted_density['Density'] <= density_mean + standart_deviation_density) & \
                                         #(sorted_density['Density'] >= density_mean - standart_deviation_density), \
                                         #['Density', 'District']].sort_values(by='Density')

#print("     Density = mean_density +- 1 standart deviation")
#print(sorted_density_mean)

def assign_color(x):
    if x <= density_mean + standart_deviation_density and x >= density_mean - standart_deviation_density:
        color = "#89cdf0"
    elif x < density_mean - standart_deviation_density and x >= density_mean - 2 * standart_deviation_density:
        color = "#61b546"
    elif x < density_mean - 2 * standart_deviation_density:
        color = "#6092cd"
    elif x > density_mean + standart_deviation_density and x <= density_mean + 2 * standart_deviation_density:
        color = "#f4a522"
    elif x > density_mean + 2 * standart_deviation_density:
        color = "#aa4498"
    return color

#Calculating points of density
def assign_den_points(x):
    if x <= density_mean + standart_deviation_density and x >= density_mean - standart_deviation_density:
        den_points = 1
    elif x < density_mean - standart_deviation_density and x >= density_mean - 2 * standart_deviation_density:
        den_points = 0.5
    elif x < density_mean - 2 * standart_deviation_density:
        den_points = 0.25
    elif x > density_mean + standart_deviation_density and x <= density_mean + 2 * standart_deviation_density:
        den_points = 0.5
    elif x > density_mean + 2 * standart_deviation_density:
        den_points = 0.25
    return den_points

sorted_density["Points"] = sorted_density["Density"].apply(assign_den_points)
#print(sorted_density)


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

    rent_mean = round(statistics.mean(df["Price_Numeric"]), 0)
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
rent_mean_df = rent_mean_df.iloc[:, [1, 2]]
rent_mean_df = rent_mean_df.sort_values(by="Mean rent", ascending=False)

mean_rent = round(statistics.mean(rent_mean_df["Mean rent"]))
summ = 0
for i in rent_mean_df["Mean rent"]:
    summ += (mean_rent - i) ** 2
standart_deviation_rent = int(math.sqrt(summ / len(rent_mean_df["Mean rent"])))
print("Standart deviation rent:", standart_deviation_rent)
#Calculating points of rent
def assign_rent_points(x):
    if x <= mean_rent+ standart_deviation_rent and x >= mean_rent - standart_deviation_rent:
        rent_points = 1
    elif x < mean_rent - standart_deviation_rent and x >= mean_rent - 2 * standart_deviation_rent:
        rent_points = 0.5
    elif x < mean_rent - 2 * standart_deviation_rent:
        rent_points = 0.25
    elif x > mean_rent + standart_deviation_rent and x <= mean_rent + 2 * standart_deviation_rent:
        rent_points = 0.5
    elif x > mean_rent + 2 * standart_deviation_rent:
        rent_points = 0.25
    return rent_points

rent_mean_df["Points"] = rent_mean_df["Mean rent"].apply(assign_rent_points)
#print(rent_mean_df)

malls_by_district = {1: ["ЦАО", 27], 2: ["ЮАО",48], 3: ["САО", 26], 4: ["ВАО", 27], 5: ["ЗАО", 24], 6: ["СВАО", 24], 7: ["ЮВАО",22], 8:["СЗАО",17], 9: ["ЮЗАО", 29]}
malls_df = pd.DataFrame.from_dict(malls_by_district, orient='index', columns=['District', 'Number of Malls'])
malls_df = malls_df.sort_values(by='Number of Malls', ascending=False)
mean_malls= round(statistics.mean(malls_df["Number of Malls"]))
summ =0
for i in malls_df["Number of Malls"]:
    summ += (mean_malls - i) ** 2
standart_deviation_malls = int(math.sqrt(summ / len(malls_df["Number of Malls"])))
print("Standart deviation malls:", standart_deviation_malls)

#Calculation
'''def assign_malls_points(x):
    if x <= mean_malls+ standart_deviation_malls/ 2 and x >= mean_malls - standart_deviation_density/2:
        malls_points = 1
    elif x < mean_malls - standart_deviation_density and x >= mean_malls - 2 * standart_deviation_density:
        malls_points = 0.5
    elif x < mean_malls - 2 * standart_deviation_density:
        malls_points = 0.25
    elif x > mean_malls + standart_deviation_density and x <= mean_malls + 2 * standart_deviation_density:
        malls_points = 0.5
    elif x > mean_malls + 2 * standart_deviation_density:
        malls_points = 0.25
    return malls_points'''

#malls_df["Points"] = malls_df["Number of Malls"].apply(assign_malls_points)


gyms = {1: ['ЦАО', 109], 2: ['ЗАО', 95], 3: ['СЗАО', 74], 4: ['ЮЗАО', 57], 5: ['ЮАО', 63], 6: ['ЮВАО', 64], 7: ['ВАО', 94], 8: ['СВАО', 91], 9: ['САО', 87]}
gyms_df = pd.DataFrame.from_dict(gyms, orient='index', columns=['District', 'Number of Gyms'])
gyms_df = gyms_df.sort_values(by='Number of Gyms', ascending=False)
#Calculation
def assign_rent_points(x):
    if x <= mean_rent+ standart_deviation_density and x >= mean_rent - standart_deviation_density:
        rent_points = 1
    elif x < mean_rent - standart_deviation_density and x >= mean_rent - 2 * standart_deviation_density:
        rent_points = 0.5
    elif x < mean_rent - 2 * standart_deviation_density:
        rent_points = 0.25
    elif x > mean_rent + standart_deviation_density and x <= mean_rent + 2 * standart_deviation_density:
        rent_points = 0.5
    elif x > mean_rent + 2 * standart_deviation_density:
        rent_points = 0.25
    return rent_points



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
                
            ]
        ),
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
                            figure = px.scatter(
                                rent_mean_df,
                                x="District",
                                y="Mean rent",
                                title="Средняя стоимость аренды по округам",
                                hover_data={"District":False, "Mean rent":True},
                                size='Mean rent',
                                color='Mean rent',
                                color_continuous_scale=color_scale,
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
                        'width': "30vw",
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
                                'height': "60vh",
                                'width': "30vw", 
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