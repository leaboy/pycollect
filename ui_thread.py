#!/usr/bin/python
#-*-coding:utf-8-*-

# thread classes.
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

import os, time
from PyQt4 import QtCore
from pycollect import Task_Flag_Waiting, Task_Flag_Runing, Task_Flag_Stoped, Task_Flag_Failed

class RunTask(QtCore.QThread):
    def __init__(self, taskinfo, parent):
        QtCore.QThread.__init__(self, parent)
        self.taskinfo = taskinfo
        self.stoped = False
        self.parent = parent

    def stop(self):
        self.stoped = True

    def run(self):
        taskid      = self.taskinfo['taskid']
        robotid     = self.taskinfo['robotid']
        isloop      = self.taskinfo['loop']
        loopperiod  = self.taskinfo['loopperiod']
        runtime     = self.taskinfo['runtime']
        nextruntime = self.taskinfo['nextruntime']

        while True:
            if self.stoped:
                return

            state = Task_Flag_Waiting
            triggertime = (nextruntime > 0 and [nextruntime] or [runtime])[0]
            currenttime = time.mktime(time.localtime())

            if triggertime == currenttime:
                state = Task_Flag_Runing
            elif triggertime < currenttime:
                if isloop == 1:
                    nextruntime = triggertime + loopperiod
                    if nextruntime > currenttime:
                        self.emit(QtCore.SIGNAL("Updated"), nextruntime, taskid)
                else:
                    state = Task_Flag_Stoped

            # is running
            spider_name, spider_file = self.parent.getCrawlSpider(taskid)
            locker_file = '%s.lock' % spider_file

            if os.path.isfile(locker_file):
                state = Task_Flag_Runing

            self.emit(QtCore.SIGNAL("Activated"), state, taskid)
            time.sleep(1)


from scrapy.conf import settings
#from scrapy import signals
from scrapy.crawler import CrawlerProcess
#from scrapy.xlib.pydispatch import dispatcher

#def connect(signal):
#    """Handy signal hook decorator"""
#    def wrapper(func):
#        dispatcher.connect(func, signal)
#        return func
#    return wrapper

class RunCrawl(QtCore.QThread):
    def __init__(self, taskinfo, crawler, spider, parent):
        QtCore.QThread.__init__(self, parent)
        self.taskinfo = taskinfo
        self.stoped = False
        self.parent = parent
        self.spider = spider
        self.crawler = crawler

    def stop(self):
        self.crawler.stop()

    def run(self):
        #while True:
            if self.spider==None:
                self.stop()
#           @connect(signals.item_passed)
#           def catch_item(sender, item, **kwargs):
#               print "Got:", item

            #dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
            #dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

            print '.'
            #self.crawler.queue.append_spider(self.spider)

            self.crawler.start()
            #self.stop()


from scrapy import log, signals
from scrapy.utils.console import start_python_console
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import threads

class BlockingCrawlerFromThread(object):

    def __init__(self, crawler):
        self.crawler = crawler
        dispatcher.connect(self._spider_closed, signals.spider_closed)
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _crawl(self, spider_name):
        spider = self.crawler.spiders.create(spider_name)
        if spider:
            self.items = []
            self.crawler.queue.append_spider(spider)
            self.deferred = defer.Deferred()
            return self.deferred

    def _item_passed(self, item):
        self.items.append(item)

    def _spider_closed(self, spider):
        self.deferred.callback(self.items)

    def crawl(self, spider_name):
        return threads.blockingCallFromThread(reactor, self._crawl, spider_name)

    def start(self):
        self.crawler.start()
