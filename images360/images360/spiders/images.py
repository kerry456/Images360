# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode

from scrapy import Request,Spider
import json
from images360.items import Images360Item

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']
    def start_requests(self):
        data = {'ch':'beauty','listtype':'new','temp':'1'}#wallpaper,beauty
        base_url = 'http://image.so.com/zj?'
        for page in range(1,self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url,callback=self.parse)


    def parse(self, response):
        result = json.loads(response.text)
        if result.get('list'):
            print('正在爬取',response.url)
            for image in result.get('list'):
                item = Images360Item()
                item['id'] = image.get('imageid')
                item['url'] = image.get('qhimg_url')
                item['title'] = image.get('group_title')
                item['thumb'] = image.get('qhimg_thumb_url')
                item['img_paths'] = image.get('group_title')
                # item['urls'] = [image.get('qhimg_url') for image in result.get('list')]
                yield item
                # return item
        else:
            print('找不到节点。。。',response.url)



