# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from images360.items import Images360Item
import pymysql
import  pymongo
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from scrapy import Request
import shutil

class Images360Pipeline(object):
    def open_spider(self,spider):
        try:
            self.conn = pymysql.connect(host='192.168.0.47', port=3306, user='root', passwd='spider', db='story',use_unicode = True,charset='utf8')
            self.cursor = self.conn.cursor()
            print('连接成功。。。')
        except Exception as e:
            print('数据库连接失败。。',e)
    def process_item(self, item, spider):
        if isinstance(item,Images360Item):
            try:
                insert_sql = ''' INSERT INTO image(IMAGEID,URL,TITLE,THUMB)  VALUES ("{}","{}","{}","{}")'''.format(item['id'],item['url'],item['title'],item['thumb'])
                self.cursor.execute(insert_sql)
                self.conn.commit()
                print('数据插入成功。。')
            except Exception as e:
                print('数据插入失败。。',e)
        return item
    def close_spider(self):
        self.conn.close()
class Images360MongoPipeline(object):
    def open_spider(self,spider):
        try:
            self.client = pymongo.MongoClient('127.0.0.1',27017)
            self.db = self.client['images']
            self.collection = self.db['image']
            print('连接成功。。')
        except Exception as e:
            print('连接失败。。',e)

    def process_item(self,item,spider):
        self.collection.insert(dict(item))
        print('数据插入成功。。。')
        return item
class Images360SavePipeline(ImagesPipeline):
    # def file_path(self, request, response=None, info=None):
    #     url = request.url
    #     file_name = url.split('/')[-1]
    #     return file_name
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')
    UA = get_project_settings().get('SAVE_HEADERS')
    def get_media_requests(self, item, info):
        url = item['url'].replace('https','http')
        # for ima_url in [item['url']]:
        print('运行到了。。。')
        yield Request(url, headers=self.UA,meta={'item': item})
    def item_completed(self, results, item, info):
        image_paths = [ x['path'] for ok, x in results if ok ]
        if not image_paths:
            raise DropItem("Item contains no images")
        # img_path = "%s%s" % (self.IMAGES_STORE, '\\'+ item['img_paths'])
        # if os.path.exists(img_path) == False:
        #     os.mkdir(img_path)
        # shutil.move(self.IMAGES_STORE + "\\" + image_paths[0],self.IMAGES_STORE   + '\\' + img_path.replace('E:\\images360\\images\\','') + '\\'  + item["title"] + ".jpg")
        shutil.move(self.IMAGES_STORE + "\\" + image_paths[0], self.IMAGES_STORE   +  '\\'  + item["title"] + ".jpg")
        #存放到单独的文件目录
        # item['img_paths'] = self.IMAGES_STORE   + '\\' + img_path.replace('E:\\images360\\images\\','') + '\\'  + item["title"] + ".jpg"
        #存放到images目录
        item['img_paths'] = self.IMAGES_STORE   +  '\\'  + item["title"] + ".jpg"
        return item







