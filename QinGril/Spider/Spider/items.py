# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class data_save(scrapy.Item):
    collage = scrapy.Field()
    d312 = scrapy.Field()
    d313 = scrapy.Field()
    d82 = scrapy.Field()
    d91 = scrapy.Field()

class pdf_save(scrapy.Item):
    collage = scrapy.Field()
    d312 = scrapy.Field()
    d313 = scrapy.Field()
    d82 = scrapy.Field()
    d91 = scrapy.Field()