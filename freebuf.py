# -*- coding: utf-8 -*-
import scrapy


class FreebufSpider(scrapy.Spider):
    name = "freebuf"
    allowed_domains = ["freebuf.com"]
    start_urls = ['http://freebuf.com/']

    def parse(self, response):
        pass
