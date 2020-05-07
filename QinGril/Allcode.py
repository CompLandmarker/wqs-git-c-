#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/05/30 07:38
# @Author  : Shyazhut
# @File    : 代码重构.py
# @Project : WQ
# @Description: ::

import jieba.analyse
import random
from docx import Document
from collections import Counter
from pyecharts import WordCloud
import pymysql
import os
import re
from matplotlib import pyplot as plt
from pylab import *

# 全局变量
NUMBER = 15
STOPWORDS = r"./datas/my/stopwords.txt"
USERWORDS = r"./datas/my/userDict.txt"
DOCXFILES = r"./datas/docx"
WORDCLOUDSAVE = "./datas/ciyun/"

# 数据库相关
LOCAL_HOST = 'localhost'
USER = 'root'
PASSWORD = '19951103'
DATA_BASE = 'scary_wq'
PORT = 3306

# 单文件调试处理
docx_file = r"./datas/docx/All专业特色汇总.docx"


def get_text(docx_file):
    """

    :param docx_file: 接受word文件
    :return: 存储到字符串并返回
    """
    document = Document(docx_file)
    document_text = ""
    filename, filetype = os.path.splitext(docx_file)
    for paragraph in document.paragraphs:
        document_text += paragraph.text

    document_text = document_text.replace("\n", "")
    return document_text


# print(get_text(docx_file))
# exit(0)
# document_text = get_text(docx_file)


def get_data(docx_file):
    """
    处理字符串
    :param docx_file: 接受字符串
    :return:
    """
    jieba.load_userdict(USERWORDS)

    # 停用词
    fp = open(STOPWORDS, "r", encoding="utf-8")
    tmp = fp.readlines()
    for i in range(0, len(tmp)):
        tmp[i] = tmp[i].replace("\n", "")

    fp.close()

    # 字典数据
    stopwords = {}.fromkeys(tmp)

    # 此处调用第一个函数
    content = get_text(docx_file)

    # 第一次分词，去除停用词
    segs = jieba.cut(content, cut_all=True)
    final = ''
    for seg in segs:
        if seg not in stopwords:
            final += seg

    # 此处的分词不包括停用词
    # segs数据是迭代器
    segs = jieba.cut(final, cut_all=False)
    # print(segs)

    # 此处使用Counter函数进行统计
    results = Counter(segs)

    # NUMBER作为全局变量，显示出需要统计词频的个数
    datas = results.most_common(NUMBER)

    return datas


# 得到分词数据
datas = get_data(docx_file)


# print(data)
# print(document_text)
# exit(0)

def wq_cool(filename, datas):
    """
    绘制词云图
    :param filename: 键入文件名
    :param datas: 数据来源
    :return:
    """
    filename = filename
    # filename = "25F33A42E25D0C1(HEX)"

    shape = ['circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star']
    # 词云内置轮廓圆，心形，钻石，三角形，三角形，五角大楼，星星

    # 显示的字词
    names = []

    # 字词频率
    values = []

    for data in datas:
        names.append(data[0])
        values.append(data[1])

    # 设置词频图的大小
    wordcloud = WordCloud(width=1300, height=620)

    # 词云图设置
    # 此处有bug 2019年6月4日19:52:29 bug还没看2019年6月5日05:11:41
    # 这是由于 当且仅当形为默认的'circle'时rotate_step参数才生效 2019年6月6日21:26:26
    # wordcloud.add("", names, values, word_size_range=[20, 100], shape=choice(shape))

    wordcloud.add("", names, values, word_size_range=[20, 100], shape="circle")

    # 词云图信息,返回json数据
    wordcloud.show_config()
    wordcloud.render(f"./datas/ciyun/{filename}.html")


# wq_cool("tmp", datas)
# exit(0)


def batch_docx():
    root = DOCXFILES
    dirs = os.listdir(root)
    collages_dict = {}

    for file in dirs:
        source_file = root + '\\' + file
        filename, filetype = os.path.splitext(file)

        # 使用正则表达式确定大学名称，去除部分数字
        if "特色" not in filename:
            pattern = r"[\u4e00-\u9fa5]+"  # 获取字符串中的汉字字符
            tmp = re.compile(pattern)
            results = tmp.findall(filename)

            # 针对类似以下数据信息：15河南师范大学（10476）软件学院 -- 进行字符串拼接
            if len(results) > 1:
                filename = results[0] + results[1]
            else:
                filename = results[0]

        # 调用处理字符串函数
        datas = get_data(source_file)

        # 调用词云图的绘制函数
        wq_cool(filename, datas)

        # 进行数据的封装
        collages_dict[filename] = datas

    # 返回字典数据
    return collages_dict


def data_save(dict_key, collages_dict, scores):
    """
    数据库存储函数
    :param dict_key:字典数据的键值
    :param collages_dict: 字典数据
    :param scores: 大学计算机专业得分数
    :return:
    """
    # 建立数据库连接
    connect = pymysql.connect(host=LOCAL_HOST, user=USER, password=PASSWORD, db=DATA_BASE, port=PORT)

    # 设置游标
    cur = connect.cursor()

    i = 0
    for vv in dict_key:
        collage = vv
        reaults = collages_dict[collage]

        if "特色" not in collage:
            score = scores[i]
            i = i + 1
        else:
            score = 0.0

        # SQL语句，写入数据表数据
        sql = 'insert into comp(collage,results,score)VALUES ("{}","{}","{}")'.format(collage, reaults, score)

        # 提交SQL语言
        cur.execute(sql)
        connect.commit()

    # 游标关闭，数据库断开连接
    cur.close()
    connect.close()

    print("数据库存储完成")


def data_analysis(collages_dict):
    """
    数据分析：专业的特色性
    根据学校词频占据的比重进行分析
    :param collages_dict:
    :return:
    """
    all = collages_dict["All专业特色汇总"]

    # 新建列表
    dict_keys = list(collages_dict.keys())
    scores = []
    collages = []

    for wan in dict_keys:
        if "专业特色" in wan:
            continue

        collage = wan
        collages.append(collage)
        sum = 0

        for i in range(0, len(collage)):
            cut = 0
            for j in range(0, len(all)):
                if collage[i][0] == all[j][0]:
                    cut = collage[i][1] / all[j][1]
                    break
            sum = sum + (1.0 - cut)

        scores.append(sum)

    # 此处调用存入数据库函数
    data_save(dict_keys, collages_dict, scores)

    return collages, scores


def bing_chart(collages, scores):
    """
    绘制饼图
    :param collages: 所有大学名称
    :param scores: 大学得到的专业分数
    :return:
    """
    labels = collages
    sizes = scores
    # 饼图颜色列表
    colors_list = ['red', 'yellowgreen', 'lightskyblue', 'orange', 'yellow', 'green', 'blue']

    # 学校对应项颜色
    colors = []
    # 学校的突出性
    explode = []

    # 记录专业评估中得分最大值
    max_score = -1.0
    # 得分最大值所在的学校
    get_max_position = 0

    for i in range(0, len(collages)):
        # 此处应该考虑学校较多情况下导致颜色值不够用的问题，解决方法就是采用循环填充方法
        colors.append(colors_list[i % len(colors_list)])
        explode.append(0)
        if scores[i] > max_score:
            max_score = scores[i]
            get_max_position = i

    # 把得分最大值的学校由饼图中突显分离
    explode[get_max_position] = 0.05

    # 设置字体
    mpl.rcParams['font.sans-serif'] = ['SimHei']

    # 设置图形尺寸
    plt.figure(figsize=(6, 9))

    # kknum = random.randint(0, 90)
    patches, l_text, p_text = plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                                      labeldistance=1.1, autopct='%3.1f%%', shadow=False,
                                      startangle=90, pctdistance=0.6)

    # 设置绘图尺寸
    for t in l_text:
        t.set_size = (30)
    for t in p_text:
        t.set_size = (20)

    # 绘制饼图
    plt.axis('equal')
    plt.legend()
    plt.show()


def main():
    collages_dict = batch_docx()
    collages, cnts = data_analysis(collages_dict)
    print(collages, cnts)
    bing_chart(collages, cnts)


if __name__ == '__main__':
    main()
