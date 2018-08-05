import scrapy
import json
import time

from ..items import GzweatherItem

class WeatherSpider(scrapy.Spider):
    name = "humidity"
    nowaday = time.strftime("%Y-%m-%d", time.localtime())
    start_urls = ["http://data.tqyb.com.cn/webLocalOssmob01/ns/rhChart.do?nowDay=" + nowaday + "&obtid=G3101"]

    def parse(self, response):
        print(response)
        gz = GzweatherItem()
        data = json.loads(response.xpath("/html/body").extract()[0].split("gz_autoStationLive = ")[1][:-23].replace("\n", ""))
        last_date = data['moniDate'].split(' ')[0]
        now_date = data['moniDate'].split(' ')[3]
        hour_list = data["hoursList"]
        t_list = data["data"]["G3155"]["actT"]
        r_list = data["data"]["G3155"]["actR"]
        ws_list = data["data"]["G3155"]["actWS"]
        wd_list = data["data"]["G3155"]["actWD"]
        flag = 0
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
            yield gz