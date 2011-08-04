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




from scrapy import log, signals, project
from scrapy.xlib.pydispatch import dispatcher
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess

def connect(signal):
    """Handy signal hook decorator"""
    def wrapper(func):
        dispatcher.connect(func, signal)
        return func
    return wrapper

class CrawlerScript(QtCore.QThread):

    def __init__(self, taskid, spider, parent):
        QtCore.QThread.__init__(self, parent)

        self.parent = parent
        self.taskid = taskid
        self.spider = spider

        settings.overrides['LOG_ENABLED'] = False
        self.crawler = CrawlerProcess(settings)
        if not hasattr(project, 'crawler'):
            self.crawler.install()
        self.crawler.configure()

        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        print "opened spider %s" % spider.name

    def spider_closed(self, spider):
        print "closed spider %s" % spider.name
        self.stop()
        self.parent.stopCrawl(self.taskid)

    def stop(self):
        self.crawler.stop()

    def run(self):
        if not self.spider:
            self.stop()
        @connect(signals.item_passed)
        def catch_item(sender, item, **kwargs):
            print "Got:", item
        self.crawler.queue.append_spider(self.spider)
        try:
            self.crawler.start()
        except:
            self.emit(QtCore.SIGNAL("Activated"), Task_Flag_Failed, taskid)
        #self.crawler.stop()
