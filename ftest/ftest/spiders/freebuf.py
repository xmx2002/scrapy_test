# -*- coding: utf-8 -*-
import scrapy
from ftest.items import *
import os
import ftest.settings
dir_path = '%s/%s' % (ftest.settings.IMAGES_STORE,"freebuf")
def gen_link():
    url=['http://www.freebuf.com/articles']
    for i in range(2,215):
        #t='http://www.freebuf.com/articles/page/'+str(i)
        url.append('http://www.freebuf.com/articles/page/'+str(i))
    return url
class FreebufSpider(scrapy.Spider):
    name = "freebuf"
    #allowed_domains = ["freebuf.com"]
    #start_urls = ['http://www.freebuf.com/articles']
    start_urls = gen_link()

    def parse(self, response):
        for href in response.xpath('//dl/dt/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        #mkdir
        #dir_path = '%s/%s' % (ftest.settings.IMAGES_STORE, self.name)
        if not os.path.exists('html'):
            os.makedirs('html')   
        #save the html file
        os.chdir('html')
        filename = response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)
        os.chdir('..')
        #parse the pic link
        for sel in response.xpath('//img/@src').extract():
            if(sel):
                item = replaceItem()
                item['html_name'] = filename
                item['pic_url'] = sel
                print item['pic_url']
                us = item['pic_url'].split('/')[3:]
                image_file_name = '_'.join(us)
                file_path = '%s/%s' % (dir_path, image_file_name)                
                #item['pic_url'] = sel.xpath('a/@href').extract()
                #item['pic_local'] = file_path
                yield item        
        