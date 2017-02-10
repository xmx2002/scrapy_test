# -*- coding: utf-8 -*-
import scrapy
from ftest.items import *
import os
import ftest.settings
import psycopg2

dir_path = '%s/%s' % (ftest.settings.IMAGES_STORE,"freebuf")

def gen_link():
    url=['http://www.freebuf.com/articles']
    #for i in range(2,225):
        #url.append('http://www.freebuf.com/articles/page/'+str(i))
    return url

def inser_db_url(url):
    #sql_desc="INSERT INTO postgresql_1(fullname, username, organization, mail, joined,followers,starred,following,popular_repos,popular_repos_download,popular_repos_star,popular_repos_info,home_page)values(item['fullname'], item['username'], item['organization'], item['mail'],item['joined'],item['followers'],item['starred'],item['following'],item['popular_repos'],item['popular_repos_download'],item['popular_repos_star'],item['popular_repos_info'], item['home_page'])"
    conn = psycopg2.connect(database="freebuf", user="postgres", password="123456", host="127.0.0.1", port="5432")
    try:
        cur=conn.cursor()
        #ret=cur.execute("CREATE TABLE URL (ID INT PRIMARY KEY NOT NULL,URL TEXT NOT NULL);")
        #cur.execute("INSERT INTO URL (ID,URL) VALUES (%d,%s)",(id,url));
        #cur.execute("INSERT INTO URL (ID,URL) VALUES (%s,%s)", (str(db_id),url,));
        cur.execute("INSERT INTO url (URL) VALUES (%s)", (url,));
        conn.commit()

    except Exception,e:
        print 'insert record into url failed'
        print e
    finally:
        if cur:
            cur.close()
    conn.close()
    return

def select_db_url(url):
    #sql_desc="INSERT INTO postgresql_1(fullname, username, organization, mail, joined,followers,starred,following,popular_repos,popular_repos_download,popular_repos_star,popular_repos_info,home_page)values(item['fullname'], item['username'], item['organization'], item['mail'],item['joined'],item['followers'],item['starred'],item['following'],item['popular_repos'],item['popular_repos_download'],item['popular_repos_star'],item['popular_repos_info'], item['home_page'])"
    conn = psycopg2.connect(database="freebuf", user="postgres", password="123456", host="127.0.0.1", port="5432")
    try:
        cur=conn.cursor()
        #cur.execute("SELECT URL from URL")
        cur.execute("SELECT URL from url where URL= %s",(url,))
        rows = cur.fetchall()
        if rows:    
            retval = True
        else:
            retval = False
        return retval
    except Exception,e:
        print 'no record in url'
        print e

    finally:
        if cur:
            cur.close()
    conn.close()
    return False
def inser_db_pic(pic_url,html_name,local_pic="not set",replaced=0):
    #sql_desc="INSERT INTO postgresql_1(fullname, username, organization, mail, joined,followers,starred,following,popular_repos,popular_repos_download,popular_repos_star,popular_repos_info,home_page)values(item['fullname'], item['username'], item['organization'], item['mail'],item['joined'],item['followers'],item['starred'],item['following'],item['popular_repos'],item['popular_repos_download'],item['popular_repos_star'],item['popular_repos_info'], item['home_page'])"
    conn = psycopg2.connect(database="freebuf_pic", user="postgres", password="123456", host="127.0.0.1", port="5432")
    try:
        cur=conn.cursor()
        cur.execute("INSERT INTO pic_replace (PIC_URL,HTML_NAME,LOCAL_PIC,REPLACE) VALUES (%s,%s,%s,%s)", (pic_url,html_name,local_pic,str(replaced),));
        conn.commit()

    except Exception,e:
        print 'insert record into pic failed'
        print e
      
    finally:
        if cur:
            cur.close()
    conn.close()
    return

def select_db_pic(url):
    #sql_desc="INSERT INTO postgresql_1(fullname, username, organization, mail, joined,followers,starred,following,popular_repos,popular_repos_download,popular_repos_star,popular_repos_info,home_page)values(item['fullname'], item['username'], item['organization'], item['mail'],item['joined'],item['followers'],item['starred'],item['following'],item['popular_repos'],item['popular_repos_download'],item['popular_repos_star'],item['popular_repos_info'], item['home_page'])"
    conn = psycopg2.connect(database="freebuf", user="postgres", password="123456", host="127.0.0.1", port="5432")
    try:
        cur=conn.cursor()
        #cur.execute("SELECT URL from URL")
        cur.execute("SELECT PIC_URL from PIC_URL where PIC_URL= %s",(url,))
        rows = cur.fetchall()
        if rows:
            retval = True
        else:
            retval = False
        return retval
    except Exception,e:
        print 'no record in pic'
        print e

    finally:
        if cur:
            cur.close()
    conn.close()
    return False
class FreebufSpider(scrapy.Spider):
    name = "freebuf"
    #allowed_domains = ["freebuf.com"]
    #start_urls = ['http://www.freebuf.com/articles']
    start_urls = gen_link()
    def parse(self, response):
        
        for href in response.xpath('//dl/dt/a/@href'):
            url = response.urljoin(href.extract())
            
            if not select_db_url(url):
                #print 'insert '+ url
                inser_db_url(url)
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
                #print item['pic_url']
                us = item['pic_url'].split('/')[3:]
                image_file_name = '_'.join(us)
                file_path = '%s/%s' % (dir_path, image_file_name)
                inser_db_pic(sel,filename,local_pic=file_path,replaced=0)
                #item['pic_url'] = sel.xpath('a/@href').extract()
                #item['pic_local'] = file_path
                yield item        
        