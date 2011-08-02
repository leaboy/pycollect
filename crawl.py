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

from scrapy.conf import settings
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher

def connect(signal):
    """Handy signal hook decorator"""
    def wrapper(func):
        dispatcher.connect(func, signal)
        return func
    return wrapper

class MyCrawl(object):
    def __init__(self, spider):
        self.spider = spider
        self.crawler = None

    def spider_opened(self, spider):
        print "opened spider %s" % spider.name

    def spider_closed(self, spider):
        print "closed spider %s" % spider.name

    def item_passed(self, item, **kwargs):
        print "Got:", item

    def stop(self):
        self.crawler.stop()

    def run(self):
        """Install item signal and run scrapy"""
        if self.spider==None:
            self.stop()
        @connect(signals.item_passed)
        def catch_item(sender, item, **kwargs):
            print "Got:", item

        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

        settings.overrides['LOG_ENABLED'] = False

        self.crawler = CrawlerProcess(settings)
        self.crawler.install()
        self.crawler.configure()

        self.crawler.queue.append_spider(self.spider)

        self.crawler.start()
        self.stop()
