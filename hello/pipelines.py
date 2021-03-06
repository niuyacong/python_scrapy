# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo
# 处理item
class HelloPipeline(object):
    def __init__(self):
        self.limit=50
    def process_item(self, item, spider):
        if item['text']:
            if len(item['text'])>self.limit:
                item['text']=item['text'][0:self.limit].rstrip()+'...'
            return item
        else:
            return DropItem('Missing Text ')

# 保存到数据库
class MongoPilpeline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_db=mongo_db
        self.mongo_url=mongo_url


    # from_crawler 拿到settings的配置参数
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    
    # 打开spider 初始化操作
    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_url)
        self.db=self.client[self.mongo_db]
    
    def process_item(self,item,spider):
        # 插入操作
        # name=self.__class__.__name__
        # self.db[name].insert(dict(item))
        #更新操作（去重）
        print(4444444)
        self.db['user'].update({'url_token':item['url_token']},{'$set':item},True)
        return item

    def close_spider(self,spider):
        self.client.close() 