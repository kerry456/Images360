'''
auth:hexl
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from images360.spiders.images import ImagesSpider

__author__ = 'Mr li'

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 获取settings.py模块的设置
settings = get_project_settings()
process = CrawlerProcess(settings=settings)

# 可以添加多个spider
# process.crawl(Spider1)
# process.crawl(BlogSpider)
process.crawl(ImagesSpider)
# 启动爬虫，会阻塞，直到爬取完成
process.start()