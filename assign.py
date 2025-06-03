def calc_points(x, mean_value, standart_deviation):
    if x <= mean_value+ standart_deviation and x >= mean_value - standart_deviation:
        rent_points = 1
    elif x < mean_value - standart_deviation and x >= mean_value - 2 * standart_deviation:
        rent_points = 0.5
    elif x < mean_value - 2 * standart_deviation:
        rent_points = 0.25
    elif x > mean_value + standart_deviation and x <= mean_value + 2 * standart_deviation:
        rent_points = 0.5
    elif x > mean_value + 2 * standart_deviation:
        rent_points = 0.25
    return rent_points


#rent_mean_df["Points"] = rent_mean_df["Mean rent"].apply(assign_rent_points)
#print(rent_mean_df)