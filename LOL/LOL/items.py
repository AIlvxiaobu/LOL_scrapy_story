# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LolItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field() #英雄名
    story = scrapy.Field() #英雄故事
    pass
