import scrapy

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

from ..settings import G_IMAGE_SET


class MyImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        '''
        从item数据里面提取image url, 产生Request对象
        将Request发送给scheduler
        :param item:
        :param info:
        :return:
        '''
        # print(info)
        # print("*"*40)
        if item['image_figer'] not in G_IMAGE_SET:
            G_IMAGE_SET.add(item['image_figer'])
            for image_url in item['image_url']:
                r = scrapy.Request(image_url)
                yield r
        else:
            raise DropItem("this image has existed.")

    def item_completed(self, results, item, info):
        '''
        当image_url request对象处理完成返回response对象后，下载完成后
        :param results:
        [(True,
        {'url':
         'https://pic.qiushibaike.com/system/avtnew/3902/39026737/thumb/2018062821144688.JPEG?imageView2/1/w/90/h/90',
        'path': 'full/ead9debfdeab7bdf0817993899eb643256799482.jpg',
        'checksum': '923a929b0358d9b4000e1231d7b4da05'})]
        :param item:
        :param info:
        :return:
        '''
        # print(f"item_completed: {results}")

        image_path = [data['path'] for status, data in results if status]
        if len(image_path) == 0:
            raise DropItem("this image has not existed.")
        item['image_url'] = image_path
        return item
