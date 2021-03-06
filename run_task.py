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
    def __init__(self, taskid, parent):
        QtCore.QThread.__init__(self, parent)
        self.taskid = taskid
        self.stoped = False
        self.parent = parent

    def stop(self):
        self.stoped = True

    def run(self):
        taskinfo    = self.parent.taskList[self.taskid]['taskinfo']
        taskid      = taskinfo.taskid
        robotid     = taskinfo.robotid
        isloop      = taskinfo.loop
        loopperiod  = taskinfo.loopperiod
        runtime     = taskinfo.runtime
        nextruntime = taskinfo.nextruntime

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
            if self.parent.crawlList.has_key(taskid):
                state = Task_Flag_Runing

            self.emit(QtCore.SIGNAL("Activated"), state, taskid)
            time.sleep(1)
