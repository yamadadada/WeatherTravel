import scrapy
import json
import urllib.request
import time

from ..items import GzweatherItem

class WeatherSpider(scrapy.Spider):
    name = "gzweather"
    start_urls = ["http://www.tqyb.com.cn/data/gzWeather/gz_autoStationLive.js?random=0.22061433767633876"]

    def parse(self, response):
        print(response)
        nowaday = time.strftime("%Y-%m-%d", time.localtime())
        url1 = "http://data.tqyb.com.cn/webLocalOssmob01/ns/tempChart.do?nowDay=" + nowaday + "&obtid=G3443"
        url2 = "http://data.tqyb.com.cn/webLocalOssmob01/ns/rhChart.do?nowDay=" + nowaday + "&obtid=G3101"
        url3 = "http://data.tqyb.com.cn/webLocalOssmob01/ns/tempChart.do?nowDay=" + nowaday + "&obtid=59287"
        url4 = "http://www.tqyb.com.cn/data/gzWeather/obtDatas.js?random=0.80458761356101"
        bytes_data1 = urllib.request.urlopen(url1).read()
        bytes_data2 = urllib.request.urlopen(url2).read()
        bytes_data3 = urllib.request.urlopen(url3).read()
        bytes_data4 = urllib.request.urlopen(url4).read()
        content1 = str(bytes_data1, encoding='utf-8')
        content2 = str(bytes_data2, encoding='utf-8')
        content3 = str(bytes_data3, encoding='utf-8')
        content4 = str(bytes_data4, encoding='utf-8')
        json_data = json.loads(content1.split("dataList")[1][2:-2])
        humidity_list = json.loads(content2.split("dataList")[1][2:-2])
        pressure_list = json.loads(content3.split("dataList")[1][2:-2])
        max_min_data = json.loads(content4.split("gz_obtDatas = ")[1][:-12])
        max_min_list = max_min_data['data']['panyu']
        gz = GzweatherItem()
        gz['max'] = " "
        gz['max_time'] = " "
        gz['min'] = " "
        gz['min_time'] = " "
        max_min_flag = 0
        for mx in max_min_list:
            if mx['obtid'] == 'G3155':
                gz['max'] = mx['maxtemp']
                gz['max_time'] = mx['maxttime']
                gz['min'] = mx['mintemp']
                gz['min_time'] = mx['minttime']
                max_min_flag = 1
                break
        if(max_min_flag == 0):
            for mx in max_min_list:
                if mx['obtid'] == 'G3242':
                    gz['max'] = mx['maxtemp']
                    gz['max_time'] = mx['maxttime']
                    gz['min'] = mx['mintemp']
                    gz['min_time'] = mx['minttime']
                    max_min_flag = 1
                    break
        if (max_min_flag == 0):
            for mx in max_min_list:
                if mx['obtid'] == 'G3220':
                    gz['max'] = mx['maxtemp']
                    gz['max_time'] = mx['maxttime']
                    gz['min'] = mx['mintemp']
                    gz['min_time'] = mx['minttime']
                    break
        data = json.loads(response.xpath("/html/body").extract()[0].split("gz_autoStationLive = ")[1][:-23].replace("\n", ""))
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
        for i in range(24):
            if flag == 0:
                gz["dateTime"] = last_date + " " + hour_list[i] + ":00"
            else:
                gz["dateTime"] = now_date + " " + hour_list[i] + ":00"
            if hour_list[i] == "23":
                flag = 1
            gz["temperature"] = t_list[i]
            gz["rain"] = r_list[i]
            gz["windSpeed"] = ws_list[i]
            gz["windDirection"] = wd_list[i]
            if str(h_list[i]).split(".")[0] == "null" or str(h_list[i]).split(".")[0] == "None":
                gz["humidity"] = ""
            else:
                gz["humidity"] = int(str(h_list[i]).split(".")[0]) / 100
            if i >= len(json_data):
                gz["wind_max_speed"] = ""
                gz["wind_max_direction"] = ""
                gz["wind_max_time"] = ""
                #gz['humidity'] = ""
                gz['pressure'] = ""
                j = j - 1
            else:
                if gz["dateTime"] == json_data[j]['ddatetime'][:-5]:
                    gz["wind_max_speed"] = json_data[j]['wd3smaxdf'] / 10
                    gz["wind_max_direction"] = json_data[j]['wd3smaxdd']
                    gz["wind_max_time"] = json_data[j]['wd3smaxtime']
                    # if j < len(humidity_list):
                    #     if isinstance(humidity_list[j]['rh'], int):
                    #         gz['humidity'] = humidity_list[j]['rh'] / 100
                    #     else:
                    #         gz['humidity'] = " "
                    # else:
                    #     gz['humidity'] = " "
                    gz['pressure'] = pressure_list[j]['p'] / 10
                else:
                    print(json_data[j]['ddatetime'][:-5])
                    gz["wind_max_speed"] = " "
                    gz["wind_max_direction"] = " "
                    gz["wind_max_time"] = " "
                    # gz['humidity'] = " "
                    gz['pressure'] = " "
                    j = j - 1
            j = j + 1
            yield gz
