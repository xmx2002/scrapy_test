# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FtestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class FreebufItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    
class replaceItem(scrapy.Item):
    html_name = scrapy.Field()
    pic_url = scrapy.Field()
    pic_local = scrapy.Field()
    
    
class HuarenItem(scrapy.Item):
    # define the fields for your item here like:
    word = scrapy.Field()
    frequency = scrapy.Field()
    valid = scrapy.Field()