# -*- coding: utf-8 -*-
import logging

import scrapy

from qiubai_proj.items import QiubaiProjItem


def create_hash_msg(input_str, type="sha1"):
    import hashlib
    hash_inst = hashlib.sha1(input_str.encode('utf8')) \
        if type == "sha1" else hashlib.md5(input_str.encode('utf8'))
    return hash_inst.hexdigest()


class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com']

    def parse(self, response):
        div_list = response.xpath('//div[@id="content-left"]/div[starts-with(@id, "qiushi_tag_")]')
        self.log(f"[QiubaiSpider] response current_url:{response.url}, fetch {len(div_list)} count.", level=logging.INFO)
        for div in div_list:
            image_url = div.xpath('./div[@class="author clearfix"]/a/img/@src').extract_first()
            if image_url is not None:
                image_url = "https:" + image_url
            name = div.xpath('./div[@class="author clearfix"]//h2/text()').extract_first().strip("\n")
            age = div.xpath('./div[@class="author clearfix"]/div/text()').extract_first()
            tmp_sex = div.xpath('./div[@class="author clearfix"]/div/@class').extract_first()
            sex = tmp_sex.split(" ")[-1][:-4] if tmp_sex is not None else None
            contents = div.xpath('./a/div[@class="content"]/span/text()').extract()

            content = ' '.join([ct.strip() for ct in contents])
            image_figer = create_hash_msg(image_url) if image_url != None else ''
            qb_item = QiubaiProjItem(image_url=[image_url], name=name, sex=sex, age=age, content=content,image_figer=image_figer)
            yield qb_item

        next_page = response.xpath('//ul[@class="pagination"]/li/a/span[@class="next"]/../@href').extract_first()
        # print(next_page)
        if next_page is not None:
            next_url = self.start_urls[0] + next_page
            self.log(f"start to scrapy next_url:{next_url}", level=logging.INFO)
            r = scrapy.Request(url=next_url)
            yield r

    def parse_detail(self, response):
        pass
