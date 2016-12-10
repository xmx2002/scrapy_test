# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import settings
import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from spiders.freebuf import dir_path
class FtestPipeline(object):
    def process_item(self, item, spider):
        return item
class ImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if 'pic_url' in item:#如何‘图片地址’在项i目中
            #images = []#定义图片空集
            
            #dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
           # for image_url in item['pic_url']:
                #us = image_url.split('/')[3:]
                #image_file_name = '_'.join(us)
                #file_path = '%s/%s' % (dir_path, image_file_name)
                #images.append(file_path)
                #file_path=item['pic_local']
                #if os.path.exists(file_path):
                 #   continue
            #print '\n@@@@@' + item['pic_url'] + '\n'
                
            yield scrapy.Request(item['pic_url'])
                #with open(file_path, 'wb') as handle:
                    #response = requests.get(image_url, stream=True)
                    #for block in response.iter_content(1024):
                        #if not block:
                            #break
                        #handle.write(block)
                        ##item['pic_local'] = file_path
                        ##yield item
                        
        #return item
        #yield 
    def item_completed(self, results,item, info):
        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['pic_local'] = image_paths[0]
        return item
        #with open(file_path, 'wb') as handle:
            ##response = requests.get(image_url, stream=True)
            #for block in response.iter_content(1024):
                #if not block:
                    #break        
    