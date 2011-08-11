from ccrawler import common
from ccrawler.ccrawler import CCrawler
from ccrawler.selector import HtmlSelector

import logging
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

class DummySpider:
    def __init__(self, taskinfo):
        self.start_urls = taskinfo['listurl']
        self.workers = 100
        self.timeout = 20
        self.importSQL = taskinfo['importSQL']

    def parse(self, response):
        hxs = HtmlSelector(response.body)

        itemlist = hxs.select('//td[@class="td10"]')

        for item in itemlist:
            title = item.select('a/text()').extract()[0]
            link = item.select('a/@href').extract()[0]
            yield (title, link)

    def process_item(self, item):
        for i in item:
            print i



from PyQt4 import QtCore
from pycollect import Task_Flag_Waiting, Task_Flag_Runing, Task_Flag_Stoped, Task_Flag_Failed

class RunCrawl(QtCore.QThread):
    def __init__(self, taskid, spider, parent):
        QtCore.QThread.__init__(self, parent)
        self.taskid = taskid
        self.spider = spider
        self.parent = parent
        self.crawl = None

    def stop(self, state=Task_Flag_Stoped):
        if self.crawl is not None and self.crawl.creq.qsize()>0:
            self.crawl.stop()

    def run(self):
        self.crawl = CCrawler(self.spider)
        self.crawl.start()
        self.emit(QtCore.SIGNAL("Updated"), self.taskid, Task_Flag_Stoped)