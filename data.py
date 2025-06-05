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
        "Пресненский", "Хамовники", "Якиманка"
    ],
    "САО": [
        "Аэропорт", "Беговой", "Бескудниковский", "Войковский", "Головинский"
        , "Дмитровский", "Коптево",
        "Левобережный", "Молжаниновский", "Савёловский", "Сокол",
        "Тимирязевский", "Ховрино", "Хорошёвский"
    ],
    "СВАО": [
        "Алексеевский", "Алтуфьевский", "Бабушкинский", "Бибирево",
        "Лианозово", "Лосиноостровский", "Марфино", "Марьина роща",
        "Медведково Северное", "Медведково Южное", "Останкинский",
        "Ростокино", "Свиблово", "Северный", "Ярославский"
    ],
    "ВАО": [
        "Богородское", "Вешняки", "Восточный", "Ивановское",
        "Косино-Ухтомский", "Метрогородок", "Новогиреево", "Новокосино", "Преображенское", "Сокольники"
    ],
    "ЮВАО": [
        "Выхино-Жулебино", "Люблино",
        "Марьино", "Рязанский",
        "Текстильщики", "Южнопортовый"
    ],
    "ЮАО": [
        "Бирюлёво Восточное", "Братеево", "Даниловский",
        "Донской", "Зябликово", "Москворечье-Сабурово", "Нагатино-Садовники",
        "Нагатинский затон", "Нагорный", "Орехово-Борисово Северное",
        "Орехово-Борисово Южное", "Царицыно"
    ],
    "ЮЗАО": [
        "Академический", "Бутово Северное", "Бутово Южное", "Гагаринский",
        "Зюзино", "Котловка", "Ломоносовский", "Обручевский",
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
den["Color"] = den["Density"].apply(assign_color)
color_map_districts = dict(zip(den["District"], den["Color"]))

air_sources = pd.DataFrame(pd.read_csv("air.csv")).iloc[:, [0, 1]]
air_sources.columns = ["District", "Number of Parks"]
sorted_airs = air_sources.sort_values(by="Number of Parks")
air = sorted_airs.groupby("Number of Parks")["District"].apply(list).reset_index()
color_scale = ["#6092cd", "#89cdf0", "#61b546", "#f4a522", "#aa4498"]
mean_parks = round(statistics.mean(air_sources["Number of Parks"]))
summ_parks = 0
for i in air_sources["Number of Parks"]:
    summ_parks += (mean_parks - i) ** 2
standart_deviation_parks = int(math.sqrt(summ_parks / len(air_sources["Number of Parks"])))

def assign_parks_points(x):
    if x >= mean_parks + 2 * standart_deviation_parks:
        parks_points = 1.0
    elif x >= mean_parks + standart_deviation_parks:
        parks_points = 0.75
    elif x >= mean_parks:
        parks_points = 0.5
    elif x >= mean_parks - standart_deviation_parks:
        parks_points = 0.25
    else:
        parks_points = 0.0
    return parks_points

air_sources["Points"] = air_sources["Number of Parks"].apply(assign_parks_points)

price_pattern = r'^\d+\.?\d*\.?'
rent = pd.DataFrame()
rent_mean_df = pd.DataFrame(columns=["District, Rent"])
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
    new_data = pd.DataFrame({"District": [id_df], "Rent": [rent_mean]})
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
rent_mean_df = rent_mean_df.sort_values(by="Rent", ascending=False)

mean_rent = round(statistics.mean(rent_mean_df["Rent"]))
summ = 0
for i in rent_mean_df["Rent"]:
    summ += (mean_rent - i) ** 2
standart_deviation_rent = int(math.sqrt(summ / len(rent_mean_df["Rent"])))

#Calculating points of rent
def assign_rent_points(x):
    if x >= mean_rent:
        rent_points = 1
    else:
        rent_points = 0
    return rent_points

rent_mean_df["Points"] = rent_mean_df["Rent"].apply(assign_rent_points)

malls_by_district = {1: ["ЦАО", 27], 2: ["ЮАО",48], 3: ["САО", 26], 4: ["ВАО", 27], 5: ["ЗАО", 24], 6: ["СВАО", 24], 7: ["ЮВАО",22], 8:["СЗАО",17], 9: ["ЮЗАО", 29]}
malls_df = pd.DataFrame.from_dict(malls_by_district, orient='index', columns=['District', 'Number of Malls'])
malls_df = malls_df.sort_values(by='Number of Malls', ascending=False)
mean_malls= round(statistics.mean(malls_df["Number of Malls"]))
summ =0
for i in malls_df["Number of Malls"]:
    summ += (mean_malls - i) ** 2
standart_deviation_malls = int(math.sqrt(summ / len(malls_df["Number of Malls"])))

#Calculating mall points
def assign_malls_points(x):
    if x <= mean_malls+ standart_deviation_malls and x >= mean_malls - standart_deviation_malls:
        malls_points = 0.5
    elif x > mean_malls + standart_deviation_malls:
        malls_points = 1
    elif x < mean_malls - standart_deviation_malls:
        malls_points = 0.25
    return malls_points

malls_df["Points"] = malls_df["Number of Malls"].apply(assign_malls_points)


gyms = {1: ['ЦАО', 109], 2: ['ЗАО', 95], 3: ['СЗАО', 74], 4: ['ЮЗАО', 57], 5: ['ЮАО', 63], 6: ['ЮВАО', 64], 7: ['ВАО', 94], 8: ['СВАО', 91], 9: ['САО', 87]}
gyms_df = pd.DataFrame.from_dict(gyms, orient='index', columns=['District', 'Number of Gyms'])
gyms_df = gyms_df.sort_values(by='Number of Gyms', ascending=False)
mean_gyms= round(statistics.mean(gyms_df["Number of Gyms"]))
summ =0
for i in gyms_df["Number of Gyms"]:
    summ += (mean_gyms - i) ** 2
standart_deviation_gyms = int(math.sqrt(summ / len(gyms_df["Number of Gyms"])))

#Calculation of gyms points
def assign_gym_points(x):
    if x >= mean_gyms + 2 * standart_deviation_gyms:
        gym_points = 1.0
    elif x >= mean_gyms + standart_deviation_gyms:
        gym_points = 0.75
    elif x >= mean_gyms:
        gym_points = 0.5
    elif x >= mean_gyms - standart_deviation_gyms:
        gym_points = 0.25
    else:
        gym_points = 0.0
    return gym_points
gyms_df["Points"] = gyms_df["Number of Gyms"].apply(assign_gym_points)

districts_data = [('Академический', 9), ('Алексеевский', 9), ('Алтуфьевский', 8), ('Арбат', 9), ('Аэропорт', 8), ('Бабушкинский', 7), ('Басманный', 7), ('Беговой', 9), ('Бескудниковский', 7), ('Бибирево', 6), ('Бирюлево Восточное', 5), ('Бирюлево Западное', 8), ('Богородское', 5), ('Братеево', 5), ('Бутырский', 10), ('Вешняки', 6), ('Внуково', 8), ('Войковский', 6), ('Восточное Дегунино', 6), ('Восточное Измайлово', 3), ('Восточный', 3), ('Выхино-Жулебино', 6), ('Гагаринский', 7), ('Головинский', 6), ('Гольяново', 6), ('Даниловский', 8), ('Дмитровский', 8), ('Донской', 9), ('Дорогомилово', 8), ('Замоскворечье', 8), ('Западное Дегунино', 10), ('Зюзино', 8), ('Зябликово', 6), ('Ивановское', 4), ('Измайлово', 2), ('Капотня', 10), ('Коньково', 8), ('Коптево', 8), ('Косино-Ухтомский', 5), ('Котловка', 7), ('Красносельский', 9), ('Крылатское', 2), ('Крюково', 5), ('Кузьминки', 3), ('Кунцево', 4), ('Куркино', 3), ('Левобережный', 6), ('Лефортово', 7), ('Лианозово', 7), ('Ломоносовский', 7), ('Лосиноостровский', 6), ('Люблино', 6), ('Марфино', 7), ('Марьина роща', 9), ('Марьино', 5), ('Матушкино', 6), ('Метрогородок', 2), ('Мещанский', 8), ('Митино', 5), ('Можайский', 6), ('Молжаниновский', 4), ('Москворечье-Сабурово', 7), ('Нагатино-Садовники', 8), ('Нагатинский Затон', 4), ('Нагорный', 9), ('Некрасовка', 7), ('Нижегородский', 10), ('Новогиреево', 7), ('Новокосино', 9), ('Новопеределкино', 4), ('Обручевский', 7), ('Орехово-Борисово Северное', 3), ('Орехово-Борисово Южное', 7), ('Останкинский', 4), ('Отрадное', 6), ('Очаково-Матвеевское', 8), ('Перово', 8), ('Печатники', 6), ('Покровское-Стрешнево', 5), ('Поселение Внуковское', 2), ('Поселение Вороновское', 1), ('Поселение Воскресенское', 2), ('Поселение Десеновское', 2), ('Поселение Киевский', 1), ('Поселение Кленовское', 1), ('Поселение Кокошкино', 3), ('Поселение Краснопахорское', 2), ('Поселение Марушкинское', 4), ('Поселение Михайлово-Ярцевское', 1), ('Поселение Московский', 2), ('Поселение Мосрентген', 6), ('Поселение Новофедоровское', 1), ('Поселение Первомайское', 1), ('Поселение Роговское', 1), ('Поселение Рязановское', 2), ('Поселение Сосенское', 3), ('Поселение Троицк', 2), ('Поселение Филимоновское', 2), ('Поселение Шаповское', 2), ('Поселение Щербинка', 6), ('Преображенское', 8), ('Пресненский', 9), ('Проспект Вернандского', 7), ('Раменки', 6), ('Ростокино', 5), ('Рязанский', 9), ('Савелки', 4), ('Савеловский', 8), ('Свиблово', 7), ('Северное Бутово', 4), ('Северное Измайлово', 8), ('Северное Медведково', 8), ('Северное Тушино', 5), ('Северный', 5), ('Силино', 3), ('Сокол', 8), ('Соколиная гора', 10), ('Сокольники', 4), ('Солнцево', 6), ('Старое Крюково', 5), ('Строгино', 5), ('Таганский', 7), ('Тверской', 7), ('Текстильщики', 9), ('Теплый стан', 6), ('Тимирязевский', 5), ('Тропарево-Никулино', 7), ('Филевский парк', 4), ('Фили-Давыдково', 7), ('Хамовники', 6), ('Ховрино', 6), ('Хорошево-Мневники', 6), ('Хорошевский', 7), ('Царицыно', 6), ('Черемушки', 9), ('Чертаново Северное', 8), ('Чертаново Центральное', 7), ('Чертаново Южное', 6), ('Щукино', 5), ('Южное Бутово', 5), ('Южное Медведково', 6), ('Южное Тушино', 5), ('Южнопортовый', 9), ('Якиманка', 7), ('Ярославский', 7), ('Ясенево', 3)]

df = pd.DataFrame(districts_data, columns=['District', 'Number of Points'])

def assign_ecology_points(num):
    if num >= 9:
        return 0.0 
    elif num>= 7:
        return 0.25 
    elif num >= 4:
        return 0.5 
    elif num >= 2:
        return 0.75 
    else:
        return 1.0 
df['Ecology Points'] = df['Number of Points'].apply(assign_ecology_points)


def calculate_overall_district_scores(
    districts_by_admin_okrug,
    gyms_df,
    rent_mean_df,
    malls_df,
    sorted_density,
    air_sources
):
    municipal_to_admin_mapping = {
        municipal_district: admin_okrug
        for admin_okrug, municipal_districts in districts_by_admin_okrug.items()
        for municipal_district in municipal_districts
    }

    all_municipal_districts_list = list(municipal_to_admin_mapping.keys())
    final_points_df = pd.DataFrame(all_municipal_districts_list, columns=['Municipal_District'])
    final_points_df['Admin_Okrug'] = final_points_df['Municipal_District'].map(municipal_to_admin_mapping)

    density_points_municipal = sorted_density[['District', 'Points']].copy()
    density_points_municipal.rename(columns={'District': 'Municipal_District', 'Points': 'Density_Points'}, inplace=True)
    final_points_df = pd.merge(final_points_df, density_points_municipal, on='Municipal_District', how='left')

    air_points_municipal = air_sources[['District', 'Points']].copy()
    air_points_municipal.rename(columns={'District': 'Municipal_District', 'Points': 'Air_Points'}, inplace=True)
    final_points_df = pd.merge(final_points_df, air_points_municipal, on='Municipal_District', how='left')

    gyms_admin_points = gyms_df[['District', 'Points']].copy()
    gyms_admin_points.rename(columns={'District': 'Admin_Okrug', 'Points': 'Gyms_Points'}, inplace=True)

    rent_admin_points = rent_mean_df[['District', 'Points']].copy()
    rent_admin_points.rename(columns={'District': 'Admin_Okrug', 'Points': 'Rent_Points'}, inplace=True)

    malls_admin_points = malls_df[['District', 'Points']].copy()
    malls_admin_points.rename(columns={'District': 'Admin_Okrug', 'Points': 'Malls_Points'}, inplace=True)

    final_points_df = pd.merge(final_points_df, gyms_admin_points, on='Admin_Okrug', how='left')
    final_points_df = pd.merge(final_points_df, rent_admin_points, on='Admin_Okrug', how='left')
    final_points_df = pd.merge(final_points_df, malls_admin_points, on='Admin_Okrug', how='left')
    
    point_columns = ['Density_Points', 'Air_Points', 'Gyms_Points', 'Rent_Points', 'Malls_Points']
    
    final_points_df[point_columns] = final_points_df[point_columns].fillna(0)
    
    final_points_df['Total_Points'] = final_points_df[point_columns].sum(axis=1)

    return final_points_df

overall_scores_df = calculate_overall_district_scores(
    districts_by_admin_okrug,
    gyms_df,
    rent_mean_df,
    malls_df,
    sorted_density,
    air_sources
)

print("\n--- Общие баллы для каждого муниципального района ---")
print(overall_scores_df.sort_values(by='Total_Points', ascending=False).iloc[:, [0, 1, -1]].head(20))


app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "display": "grid",
        "grid-template-columns": "20vw 30vw 30vw", 
        "gap": "20px",
        "height": "auto",
        "width": "fit-content",
        "padding": "20px",
        "box-sizing": "border-box"
    },
    children=[
        html.H1("Лучшие районы г. Москва для молодых специалистов",
                style={'grid-column': '1 / -1', 'margin-bottom': '20px'}),
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
                'grid-column': '2',
                'display': 'flex',
                'flex-direction': 'column',
                'gap': '20px',
                'width': '30vw', 
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
                                y="Rent",
                                title="Средняя стоимость аренды по округам",
                                hover_data={"District":False, "Rent":True},
                                size='Rent',
                                color='Rent',
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
                                x="Number of Parks",
                                y="Number of Parks",
                                title="Количество лесов и парков по районам",
                                hover_data={'Number of Parks': True, 'District': False},
                                color=air['Number of Parks'],
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
                    style={'height': "auto", "width": "30vw", 'box-sizing': 'border-box'} 
                ),
            ]
        ),
        html.Div( 
            style={
                'grid-column': '3',
                'display': 'flex',
                'flex-direction': 'column',
                'gap': '20px',
                'width': '30vw',
                'box-sizing': 'border-box'
            },
            children=[
                html.Div(
                    [
                        dcc.Graph(
                            id="gyms-plot",
                            figure = px.scatter(
                                gyms_df,
                                x="District",
                                y="Number of Gyms",
                                title="Количество спортзалов по округам",
                                hover_data={"District":True, "Number of Gyms":True},
                                size='Number of Gyms',
                                color='Number of Gyms',
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
            html.H3(f"Районы с {districts_info['Number of Parks']} источниками воздуха:"),
            html.Ul([html.Li(district) for district in districts_list])
        ])
    return html.P("Нажмите на столбец, чтобы увидеть список районов.")

if __name__ == "__main__":
    app.run(debug=True)