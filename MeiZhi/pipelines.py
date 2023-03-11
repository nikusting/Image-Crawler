# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql.cursors
from scrapy.http import Request
import re
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MeizhiPipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_settings(cls,settings):
        dbparams=dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool("pymysql",**dbparams)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self,failure,item,spider):

        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
                insert into meizhi(name,image_url)
                VALUES (%s,%s)
                """
        # params = (item["name"], item["image_url"])
        cursor.execute(insert_sql,(item['name'],item['image_url']))

        return item

# class MyImagesPipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         for image_url in item['image_url']:
#             return [Request(image_url, meta={'name':item['name']},callback=self.file_path)]
#
#     def file_path(self, request, response=None, info=None):
#         name = request.meta['name']
#         # name = filter(lambda x: x not in '()0123456789', name)
#         name = re.sub(r'[？\\*|“<>:/()0123456789]', '', name)
#         image_guid = request.url.split('/')[-1]
#         # name2 = request.url.split('/')[-2]
#         filename = u'full/{0}/{1}'.format(name, image_guid)
#         return filename
#         # return 'full/%s' % (image_guid)
#
#     def item_completed(self, results, item, info):
#         if "image_url" in item:
#             for ok,value in results:
#                 image_path=value["path"]
#             item["image_path"]=image_path
#         return item