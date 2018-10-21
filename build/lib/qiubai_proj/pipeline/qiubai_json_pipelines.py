# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter, CsvItemExporter, XmlItemExporter

'''
导出数据到exportor.json文件里面
'''
class QiubaiProjPipeline(object):

    def __init__(self):
        self.__json_file = open("qiubai_exporter.json", "wb")
        #产生一个exporter实例
        self.__exporter = JsonItemExporter(self.__json_file, encoding="utf-8", ensure_ascii=False)
        #开始导出数据
        self.__exporter.start_exporting()


    def close_spider(self, spider):
        self.__exporter.finish_exporting()
        self.__json_file.close()

    def process_item(self, item, spider):
        '''
        处理item数据
        :param item: 从spiders通过yield发送过来数据
        :param spider: 从spiders里面选取的spider
        :return:
        '''
        self.__exporter.export_item(item)
        return item
