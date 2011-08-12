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
from database import Connection

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

        self.task_id_col = self.task_state_col = self.task_nextruntime_col = 0

        # mainlist menu
        self.taskAdd    = QtGui.QAction(self.task_add_icon, u"添加", self, triggered=self.TaskDialog, shortcut="Ctrl+N")
        self.taskEdit   = QtGui.QAction(self.common_edit_icon, u"修改", self)
        self.taskDelete = QtGui.QAction(self.common_del_icon, u"删除", self)
        self.separator  = QtGui.QAction(self)
        self.separator.setSeparator(True)
        self.taskStart  = QtGui.QAction(u"立即执行", self, triggered=self.manualStart)
        self.taskStop   = QtGui.QAction(u"立即结束", self, triggered=self.manualStop)

        self.robotAdd    = QtGui.QAction(self.robot_add_icon, u"添加", self, triggered=self.RobotDialog, shortcut="Ctrl+N")
        self.robotEdit   = QtGui.QAction(self.common_edit_icon, u"修改", self)
        self.robotDelete = QtGui.QAction(self.common_del_icon, u"删除", self)

        # task list: {taskid: {item: QTreeWidgetItem, taskinfo: taskinfo list}}
        self.taskList = {}
        # task thread list: {taskid: threadObject}
        self.threadList = {}
        # crawl thread list: {taskid: crawlObject}
        self.crawlList = {}

        # menu signal
        self.ui.taskadd.triggered.connect(self.TaskDialog)
        self.ui.taskadd.setIcon(self.task_add_icon)
        self.ui.m_tasklist.triggered.connect(self.getTaskList)
        self.ui.m_tasklist.setIcon(self.common_list_icon)
        self.ui.robotadd.triggered.connect(self.RobotDialog)
        self.ui.robotadd.setIcon(self.robot_add_icon)
        self.ui.m_robotlist.triggered.connect(self.getRobotList)
        self.ui.m_robotlist.setIcon(self.common_list_icon)
        self.ui.mquit.triggered.connect(QtGui.qApp.quit)

        self.ui.database.triggered.connect(self.DatabaseDialog)

    def TaskDialog(self):
        from ui import TaskUI
        Dialog = TaskUI(u'添加任务', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            self.getTaskList()

    def RobotDialog(self):
        from ui import RobotUI
        Dialog = RobotUI(u'添加采集器', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            self.getRobotList()

    def DatabaseDialog(self, flag=False):
        from ui import DatabaseUI
        Dialog = DatabaseUI(u'数据库配置', flag, self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            ini.set("database", "dbhost", _G['dbhost'])
            ini.set("database", "dbname", _G['dbname'])
            ini.set("database", "dbuser", _G['dbuser'])
            ini.set("database", "dbpw", _G['dbpw'])
            self.ui.statusbar.clearMessage()
            self.getTaskList()

    def iniDatabaseConn(self):
        _G['dbhost']    = ini.get("database","dbhost")
        _G['dbhost']    = (_G['dbhost']==None and [''] or [_G['dbhost']])[0]
        _G['dbname']    = ini.get("database","dbname")
        _G['dbname']    = (_G['dbname']==None and [''] or [_G['dbname']])[0]
        _G['dbuser']    = ini.get("database","dbuser")
        _G['dbuser']    = (_G['dbuser']==None and [''] or [_G['dbuser']])[0]
        _G['dbpw']      = ini.get("database","dbpw")
        _G['dbpw']      = (_G['dbpw']==None and [''] or [_G['dbpw']])[0]

        if _G['dbhost'] and _G['dbname'] and _G['dbuser'] and _G['dbpw'] is not None:
            self.getConnection()

        if _G['conn']==None:
            _G['DB'] = _G['conn'] = None
            self.ui.statusbar.showMessage(u'* 数据库链接错误.')
            self.DatabaseDialog()
        else:
            Mainapp.getTaskList()

    def getConnection(self):
        if _G['conn']==None:
            conn = Connection(host=_G['dbhost'],database=_G['dbname'],user=_G['dbuser'],password=_G['dbpw'])
            if conn and conn._db is not None:
                _G['DB'] = conn
                _G['conn'] = conn._db
        return _G

    def setHeaderMainList(self, header):
        self.ui.mainlist.header().setDefaultAlignment(QtCore.Qt.AlignHCenter)
        self.ui.mainlist.setColumnCount(len(header))
        self.ui.mainlist.setHeaderLabels(header)
        self.ui.mainlist.resizeColumnToContents(0)
        self.ui.mainlist.clear()

    def getTaskList(self):
        self.updateMainListFlag(True, False)
        self.setTaskMenu()

        if _G['conn']==None:
            return

        itemList = []
        self.setHeaderMainList([u'任务名称', u'采集器', u'循环', u'执行时间', u'下次执行时间', u'状态'])
        self.task_state_col = self.ui.mainlist.columnCount()-1
        self.task_nextruntime_col = self.task_state_col-1

        taskList = _G['DB'].query("SELECT t.taskid,t.robotid,t.taskname,t.loop,t.loopperiod,t.runtime,t.nextruntime, r.* FROM `pre_robots_task` t LEFT JOIN `pre_robots` r ON t.robotid = r.robotid ORDER BY t.taskid")
        for i in taskList:
            taskid  = i['taskid']
            isloop  = (i['loop']==1 and [self.yesstr] or [self.nostr])[0]
            runtime = Func.fromTimestamp(i['runtime'])
            nextruntime = (i['nextruntime'] and [Func.fromTimestamp(i['nextruntime'])] or ['-'])[0]

            taskItem = QtGui.QTreeWidgetItem([i['taskname'], i['name'], isloop, runtime, nextruntime])
            taskItem.setIcon(self.task_state_col, QtGui.QIcon(self.task_state_wait))
            taskItem.setIcon(self.task_id_col, self.task_icon)
            taskItem.setData(self.task_id_col, QtCore.Qt.UserRole, QtCore.QVariant(taskid))
            taskItem.setData(self.task_state_col, QtCore.Qt.UserRole, QtCore.QVariant(Task_Flag_Waiting))
            taskItem.setTextAlignment(2, QtCore.Qt.AlignHCenter)
            self.ui.mainlist.addTopLevelItem(taskItem)

            # start task thread
            self.taskList[taskid] = {'item': taskItem, 'taskinfo': i}
            self.runThread(taskid)

    def setTaskMenu(self):
        '''taskitem menu'''
        if not self.task_list_menu:
            self.ui.mainlist.addAction(self.taskAdd)
            self.ui.mainlist.addAction(self.taskEdit)
            self.ui.mainlist.addAction(self.taskDelete)
            self.ui.mainlist.addAction(self.separator)
            self.ui.mainlist.addAction(self.taskStart)
            self.ui.mainlist.addAction(self.taskStop)
            self.task_menu = True

        self.ui.mainlist.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def getCurrentTask(self):
        item = self.ui.mainlist.currentItem()
        return item, Func._variantConv(item.data(self.task_id_col, QtCore.Qt.UserRole), 'int')

    def manualStart(self):
        '''executed task Immediately'''
        item, taskid = self.getCurrentTask()
        self.updateTaskState(Task_Flag_Runing, taskid)
        if not self.threadList.has_key(taskid):
            self.runThread(taskid)

    def manualStop(self):
        '''stopped task Immediately'''
        item, taskid = self.getCurrentTask()
        self.stopCrawl(taskid, Task_Flag_Failed)

    def getRobotList(self):
        self.updateMainListFlag(False, True)
        self.setRobotMenu()

        if _G['conn']==None:
            return

        self.setHeaderMainList([u'采集器名称', u'匹配模式', u'延迟', u'线程', u'倒序模式', u'列表模式', u'下载模式'])
        robotList = _G['DB'].query("SELECT * FROM `pre_robots` ORDER BY robotid")
        for i in robotList:
            i['speed']          = str(i['speed'])
            i['threads']        = str(i['threads'])
            i['reverseorder']   = (i['reverseorder'] and [self.yesstr] or [self.nostr])[0]
            i['linkmode']       = (i['linkmode'] and [self.yesstr] or [self.nostr])[0]
            i['downloadmode']   = (i['downloadmode'] and [self.yesstr] or [self.nostr])[0]
            robotItem = QtGui.QTreeWidgetItem([i['name'], i['rulemode'], i['speed'], i['threads'], i['reverseorder'], i['linkmode'], i['downloadmode']])
            self.ui.mainlist.addTopLevelItem(robotItem)

    def setRobotMenu(self):
        '''robotitem menu'''
        if not self.task_robot_menu:
            self.ui.mainlist.addAction(self.robotAdd)
            self.ui.mainlist.addAction(self.robotEdit)
            self.ui.mainlist.addAction(self.robotDelete)
            self.task_bobot_menu = True

        self.ui.mainlist.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def updateMainListFlag(self, task=True, robot=False):
        self.task_list = task
        self.task_robot = robot

        self.taskAdd.setVisible(task)
        self.taskEdit.setVisible(task)
        self.taskDelete.setVisible(task)
        self.separator.setVisible(task)
        self.taskStart.setVisible(task)
        self.taskStop.setVisible(task)

        self.robotAdd.setVisible(robot)
        self.robotEdit.setVisible(robot)
        self.robotDelete.setVisible(robot)

    def updateTaskState(self, state, taskid):
        '''change task state'''
        if not self.task_list:
            return
        taskList = self.taskList[taskid]
        isloop = taskList['taskinfo']['loop']
        taskItem = taskList['item']
        curState = Func._variantConv(taskItem.data(self.task_state_col, QtCore.Qt.UserRole), 'int')
        if curState==state:
            return
        #taskItem.setIcon(self.task_state_col, QtGui.QIcon('icons/loading.gif'))
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
        _G['DB'].execute("UPDATE `pre_robots_task` SET `nextruntime` = '%d' WHERE `pre_robots_task`.`taskid` = '%d'" % (timestamp, taskid))
        self.taskList[taskid]['item'].setText(self.task_nextruntime_col, Func.fromTimestamp(timestamp))

    def runThread(self, taskid):
        '''create threads if it's not exist'''
        if self.threadList.has_key(taskid):
            return
        from run_task import RunTask
        t = RunTask(self.taskList[taskid]['taskinfo'], self)
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

        taskinfo = self.taskList[taskid]['taskinfo'].copy()
        task_listurl    = taskinfo['listurl']
        task_pagestart  = taskinfo['listpagestart']
        task_pageend    = taskinfo['listpageend']
        task_wildcardlen= taskinfo['wildcardlen']
        task_stockdata  = taskinfo['stockdata']
        task_listrule   = taskinfo['subjecturlrule']
        task_titlerule  = taskinfo['subjectrule']
        task_linkrule   = taskinfo['subjecturllinkrule']
        task_contentrule= taskinfo['messagerule']

        taskinfo['listurl'] = Func.getStartUrls(task_listurl, task_pagestart, task_pageend, task_wildcardlen, task_stockdata)

        spider = DummySpider(taskinfo, self)
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
    _G = {'DB': None, 'conn': None, 'dbhost':'', 'dbname':'', 'dbuser':'', 'dbpw':''}
    ini = IniFile("config.cfg", True)

    app = QtGui.QApplication(sys.argv)

    # show main window
    Mainapp = MainUI()
    Mainapp.show()

    # init database connection
    Mainapp.iniDatabaseConn()

    sys.exit(app.exec_())
