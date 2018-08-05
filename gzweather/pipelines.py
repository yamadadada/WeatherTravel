# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

from .items import GzweatherItem

class GzweatherPipeline(object):
    def open_spider(self, spider):
        self.con = sqlite3.connect("gzweather.sqlite")
        self.cu = self.con.cursor()

    def process_item(self, item, spider):
        if isinstance(item, GzweatherItem):
            replace_sql = "replace into weather (dateTime, temperature, rain, windSpeed, windDirection, windmaxspeed, windmaxdirection, windmaxtime, humidity, pressure, max, maxttime, min, minttime) VALUES('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') ".format(
                item['dateTime'], item['temperature'], item['rain'], item['windSpeed'], item['windDirection'], item['wind_max_speed'], item['wind_max_direction'], item['wind_max_time'], item['humidity'], item['pressure'], item['max'], item['max_time'], item['min'], item['min_time'])
        self.cu.execute(replace_sql)
        self.con.commit()
        return item

    def spider_close(self, spider):
        self.con.close()
