# -*- coding: utf-8 -*-
import scrapy
from urllib import request

from ..items import data_save


class CstSpider(scrapy.Spider):
    name = 'cst'
    allowed_domains = ['neusoft.edu.cn']
    start_urls = ['http://zypt.neusoft.edu.cn/hasdb/pubfiles/gongshi2016//index.html']

    def parse(self, response):
        print("**********************")
        pages = response.xpath("//span/a/text()").extract()[5]
        herf = response.xpath("//span/a/@href").extract()[5]
        new_url = url = "http://zypt.neusoft.edu.cn/hasdb/pubfiles/gongshi2016//" + herf
        yield scrapy.Request(
            new_url,
            callback=self.pares_profession,
        )

    def pares_profession(self, response):
        # print(response)
        collages = response.xpath("//td/a/text()").extract()
        collages_url = response.xpath("//td/a/@href").extract()

        for i in range(0, len(collages_url), 2):
            col_url = "http://zypt.neusoft.edu.cn/hasdb/pubfiles/gongshi2016/" + collages_url[i].replace("..", "")

            yield scrapy.Request(
                col_url,
                callback=self.pares_getdown,
            )

    def pares_getdown(self, response):
        # 312 313 82 91
        datas = []
        datas.append(response.xpath("//tbody/tr/td/a[text()='本专业人才培养模式改革创新的具体措施与实施效果']/@href").extract_first())
        datas.append(response.xpath("//tbody/tr/td/a[text()='本专业国际化人才培养的改革措施与实施效果']/@href").extract_first())
        datas.append(response.xpath("//tbody/tr/td/a[text()='十名优秀校友简介']/@href").extract_first())
        datas.append(response.xpath("//tbody/tr/td/a[text()='专业特色、实施过程和效果说明']/@href").extract_first())

        for data in datas:
            tmp = data.replace("..", "")
            download_pages = "http://zypt.neusoft.edu.cn/hasdb/pubfiles/gongshi2016//detail" + tmp
            # print(download_pages)

            yield scrapy.Request(
                download_pages,
                callback=self.download_pdf,
                meta={"downItem": datas}
            )



    def download_pdf(self,response):
        downItem = response.meta["downItem"]
        wqs = "http://zypt.neusoft.edu.cn/hasdb/pubfiles/gongshi2016//detail"
        type = response.xpath("//h3[@class='ui-box-head-title']/text()").extract()[-1]
        urls = data_save()

        urls["collage"] = response.xpath("//h3[@class='ui-box-head-title']/a/text()").extract_first()
        urls["d312"]=0
        urls["d313"]=0
        urls["d82"]=0
        urls["d91"]=0

        get_download = response.xpath("//td/a[@target='_blank']/@href").extract_first()
        get_download = get_download.replace("../../../../..", "")
        wqs = "http://zypt.neusoft.edu.cn/hasdb/pubfiles" + get_download
        # http://zypt.neusoft.edu.cn/hasdb/pubfiles/itemfiles/IM_YQXYJJ/080901/IM_YQXYJJ-1045902-080901-DB3464.pdf
        # /itemfiles/IM_YQXYJJ/080901/IM_YQXYJJ-10477-080901-0CA386.pdf
        save_path = "../../../datas/pdf"
        if "3.12" in type:
            urls["d312"] = get_download
            save_path = save_path + f"/d312/{urls['collage']}_312.pdf"
            request.urlretrieve(wqs, save_path)

        elif "3.13" in type:
            urls["d313"] = get_download
            save_path = save_path + f"/d313/{urls['collage']}_313.pdf"
            request.urlretrieve(wqs, save_path)

        elif "8.2" in type:
            urls["d82"] = get_download
            save_path = save_path + f"/d82/{urls['collage']}_82.pdf"
            request.urlretrieve(wqs, save_path)

        elif "9.1" in type:
            urls["d91"] = get_download
            save_path = save_path + f"/d91/{urls['collage']}_91.pdf"
            request.urlretrieve(wqs, save_path)

        else:
            print("数据有误")
            return
        """
        此处下载项已经注释，因为资源网址下载项目已不可用
        """
        return urls
