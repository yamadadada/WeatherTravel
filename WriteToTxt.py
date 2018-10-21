import sqlite3


def parse_direction(wind_direction):
    if wind_direction == " " or wind_direction == "None" or wind_direction == "":
        return " "
    wind_direction = float(wind_direction)
    if wind_direction < 11.25 or wind_direction > 348.75:
        return "北"
    elif 11.25 < wind_direction < 33.75:
        return "东北偏北"
    elif 33.75 < wind_direction < 56.25:
        return "东北"
    elif 56.25 < wind_direction < 78.75:
        return "东北偏东"
    elif 78.75 < wind_direction < 101.25:
        return "东"
    elif 101.25 < wind_direction < 123.75:
        return "东南偏东"
    elif 123.75 < wind_direction < 146.25:
        return "东南"
    elif 146.25 < wind_direction < 168.75:
        return "东南偏南"
    elif 168.75 < wind_direction < 191.25:
        return "南"
    elif 191.25 < wind_direction < 213.75:
        return "西南偏南"
    elif 213.75 < wind_direction < 236.25:
        return "西南"
    elif 236.25 < wind_direction < 258.75:
        return "西南偏西"
    elif 258.75 < wind_direction < 281.25:
        return "西"
    elif 281.25 < wind_direction < 303.75:
        return "西北偏西"
    elif 303.75 < wind_direction < 326.25:
        return "西北"
    elif 326.25 < wind_direction < 348.75:
        return "西北偏北"
    return " "


mydb = sqlite3.connect("gzweather.sqlite")
cursor = mydb.cursor()
sql = "select * from weather"
results = cursor.execute(sql)
data = cursor.fetchall()
with open("WeatherData.txt", 'w') as f:
    f.write("时间,温度,降水量,风速,风向,湿度,气压,最大风速,风向,出现时间,最高温,最低温,最高温时间,最低温时间\n")
with open("WeatherData.txt", 'a') as f:
    for aa in data:
        a = list(aa)
        f.write(a[0] + ",")
        f.write(a[1] + ",")
        f.write(a[2] + ",")
        f.write(a[3] + ",")
        f.write(parse_direction(a[4]) + ",")
        f.write(a[5] + ",")
        f.write(a[6] + ",")
        f.write(a[8] + ",")
        f.write(parse_direction(a[9]) + ",")
        f.write(a[10] + ",")
        f.write(a[11] + ",")
        f.write(a[13] + ",")
        f.write(a[14] + ",")
        f.write(a[15] + "\n")
print("Write to successful!")
