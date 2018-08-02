# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 爬取的数据项
class HelloItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text=scrapy.Field()
    author=scrapy.Field()
    tags=scrapy.Field() 


class UserItem(scrapy.Item):
    avatar_url=scrapy.Field()
    url_token=scrapy.Field()
    name=scrapy.Field()
