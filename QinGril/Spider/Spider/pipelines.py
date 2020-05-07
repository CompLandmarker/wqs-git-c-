# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class OpMySQL(object):
    def __init__(self):
        # 连接MySQL数据库
        self.connect = pymysql.connect(host='localhost', user='root', password='19951103', db='scary_wq', port=3306)
        # self.connect = pymysql.connect(host=LOCAL_HOST, user=USER, password=PASSWORD, db=DATA_BASE, port=PORT)

        self.cursor = self.connect.cursor()

    def process_item(self, urls, spider):
        sql = "SELECT * FROM comp WHERE collage = '%s' "
        data = (urls['collage'],)
        print(data)
        self.cursor.execute(sql % data)
        self.connect.commit()

        res = len(self.cursor.fetchall())
        # print(res)
        # 往数据库里面写入数据
        if res == 0:
            self.cursor.execute(
                'insert into get_data(collage,d312,d313,d82,d91)VALUES ("{}","{}","{}","{}","{}")'.format(urls['collage'],
                                                                                                          urls['d312'],
                                                                                                          urls['d313'],
                                                                                                          urls['d82'],
                                                                                                          urls['d91']))
            self.connect.commit()
            # return urls
        else:
            print("数据已存在")

        return

    # 关闭数据库
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
