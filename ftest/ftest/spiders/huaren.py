# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
from ftest.items import *
import os
import ftest.settings
import re
from operator import itemgetter 

regex=re.compile("(?x) (?: [\w-]+ | [\x80-\xff]{3} )") 
#regex=re.compile("(?x) ( [\w-]+ )") 
dicts={} 

def divide(c, regex): 
#the regex below is only valid for utf8 coding 
    return regex.findall(c) 


def update_dict(li): 
    for i in li: 
        if dicts.has_key(i): 
            dicts[i]+=1 
        else: 
            dicts[i]=1 
    
def gen_link():
    url=[]
    for i in range(1,2):
        url.append('http://forums.huaren.us/showforum.aspx?forumid=398&page='+str(i))
    return url
class HuarenSpider(scrapy.Spider):
    name = "huaren"
    #allowed_domains = ["http://forums.huaren.us/"]
    start_urls = gen_link()

    def parse(self, response):
        for href in response.xpath('//tbody/tr/th/a/@href'):
            url = response.urljoin(href.extract())
            #print 'xxxxxx' + url
            yield scrapy.Request(url, callback=self.parse_dir_contents)
    
    def parse_dir_contents(self, response):
        #print '123456'
        
        #for sel in response.xpath('//td[@class="postcontent"]/div/div/p').extract():
        for sel in response.xpath('//div[@class="postmessage defaultpost"]/div[@class="t_msgfont"]/text()').extract():
            if(sel): 
                #print 'ttt '+ sel
                words=divide(sel, regex) 
                update_dict( words) 
                print words
                
        #sort dictionary by value 
        #dict is now a list. 
        #dicts1=sorted(dicts.items(), key=itemgetter(1), reverse=True) 
        
        #output to standard-output 
        #for s in dicts1: 
            #item = HuarenItem()
            #item['word'] = s[0]
            #item['frequency'] = s[1]
            #print s[0], s[1] 
            #yield item 
            
    def closed(self,reason):
        dicts1=sorted(dicts.items(), key=itemgetter(1), reverse=True)
        #print 'xxxxxxxxxxxxxxxx'
        with open('huarentest.txt', 'wb') as f:
            f.write('\n'.join('%s %s' % x for x in dicts1))  
        #for word in dicts1:
            #item = HuarenItem()
            #item['word'] = word[0]
            #item['frequency'] = word[1]
            #print word[0], word[1] 
            ##yield item             
    
                 
