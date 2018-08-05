import requests
import json
import time
import pymysql


url = "http://www.tqyb.com.cn/data/gzWeather/gz_autoStationLive.js?random=0.22061433767633876"
nowaday = time.strftime("%Y-%m-%d", time.localtime())
url1 = "http://data.tqyb.com.cn/webLocalOssmob01/ns/tempChart.do?nowDay=" + nowaday + "&obtid=G3443"
url3 = "http://data.tqyb.com.cn/webLocalOssmob01/ns/tempChart.do?nowDay=" + nowaday + "&obtid=59287"
url4 = "http://www.tqyb.com.cn/data/gzWeather/obtDatas.js?random=0.80458761356101"


class GzweatherItem():
    pass


r = requests.get(url)
r1 = requests.get(url1)
r3 = requests.get(url3)
r4 = requests.get(url4)

json_data = r1.json()['dataList']
pressure_list = r3.json()['dataList']
max_min_data = json.loads(r4.text.split('gz_obtDatas = ')[1][:-12])
max_min_list = max_min_data['data']['panyu']
gz = GzweatherItem()
gz.max = " "
gz.max_time = " "
gz.min = " "
gz.min_time = " "
max_min_flag = 0
for mx in max_min_list:
    if mx['obtid'] == 'G3155':
        gz.max = mx['maxtemp']
        gz.max_time = mx['maxttime']
        gz.min = mx['mintemp']
        gz.min_time = mx['minttime']
        max_min_flag = 1
        break
if(max_min_flag == 0):
    for mx in max_min_list:
        if mx['obtid'] == 'G3242':
            gz.max = mx['maxtemp']
            gz.max_time = mx['maxttime']
            gz.min = mx['mintemp']
            gz.min_time = mx['minttime']
            max_min_flag = 1
            break
if (max_min_flag == 0):
    for mx in max_min_list:
        if mx['obtid'] == 'G3220':
            gz.max = mx['maxtemp']
            gz.max_time = mx['maxttime']
            gz.min = mx['mintemp']
            gz.min_time = mx['minttime']
            break
data = json.loads(r.text.split('gz_autoStationLive = ')[1][:-12])
last_date = data['moniDate'].split(' ')[0]
now_date = data['moniDate'].split(' ')[3]
hour_list = data["hoursList"]
t_list = data["data"]["G3155"]["actT"]
r_list = data["data"]["G3155"]["actR"]
ws_list = data["data"]["G3155"]["actWS"]
wd_list = data["data"]["G3155"]["actWD"]
h_list = data["data"]["G3220"]["actH"]
flag = 0
j = 0

db = pymysql.connect("localhost", "root", "jerry75911", "gzweather")
con = db.cursor()

for i in range(24):
    if flag == 0:
        gz.dateTime = last_date + " " + hour_list[i] + ":00"
    else:
        gz.dateTime = now_date + " " + hour_list[i] + ":00"
    if hour_list[i] == "23":
        flag = 1
    gz.temperature = t_list[i]
    gz.rain = r_list[i]
    gz.windSpeed = ws_list[i]
    gz.windDirection = wd_list[i]
    if str(h_list[i]).split(".")[0] == "null" or str(h_list[i]).split(".")[0] == "None":
        gz.humidity = ""
    else:
        gz.humidity = int(str(h_list[i]).split(".")[0]) / 100
    if i >= len(json_data):
        gz.wind_max_speed = ""
        gz.wind_max_direction = ""
        gz.wind_max_time = ""
        gz.pressure = ""
        j = j - 1
    else:
        if gz.dateTime == json_data[j]['ddatetime'][:-5]:
            gz.wind_max_speed = json_data[j]['wd3smaxdf'] / 10
            gz.wind_max_direction = json_data[j]['wd3smaxdd']
            gz.wind_max_time = json_data[j]['wd3smaxtime']
            gz.pressure = pressure_list[j]['p'] / 10
        else:
            gz.wind_max_speed = " "
            gz.wind_max_direction = " "
            gz.wind_max_time = " "
            gz.pressure = " "
            j = j - 1
    sql = "insert into weather(dateTime, temperature, rain, windSpeed, windDirection, windmaxspeed, " \
          "windmaxdirection, windmaxtime, humidity, pressure, max, maxttime, min, minttime) VALUES('{}','{}', '{}', " \
          "'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') on DUPLICATE key update temperature='{}'" \
          ", rain='{}', windSpeed='{}', windDirection='{}', windmaxspeed='{}', windmaxdirection='{}', " \
          "windmaxtime='{}', humidity='{}', pressure='{}', max='{}', maxttime='{}', min='{}', minttime='{}'"\
        .format(gz.dateTime, gz.temperature, gz.rain, gz.windSpeed, gz.windDirection, gz.wind_max_speed,
                gz.wind_max_direction, gz.wind_max_time, gz.humidity, gz.pressure, gz.max, gz.max_time, gz.min,
                gz.min_time, gz.temperature, gz.rain, gz.windSpeed, gz.windDirection, gz.wind_max_speed,
                gz.wind_max_direction, gz.wind_max_time, gz.humidity, gz.pressure, gz.max, gz.max_time, gz.min,
                gz.min_time)
    con.execute(sql)
    print("时间:" + str(gz.dateTime))
    print("温度:" + str(gz.temperature))
    print("降水量：" + str(gz.rain))
    print("风速:" + str(gz.windSpeed))
    print("风向:" + str(gz.windDirection))
    print("最大风速:" + str(gz.wind_max_speed))
    print("最大风向:" + str(gz.wind_max_direction))
    print("最大风速时间:" + str(gz.wind_max_time))
    print("湿度:" + str(gz.humidity))
    print("气压:" + str(gz.pressure))
    print("最高温度:" + str(gz.max))
    print("最高温度时间:" + str(gz.max_time))
    print("最低温度:" + str(gz.min))
    print("最低温度时间:" + str(gz.min_time))
    j = j + 1
    print("--------------------------------")
db.commit()
db.close()
