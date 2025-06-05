import math
def calc_points(x, column_name):
    x_mean = x[column_name].sum() / len(x[column_name])
    summ = 0
    for i in x["Density"]:
        summ += (x_mean - i) ** 2
    standart_deviation = int(math.sqrt(summ / len(x[column_name])))
    print("Standart deviation density:", standart_deviation)
    if x <= x_mean+ standart_deviation and x >= x_mean - standart_deviation:
        points = 1
    elif x < x_mean - standart_deviation and x >= x_mean - 2 * standart_deviation:
        points = 0.5
    elif x < x_mean - 2 * standart_deviation:
        points = 0.25
    elif x > x_mean + standart_deviation and x <= x_mean + 2 * standart_deviation:
        points = 0.5
    elif x > x_mean + 2 * standart_deviation:
        points = 0.25
    return points