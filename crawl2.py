from ccrawler import common
from ccrawler.ccrawler import CCrawler

import logging
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

class DummySpider:
    def __init__(self, taskinfo):
        self.start_urls = taskinfo['listurl']
        print taskinfo['listurl']
        self.workers = 100
        self.timeout = 20

    def parse(self, response):
        print response.status

    def pipeline(self, item):
        pass



from PyQt4 import QtCore
from pycollect import Task_Flag_Waiting, Task_Flag_Runing, Task_Flag_Stoped, Task_Flag_Failed

class RunCrawl(QtCore.QThread):
    def __init__(self, spider, parent):
        QtCore.QThread.__init__(self, parent)
        self.spider = spider
        self.stoped = False
        self.parent = parent

    def stop(self):
        self.stoped = True

    def run(self):
        crawl = CCrawler(self.spider)
        crawl.start()