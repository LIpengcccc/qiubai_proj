# -*- coding: utf-8 -*-
import logging

import scrapy

from qiubai_proj.items import ToScrapeItem


class ToscrapeSpider(scrapy.Spider):
    name = 'toscrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        li_list = response.xpath('//ol[@class="row"]/li')
        self.log(f"[ToscrapeSpider] response url:{response.url}, fetch {len(li_list)} count.", level=logging.INFO)
        # detail_urls = []
        # print(f"curent url: {response.url}, page_count:{len(li_list)}")
        for li in li_list:
            # item = ToScrapeItem()

            detail_url = li.xpath('./article/div/a/@href').extract_first()
            if detail_url.startswith('catalogue/'):
                url_item = 'http://books.toscrape.com/' + detail_url
            else:
                url_item = 'http://books.toscrape.com/' + 'catalogue/' + detail_url
            # # print(url_item)
            # detail_urls.append(url_item)
            # # print(len(detail_urls))
            # for url_item in detail_urls:
            yield scrapy.Request(url=url_item, callback=self.parse_detail)

        next_page = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            if next_page.startswith('catalogue/'):
                print(next_page)
                next_url = self.start_urls[0] + next_page
            else:
                next_url = self.start_urls[0] + 'catalogue/' + next_page
            # print(next_url)
            # self.log(f"start to scrapy next_url:{next_url}", level=logging.INFO)
            r = scrapy.Request(url=next_url, dont_filter=True)
            yield r

    def parse_detail(self, response):
        img_url = response.xpath('//div[@id="product_gallery"]//img/@src').extract_first()
        if img_url is not None:
            img_url = self.start_urls[0] + img_url[6:]
        detail_url = response.url
        book_name = response.xpath('//h1/text()').extract_first()
        book_price = response.xpath('//div[@class="col-sm-6 product_main"]/p/text()').extract_first()
        book_description = response.xpath('//div[@id="product_description"]/../p/text()').extract_first()
        if book_description is None:
            book_description = '无详细信息'
        else:
            book_description = book_description

        ts_item = ToScrapeItem(img_url=img_url, detail_url=detail_url, book_name=book_name,
                               book_price=book_price[-5:], book_description=book_description)

        yield ts_item
