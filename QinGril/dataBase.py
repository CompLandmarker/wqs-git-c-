#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/05/30 02:33
# @Author  : Shyazhut
# @File    : dataBase.py
# @Project : WQ
# @Description: ::


import pymysql

# 数据库连接
conn = pymysql.connect(host='localhost', user='root', password='19951103', db='scary_wq', port=3306)

# 使用cursor()方法获取操作游标
cur = conn.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
sql = "DROP TABLE IF EXISTS hhhhh"
cur.execute(sql)


# 数据库测试
aa = "ffgg"
bb = "jj"
sql = """CREATE TABLE ty666(
            a VARCHAR(100), 
            b VARCHAR(100))"""



sata = cur.execute(sql)

conn.commit()

cur.close()
conn.close()
