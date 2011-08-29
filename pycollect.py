#!/usr/bin/python
#-*-coding:utf-8-*-

# Main App.
#
# $Author$
# $Id$
#
# Package: ui files, simplejson
#
# GNU Free Documentation License 1.3

import os, sys, time
import hashlib
import simplejson

from iniFile import IniFile
from common import Func
from models import Robot, Task, Session, metadata, sys_engine


from PyQt4 import QtCore, QtGui
from ui_main import Ui_MainWindow


# task flag
Task_Flag_Waiting   = 0
Task_Flag_Runing    = 1
Task_Flag_Stoped    = 2
Task_Flag_Failed    = 3


class MainUI(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.yesstr = u'√'
        self.nostr  = u'-'
        self.task_list          = False
        self.task_list_menu     = False
        self.task_robot         = False
        self.task_robot_menu    = False
        self.task_state_wait    = 'icons/task_state_waiting.png'
        self.task_state_run     = 'icons/task_state_runing.png'
        self.task_state_stop    = 'icons/task_state_stoped.png'
        self.task_state_failed  = 'icons/task_state_failed.png'

        self.task_icon      = QtGui.QIcon('icons/task.png')
        self.task_add_icon  = QtGui.QIcon('icons/task_add.png')

        self.robot_icon      = QtGui.QIcon('icons/robot.png')
        self.robot_add_icon      = QtGui.QIcon('icons/robot_add.png')

        self.common_list_icon    = QtGui.QIcon('icons/common_list.png')
        self.common_edit_icon   = QtGui.QIcon('icons/common_edit.png')
        self.common_del_icon    = QtGui.QIcon('icons/common_delete.png')

        self.id_col = self.task_state_col = self.task_nextruntime_col = 0

        # mainlist menu
        self.setMainListMenu()

        # task list: {taskid: {item: QTreeWidgetItem, taskinfo: taskinfo list}}
        self.taskList = {}
        # task thread list: {taskid: threadObject}
        self.threadList = {}
        # crawl thread list: {taskid: crawlObject}
        self.crawlList = {}

        # menu signal
        self.ui.taskadd.triggered.connect(self.TaskDialog_add)
        self.ui.taskadd.setIcon(self.task_add_icon)
        self.ui.m_tasklist.triggered.connect(self.getTaskList)
        self.ui.m_tasklist.setIcon(self.common_list_icon)
        self.ui.robotadd.triggered.connect(self.RobotDialog_add)
        self.ui.robotadd.setIcon(self.robot_add_icon)
        self.ui.m_robotlist.triggered.connect(self.getRobotList)
        self.ui.m_robotlist.setIcon(self.common_list_icon)
        self.ui.mquit.triggered.connect(QtGui.qApp.quit)

    def TaskDialog_add(self):
        from ui import TaskUI
        Dialog = TaskUI(u'添加任务', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            self.getTaskList()

    def TaskDialog_edit(self):
        item, taskid = self.getCurrentItem()
        if taskid>0:
            from ui import TaskUI
            Dialog = TaskUI(u'修改任务', self, taskid)
            if Dialog.exec_() == QtGui.QDialog.Accepted:
                self.stopThread(taskid)
                self.getTaskList()
        else:
            self.getTaskList()

    def TaskDialog_delete(self):
        item, taskid = self.getCurrentItem()
        self.stopThread(taskid)
        session = Session()
        task = session.query(Task).filter(Task.taskid==taskid).first()
        session.delete(task)
        session.commit()
        self.getTaskList()

    def RobotDialog_add(self):
        from ui import RobotUI
        Dialog = RobotUI(u'添加采集器', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            self.getRobotList()

    def RobotDialog_edit(self):
        item, robotid = self.getCurrentItem()
        if robotid>0:
            from ui import RobotUI
            Dialog = RobotUI(u'修改采集器', self, robotid)
            if Dialog.exec_() == QtGui.QDialog.Accepted:
                self.getRobotList()
        else:
            self.getRobotList()

    def RobotDialog_delete(self):
        item, robotid = self.getCurrentItem()
        if robotid>0:
            session = Session()
            robot = session.query(Robot).filter(Robot.robotid==robotid).first()
            session.delete(robot)
            session.commit()
        self.getRobotList()

    def setMainListMenu(self):
        # task
        self.taskMenu = QtGui.QMenu()
        self.taskAdd    = QtGui.QAction(self.task_add_icon, u"添加", self, triggered=self.TaskDialog_add, shortcut="Ctrl+N")
        self.taskEdit   = QtGui.QAction(self.common_edit_icon, u"修改", self, triggered=self.TaskDialog_edit)
        self.taskDelete = QtGui.QAction(self.common_del_icon, u"删除", self, triggered=self.TaskDialog_delete)
        self.separator  = QtGui.QAction(self)
        self.separator.setSeparator(True)
        self.taskStart  = QtGui.QAction(u"立即执行", self, triggered=self.manualStart)
        self.taskStop   = QtGui.QAction(u"立即结束", self, triggered=self.manualStop)

        self.taskMenu.addAction(self.taskAdd)
        self.taskMenu.addAction(self.taskEdit)
        self.taskMenu.addAction(self.taskDelete)
        self.taskMenu.addAction(self.separator)
        self.taskMenu.addAction(self.taskStart)
        self.taskMenu.addAction(self.taskStop)

        # robot
        self.robotMenu = QtGui.QMenu()
        self.robotAdd    = QtGui.QAction(self.robot_add_icon, u"添加", self, triggered=self.RobotDialog_add, shortcut="Ctrl+N")
        self.robotEdit   = QtGui.QAction(self.common_edit_icon, u"修改", self, triggered=self.RobotDialog_edit)
        self.robotDelete = QtGui.QAction(self.common_del_icon, u"删除", self, triggered=self.RobotDialog_delete)

        self.robotMenu.addAction(self.robotAdd)
        self.robotMenu.addAction(self.robotEdit)
        self.robotMenu.addAction(self.robotDelete)

        self.ui.mainlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.mainlist.customContextMenuRequested.connect(self.updateMainListMenu)

    def setHeaderMainList(self, header):
        self.ui.mainlist.header().setDefaultAlignment(QtCore.Qt.AlignHCenter)
        self.ui.mainlist.setColumnCount(len(header))
        self.ui.mainlist.setHeaderLabels(header)
        self.ui.mainlist.resizeColumnToContents(0)
        self.ui.mainlist.clear()

    def getTaskList(self):
        self.updateMainListFlag(True, False)
        itemList = []
        self.setHeaderMainList([u'任务名称', u'采集器', u'循环', u'执行时间', u'下次执行时间', u'状态'])
        self.task_state_col = self.ui.mainlist.columnCount()-1
        self.task_nextruntime_col = self.task_state_col-1
        self.ui.mainlist.setColumnWidth(0, 120)
        self.ui.mainlist.setColumnWidth(1, 120)
        self.ui.mainlist.setColumnWidth(2, 50)
        self.ui.mainlist.setColumnWidth(3, 140)
        self.ui.mainlist.setColumnWidth(4, 140)
        session = Session()
        taskList = session.query(Task).outerjoin(Robot, Task.robotid==Robot.robotid).all()
        for i in taskList:
            taskid  = i.taskid
            isloop  = (i.loop==1 and [self.yesstr] or [self.nostr])[0]
            runtime = Func.fromTimestamp(i.runtime)
            nextruntime = (i.nextruntime and [Func.fromTimestamp(i.nextruntime)] or ['-'])[0]
            robotname = (hasattr(i, 'robotinfo') and [i.robotinfo.robotname] or ['-'])[0]

            taskItem = QtGui.QTreeWidgetItem([i.taskname, robotname, isloop, runtime, nextruntime])
            taskItem.setIcon(self.task_state_col, QtGui.QIcon(self.task_state_wait))
            taskItem.setIcon(self.id_col, self.task_icon)
            taskItem.setData(self.id_col, QtCore.Qt.UserRole, QtCore.QVariant(taskid))
            taskItem.setData(self.task_state_col, QtCore.Qt.UserRole, QtCore.QVariant(Task_Flag_Waiting))
            taskItem.setTextAlignment(1, QtCore.Qt.AlignHCenter)
            taskItem.setTextAlignment(2, QtCore.Qt.AlignHCenter)
            taskItem.setTextAlignment(3, QtCore.Qt.AlignHCenter)
            taskItem.setTextAlignment(4, QtCore.Qt.AlignHCenter)
            self.ui.mainlist.addTopLevelItem(taskItem)

            # start task thread
            self.taskList[taskid] = {'item': taskItem, 'taskinfo': i}
            self.runThread(taskid)

    def getCurrentItem(self):
        item = self.ui.mainlist.currentItem()
        return item, Func._variantConv(item.data(self.id_col, QtCore.Qt.UserRole), 'int')

    def manualStart(self):
        '''executed task Immediately'''
        item, taskid = self.getCurrentItem()
        self.updateTaskState(Task_Flag_Runing, taskid)
        if not self.threadList.has_key(taskid):
            self.runThread(taskid)

    def manualStop(self):
        '''stopped task Immediately'''
        item, taskid = self.getCurrentItem()
        self.stopCrawl(taskid, Task_Flag_Failed)

    def getRobotList(self):
        self.updateMainListFlag(False, True)
        self.setHeaderMainList([u'采集器名称', u'匹配模式', u'超时', u'线程', u'倒序模式', u'列表模式', u'下载模式'])
        self.ui.mainlist.setColumnWidth(0, 150)
        self.ui.mainlist.setColumnWidth(1, 80)
        self.ui.mainlist.setColumnWidth(2, 60)
        self.ui.mainlist.setColumnWidth(3, 60)
        self.ui.mainlist.setColumnWidth(4, 80)
        self.ui.mainlist.setColumnWidth(5, 80)
        self.ui.mainlist.setColumnWidth(6, 80)
        session = Session()
        robotList = session.query(Robot).all()
        for i in robotList:
            timeout         = str(i.timeout)
            threads         = str(i.threads)
            reversemode     = (i.reversemode and [self.yesstr] or [self.nostr])[0]
            linkmode        = (i.linkmode and [self.yesstr] or [self.nostr])[0]
            downloadmode    = (i.downloadmode and [self.yesstr] or [self.nostr])[0]
            robotItem = QtGui.QTreeWidgetItem([i.robotname, i.rulemode, timeout, threads, reversemode, linkmode, downloadmode])
            robotItem.setIcon(self.id_col, self.robot_icon)
            robotItem.setData(self.id_col, QtCore.Qt.UserRole, QtCore.QVariant(i.robotid))
            robotItem.setTextAlignment(1, QtCore.Qt.AlignHCenter)
            robotItem.setTextAlignment(2, QtCore.Qt.AlignHCenter)
            robotItem.setTextAlignment(3, QtCore.Qt.AlignHCenter)
            robotItem.setTextAlignment(4, QtCore.Qt.AlignHCenter)
            robotItem.setTextAlignment(5, QtCore.Qt.AlignHCenter)
            robotItem.setTextAlignment(6, QtCore.Qt.AlignHCenter)
            self.ui.mainlist.addTopLevelItem(robotItem)

    def updateMainListFlag(self, task=True, robot=False):
        self.task_list = task
        self.task_robot = robot

    def updateMainListMenu(self, point):
        '''show ContextMenu'''
        index = self.ui.mainlist.indexAt(point)
        if not index.isValid():
            self.ui.mainlist.clearSelection()
            self.taskEdit.setDisabled(True)
            self.taskDelete.setDisabled(True)
            self.taskStart.setDisabled(True)
            self.taskStop.setDisabled(True)

            self.robotEdit.setDisabled(True)
            self.robotDelete.setDisabled(True)
        else:
            item = self.ui.mainlist.itemAt(point)
            state = Func._variantConv(item.data(self.task_state_col, QtCore.Qt.UserRole), 'int')
            if state==Task_Flag_Waiting:
                self.taskEdit.setDisabled(False)
                self.taskDelete.setDisabled(False)
                self.taskStart.setDisabled(False)
                self.taskStop.setDisabled(True)
            elif state==Task_Flag_Runing:
                self.taskStart.setDisabled(True)
                self.taskStop.setDisabled(False)
            else:
                self.taskEdit.setDisabled(False)
                self.taskDelete.setDisabled(False)
                self.taskStart.setDisabled(False)

            self.robotEdit.setDisabled(False)
            self.robotDelete.setDisabled(False)

        if self.task_list:
            self.taskMenu.exec_(QtGui.QCursor.pos())
        elif self.task_robot:
            self.robotMenu.exec_(QtGui.QCursor.pos())

    def updateTaskState(self, state, taskid):
        '''change task state'''
        if not self.task_list:
            return
        taskList = self.taskList[taskid]
        isloop = taskList['taskinfo'].loop
        taskItem = taskList['item']
        curState = Func._variantConv(taskItem.data(self.task_state_col, QtCore.Qt.UserRole), 'int')
        if curState==state:
            return
        stateIcon = {Task_Flag_Waiting: self.task_state_wait, Task_Flag_Runing: self.task_state_run, Task_Flag_Stoped: self.task_state_stop, Task_Flag_Failed: self.task_state_failed}
        taskItem.setIcon(self.task_state_col, QtGui.QIcon(stateIcon[state]))
        taskItem.setData(self.task_state_col, QtCore.Qt.UserRole, QtCore.QVariant(state))

        if state==Task_Flag_Stoped and isloop==0:
            self.stopThread(taskid)
        elif state==Task_Flag_Runing:
            self.runCrawl(taskid)

    def updateNextRunTime(self, timestamp, taskid):
        '''change nextruntime item'''
        if not self.task_list:
            return
        session = Session()
        task = session.query(Task).filter(Task.taskid==taskid).first()
        task.nextruntime = timestamp
        session.commit()
        self.taskList[taskid]['item'].setText(self.task_nextruntime_col, Func.fromTimestamp(timestamp))

    def runThread(self, taskid):
        '''create threads if it's not exist'''
        if self.threadList.has_key(taskid):
            return
        from run_task import RunTask
        t = RunTask(taskid, self)
        self.threadList[taskid] = t
        self.connect(t, QtCore.SIGNAL("Updated"), self.updateNextRunTime)
        self.connect(t, QtCore.SIGNAL("Activated"), self.updateTaskState)
        t.start()

    def stopThread(self, taskid):
        '''stop threads by taskid/all'''
        if not len(self.threadList)>0 or (not self.threadList.has_key(taskid) and taskid!=-1):
            return
        if taskid == -1:
            for t in self.threadList: t.stop()
            self.threadList.clear()
        else:
            t = self.threadList[taskid]
            t.stop()

            self.taskList[taskid]['item'].setIcon(self.task_state_col, QtGui.QIcon(self.task_state_stop))
            del self.threadList[taskid]

    def runCrawl(self, taskid):
        '''run scrapy crawl'''
        if self.crawlList.has_key(taskid):
            return

        from run_crawl import DummySpider, RunCrawl

        task = self.taskList[taskid]['taskinfo']

        spider = DummySpider(task, self)
        t = RunCrawl(taskid, spider, self)
        self.crawlList[taskid] = t
        self.connect(t, QtCore.SIGNAL("Updated"), self.stopCrawl)
        t.start()

    def stopCrawl(self, taskid, state):
        if not len(self.crawlList)>0 or (not self.crawlList.has_key(taskid) and taskid!=-1):
            return
        if taskid == -1:
            self.crawlList.clear()
        else:
            self.crawlList[taskid].stop()
            del self.crawlList[taskid]
            self.updateTaskState(state, taskid)


if __name__ == "__main__":
    # init database
    metadata.create_all(sys_engine)

    app = QtGui.QApplication(sys.argv)

    Mainapp = MainUI()
    Mainapp.show()
    Mainapp.getTaskList()

    sys.exit(app.exec_())
