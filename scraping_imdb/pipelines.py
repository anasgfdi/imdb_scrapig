# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from pymongo import MongoClient


# class ScrapingImdbPipeline:

#     def __init__(self):
#         self.conn=pymongo.MongoClient(
#             'localhost',27017
#         )
#         db=self.conn['movies']
#         self.collection=db['movies_detail']

#     def process_item(self, item, spider):
#         self.collection.insert(dict(item))
#         return item


class ImdbPipeline:
    def process_item(self, item, spider):
        return item


class MoviesPipeline:
    collection_name = "movies_detail"
    
    def open_spider(self, spider):
        self.client = MongoClient("mongodb://localhost:27017")
        db = self.client["moviesimdb"]

        self.movie = db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.movie.insert_one(dict(item))
        return item