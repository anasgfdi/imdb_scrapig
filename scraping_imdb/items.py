# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapingImdbItem(scrapy.Item):
    title= scrapy.Field()
    original_title= scrapy.Field()
    score= scrapy.Field()
    genre= scrapy.Field()
    date= scrapy.Field()
    synopsis=scrapy.Field()
    duree=scrapy.Field()
    casting=scrapy.Field()
    pays=scrapy.Field()