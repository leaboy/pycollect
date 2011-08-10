# -*- coding: utf-8 -*-
'''
Example of Usage
'''

import common
from ccrawler import CCrawler

import logging
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

class DummySpider:
    start_urls = ['http://www.soso.com', 'http://www.google.tk', 'http://www.baidu.com', 'http://www.google.com', 'http://wiki.nocn.net']
    workers = 100
    timeout = 8

    def parse(self, response):
        url = response.url;
        title = response.body;
        return [url]

    def process_item(self, item):
        for r in results:
            print "save : %s" % r


class a:
    pass


spider = DummySpider()
crawler = CCrawler(spider)
crawler.start()
crawler.stop()


'''
spider2 = a()
crawler2 = CCrawler('')
crawler2.start()
'''

