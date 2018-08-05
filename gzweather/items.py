# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GzweatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dateTime = scrapy.Field()
    temperature = scrapy.Field()
    rain = scrapy.Field()
    windSpeed = scrapy.Field()
    windDirection = scrapy.Field()
    wind_max_speed = scrapy.Field()
    wind_max_direction = scrapy.Field()
    wind_max_time = scrapy.Field()
    humidity = scrapy.Field()
    pressure = scrapy.Field()
    max = scrapy.Field()
    max_time = scrapy.Field()
    min = scrapy.Field()
    min_time = scrapy.Field()
    # pass
