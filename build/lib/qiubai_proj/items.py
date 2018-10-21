# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiubaiProjItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    age = scrapy.Field()
    content = scrapy.Field()
    image_figer = scrapy.Field()


class ToScrapeItem(scrapy.Item):
    img_url = scrapy.Field()
    detail_url = scrapy.Field()
    book_name = scrapy.Field()
    book_price = scrapy.Field()
    book_description = scrapy.Field()

