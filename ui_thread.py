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


from crawl2 import Crawl2

class RunCrawl2(QtCore.QThread):
    def __init__(self, url, taskinfo, parent):
        QtCore.QThread.__init__(self, parent)
        self.url = url
        self.taskinfo = taskinfo
        self.stoped = False
        self.parent = parent

    def stop(self):
        self.stoped = True

    def run(self):
        if not self.stoped:
            Crawl2(self.url, self.taskinfo, self.parent)
