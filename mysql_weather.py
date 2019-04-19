import requests
import json
import time
import pymysql


url = "http://www.tqyb.com.cn/data/gzWeather/gz_autoStationLive.js?random=0.22061433767633876"
nowaday = time.strftime("%Y-%m-%d", time.localtime())
url1 = "http://data.tqyb.com.cn/webLocalOssmob01/ns/tempChart.do?nowDay=" + nowaday + "&obtid=G3156"
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
    if mx['obtid'] == 'G3220':
        gz.max = mx['maxtemp']
        gz.max_time = mx['maxttime']
        gz.min = mx['mintemp']
        gz.min_time = mx['minttime']
        gz.wind_max_speed = mx['maxwd3smaxdf']
        gz.wind_max_direction = ""
        gz.wind_max_time = mx['wd3smaxtime'] + "  " + mx['wd3smaxdd']
        max_min_flag = 1
        break
if(max_min_flag == 0):
    for mx in max_min_list:
        if mx['obtid'] == 'G3242':
            gz.max = mx['maxtemp']
            gz.max_time = mx['maxttime']
            gz.min = mx['mintemp']
            gz.min_time = mx['minttime']
            gz.wind_max_speed = mx['maxwd3smaxdf']
            gz.wind_max_direction = ""
            gz.wind_max_time = mx['wd3smaxtime'] + "  " + mx['wd3smaxdd']
            max_min_flag = 1
            break
if (max_min_flag == 0):
    for mx in max_min_list:
        if mx['obtid'] == 'G3155':
            gz.max = mx['maxtemp']
            gz.max_time = mx['maxttime']
            gz.min = mx['mintemp']
            gz.min_time = mx['minttime']
            gz.wind_max_speed = mx['maxwd3smaxdf']
            gz.wind_max_direction = ""
            gz.wind_max_time = mx['wd3smaxtime'] + "  " + mx['wd3smaxdd']
            break
data = json.loads(r.text.split('gz_autoStationLive = ')[1][:-12])
last_date = data['moniDate'].split(' ')[0]
now_date = data['moniDate'].split(' ')[3]
hour_list = data["hoursList"]
t_list = data["data"]["G3220"]["actT"]
r_list = data["data"]["G3220"]["actR"]
ws_list = data["data"]["G3242"]["actWS"]
wd_list = data["data"]["G3242"]["actWD"]
h_list = data["data"]["G3220"]["actH"]
flag = 0
j = 0

db = pymysql.connect("localhost", "root", "3116004646", "gzweather")
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
    if j < len(json_data) and gz.dateTime == json_data[j]['ddatetime'][:-5]:
        gz.wind_max_speed = json_data[j]['wd3smaxdf'] / 10
        gz.wind_max_direction = json_data[j]['wd3smaxdd']
        gz.wind_max_time = json_data[j]['wd3smaxtime']
        if j < len(pressure_list) and pressure_list[j]['p'] is not None:
            gz.pressure = pressure_list[j]['p'] / 10
        else:
            gz.pressure = " "
    else:
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
    j = j + 1
db.commit()
db.close()
