#!/usr/bin/python
#-*-coding:utf-8-*-

# The Main class for crawl.
#
# Created: 2011-Aug-01 11:28:20
#      By: leaboy.w
#   Email: leaboy.w@gmail.com
#     Lib: Scrapy 0.12.0
#
# GNU Free Documentation License 1.3

import sys, os

from scrapy.conf import settings
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from scrapy.xlib.pydispatch import dispatcher

class MyItems(Item):
    """necessary Item"""
    title = Field()
    link = Field()
    content = Field()


from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.contrib.loader import XPathItemLoader

class MySpider(BaseSpider):
    """spider"""
    name = 'spider_name'
    start_urls = ['http://stackoverflow.com/']
    list_xpath = '//div[@id="content"]//div[contains(@class, "question-summary")]'

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        for qxs in hxs.select(self.list_xpath):
            loader = XPathItemLoader(MyItems(), selector=qxs)
            loader.add_xpath('title', './/h3/a/text()')
            loader.add_xpath('link', './/h3/a/@title')
            loader.add_xpath('content', './/a[@rel="tag"]/text()')

            yield loader.load_item()


class MyCrawl:
    def item_passed(self, item):
        print "Got:", item

    def stop(self):
        pass

    def run(self):
        """Install item signal and run scrapy"""
        dispatcher.connect(self.item_passed, signals.item_passed)

        settings.overrides['LOG_ENABLED'] = False

        crawler = CrawlerProcess(settings)
        crawler.install()
        crawler.configure()

        spider = MySpider()
        crawler.queue.append_spider(spider)

        print "STARTING ENGINE"
        crawler.start()
        print "ENGINE STOPPED"