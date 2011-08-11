# -*- coding: utf-8 -*-
'''
Example of Usage
'''

import common
from ccrawler import CCrawler
from selector import HtmlSelector

import logging
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

class DummySpider:
    start_urls = ['http://disclosure.szse.cn/m/drgg000023.htm', 'http://disclosure.szse.cn/m/drgg000024.htm']
    #start_urls = ['http://www.baidu.com', 'http://www.google.com', 'http://www.google.hk']
    workers = 100
    timeout = 8

    def parse(self, response):
        hxs = HtmlSelector(response.body)
        itemlist = hxs.select('//td[@class="td10"]')
        #print len(response.body)

        for item in itemlist:
            #print item._root.xpath('a/text()')
            title = item.select('a/text()').extract()[0]
            link = item.select('a/@href').extract()[0]
            yield (title, link)

    def process_item(self, item):
        for i in item:
            print i

class a:
    pass


spider = DummySpider()
crawler = CCrawler(spider)
crawler.start()

