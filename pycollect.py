#!/usr/bin/python
#-*-coding:utf-8-*-

# The Main App for Data collector.
#
# Created: 2011-Jul-12 ‏‎11:01:24
#      By: leaboy.w
#   Email: leaboy.w@gmail.com
# Package: ui files, phpserialize
#
# GNU Free Documentation License 1.3

import re, sys, time, datetime, os
import threading
import httplib, urllib
import hashlib
import simplejson
from urlparse import urlparse,urljoin

from iniFile import *
from database import *
from phpserialize import *
from PyQt4 import QtCore, QtGui

from ui_main import Ui_MainWindow
from ui_robot import Ui_RobotDialog
from ui_task import Ui_TaskDialog
from ui_database import Ui_DatabaseDialog


class MainUI(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.yesstr = u'√'
        self.nostr  = u'-'
        self.list_with_task     = False
        self.list_with_robot    = False
        self.task_state_wait    = 'res/task_state_waiting.png'
        self.task_state_run     = 'res/task_state_runing.png'
        self.task_state_stop    = 'res/task_state_stoped.png'

        self.task_id_col = self.task_state_col = self.task_nextruntime_col = 0

        # task list: {taskid: {item: QTreeWidgetItem, taskinfo: taskinfo list}}
        self.taskList = {}
        # thread list: {taskid: threadObject}
        self.threadList = {}

        # menu signal
        self.ui.taskadd.triggered.connect(self.TaskDialog)
        self.ui.m_tasklist.triggered.connect(self.getTaskList)
        self.ui.robotadd.triggered.connect(self.RobotDialog)
        self.ui.m_robotlist.triggered.connect(self.getRobotList)
        self.ui.mquit.triggered.connect(QtGui.qApp.quit)

        self.ui.database.triggered.connect(self.DatabaseDialog)

    def TaskDialog(self):
        Dialog = TaskUI(u'添加任务', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            self.getTaskList()

    def RobotDialog(self):
        Dialog = RobotUI(u'添加采集器', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            self.getRobotList()

    def DatabaseDialog(self, flag=False):
        Dialog = DatabaseUI(u'数据库配置', flag, self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            ini.set("database", "dbhost", _G['dbhost'])
            ini.set("database", "dbname", _G['dbname'])
            ini.set("database", "dbuser", _G['dbuser'])
            ini.set("database", "dbpw", _G['dbpw'])
            self.ui.statusbar.clearMessage()

    def iniDatabaseConn(self):
        _G['dbhost']  = ini.get("database","dbhost")
        _G['dbname']  = ini.get("database","dbname")
        _G['dbuser']  = ini.get("database","dbuser")
        _G['dbpw']    = ini.get("database","dbpw")

        if _G['dbhost'] and _G['dbname'] and _G['dbuser'] and _G['dbpw'] is not None:
            conn = Connection(host=_G['dbhost'],database=_G['dbname'],user=_G['dbuser'],password=_G['dbpw'])
            if conn and conn._db is not None:
                _G['DB'] = conn
                _G['conn'] = conn._db

        if _G['conn']==None:
            _G['DB'] = _G['conn'] = None
            self.ui.statusbar.showMessage(u'* 数据库链接错误.')
            time.sleep(1)
            self.DatabaseDialog()
        else:
            Mainapp.getTaskList()

    def setHeaderMainList(self, header):
        self.ui.mainlist.header().setDefaultAlignment(QtCore.Qt.AlignHCenter)
        self.ui.mainlist.setColumnCount(len(header))
        self.ui.mainlist.setHeaderLabels(header)
        self.ui.mainlist.resizeColumnToContents(0)
        self.ui.mainlist.clear()

    def getTaskList(self):
        self.updateMainListFlag(True, False)
        if _G['conn']==None:
            return
        itemList = []
        self.setHeaderMainList([u'任务名称', u'采集器', u'循环', u'执行时间', u'下次执行时间', u'状态'])
        self.task_state_col = self.ui.mainlist.columnCount()-1
        self.task_nextruntime_col = self.task_state_col-1
        taskList = _G['DB'].query("SELECT t.taskid,t.robotid,t.taskname,t.loop,t.loopperiod,t.runtime,t.nextruntime, r.name FROM `pre_robots_task` t LEFT JOIN `pre_robots` r ON t.robotid = r.robotid ORDER BY t.taskid")
        for i in taskList:
            taskid  = i['taskid']
            isloop  = (i['loop']==1 and [self.yesstr] or [self.nostr])[0]
            runtime = Func.fromTimestamp(i['runtime'])
            nextruntime = (i['nextruntime'] and [Func.fromTimestamp(i['nextruntime'])] or ['-'])[0]

            taskItem = QtGui.QTreeWidgetItem([i['taskname'], i['name'], isloop, runtime, nextruntime])
            taskItem.setIcon(self.task_state_col, QtGui.QIcon(self.task_state_wait))
            taskItem.setData(self.task_id_col, QtCore.Qt.UserRole, QtCore.QVariant(taskid))
            taskItem.setData(self.task_state_col, QtCore.Qt.UserRole, QtCore.QVariant(Task_Flag_Waiting))
            taskItem.setTextAlignment(2, QtCore.Qt.AlignHCenter)
            self.ui.mainlist.addTopLevelItem(taskItem)

            self.taskList[taskid] = {'item': taskItem, 'taskinfo': i}
            self.threadStart(taskid)

    def getRobotList(self):
        self.updateMainListFlag(False, True)
        if _G['conn']==None:
            return
        self.setHeaderMainList([u'采集器名称', u'编码', u'延迟', u'线程', u'倒序模式', u'列表模式', u'下载模式', u'文件后缀'])
        robotList = _G['DB'].query("SELECT * FROM `pre_robots` ORDER BY robotid")
        for i in robotList:
            i['speed']          = str(i['speed'])
            i['threads']        = str(i['threads'])
            i['reverseorder']   = (i['reverseorder'] and [self.yesstr] or [self.nostr])[0]
            i['onlylinks']      = (i['onlylinks'] and [self.yesstr] or [self.nostr])[0]
            i['downloadmode']   = (i['downloadmode'] and [self.yesstr] or [self.nostr])[0]
            robotItem = QtGui.QTreeWidgetItem([i['name'], i['encode'], i['speed'], i['threads'], i['reverseorder'], i['onlylinks'], i['downloadmode'], i['extension']])
            self.ui.mainlist.addTopLevelItem(robotItem)

    def updateMainListFlag(self, task=True, robot=False):
        self.list_with_task = task
        self.list_with_robot = robot

    def updateTaskState(self, state, taskid):
        '''change task state'''
        if not self.list_with_task:
            return
        taskItem = self.taskList[taskid]['item']
        curState = Func._variantConv(taskItem.data(self.task_state_col, QtCore.Qt.UserRole), 'int')
        if curState==state:
            return
        taskItem.setIcon(self.task_state_col, QtGui.QIcon('res/loading.gif'))
        stateIcon = {Task_Flag_Waiting: self.task_state_wait, Task_Flag_Runing: self.task_state_run, Task_Flag_Stoped: self.task_state_stop}
        taskItem.setIcon(self.task_state_col, QtGui.QIcon(stateIcon[state]))
        QtGui.QTreeWidgetItem().setData(self.task_state_col, QtCore.Qt.UserRole, QtCore.QVariant(state))

        if state==Task_Flag_Stoped:
            self.threadStop(taskid)

    def updateNextRunTime(self, timestr, taskid):
        if not self.list_with_task:
            return
        self.taskList[taskid]['item'].setText(self.task_nextruntime_col, timestr)

    def threadStart(self, taskid):
        '''create threads if it's not exist'''
        if self.threadList.has_key(taskid):
            return
        t = RunTask(self.taskList[taskid]['taskinfo'], self)
        self.threadList[taskid] = t
        self.connect(t, QtCore.SIGNAL("Updated"), self.updateNextRunTime)
        self.connect(t, QtCore.SIGNAL("Activated"), self.updateTaskState)
        t.start()

    def threadStop(self, taskid=-1):
        '''stop threads by taskid/all'''
        if not len(self.threadList)>0 or (not self.threadList.has_key(taskid) and taskid!=-1):
            return
        if taskid == -1:
            for i in self.threadList: i[1].stop()
            self.threadList.clear()
        else:
            t = self.threadList[taskid]
            t.stop()

            self.taskList[taskid]['item'].setIcon(self.task_state_col, QtGui.QIcon(self.task_state_stop))
            del self.threadList[taskid]


class TaskUI(QtGui.QDialog):
    def __init__(self, title, parent):
        super(TaskUI, self).__init__(parent)

        self.ui = Ui_TaskDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)
        self.ui.runtime.setMinimumDateTime(QtCore.QDateTime.currentDateTime())

        # get robot list from database
        self.getRobotList()

        # init form field
        self.taskname = self.robotid = self.isloop = self.loopperiod = self.runtime = None

        self.connect(self.ui.robotid, QtCore.SIGNAL("currentIndexChanged(int)"), self.SelectRobot)
        self.connect(self.ui.taskSave, QtCore.SIGNAL("clicked()"), self.verify)

    def getRobotList(self):
        if _G['conn']==None:
            return
        robotList = _G['DB'].query("SELECT * FROM `pre_robots` ORDER BY robotid")
        self.ui.robotid.addItem(u'-选择采集方案-', QtCore.QVariant(0))
        for i in robotList:
            self.ui.robotid.addItem(i['name'], QtCore.QVariant(i['robotid']))

    def SelectRobot(self, index):
        self.robotid = Func._variantConv(self.ui.robotid.itemData(index), 'string')

    def verify(self):
        self.taskname   = Func.toStr(self.ui.taskname.text())
        self.robotid    = int(Func.toStr(self.robotid))
        self.isloop     = (self.ui.isloop.isChecked() and [1] or [0])[0]
        self.loopperiod = self.ui.loopperiod.value()
        self.runtime    = Func.toTimestamp(self.ui.runtime.dateTime())
        if self.taskname and self.robotid:
            _G['DB'].insert('pre_robots_task', robotid=self.robotid, taskname=self.taskname, loop=self.isloop, loopperiod=self.loopperiod, runtime=self.runtime)
            self.accept()


class RobotUI(QtGui.QDialog):
    def __init__(self, title, parent):
        super(RobotUI, self).__init__(parent)

        self.ui = Ui_RobotDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)

        self.connect(self.ui.robotSave, QtCore.SIGNAL("clicked()"), self.verify)

    def serializeListUrl(self, autourl, manualurl):
        manualurlList = manualurl.splitlines()
        listurl = {'auto': autourl, 'manual': manualurl}
        return simplejson.dumps(listurl)

    def verify(self):
        robotname       = Func.toStr(self.ui.robotname.text())
        speed           = self.ui.speed.value()
        threads         = self.ui.threads.value()
        autourl         = Func.toStr(self.ui.autourl.text())
        listpagestart   = self.ui.listpagestart.value()
        listpageend     = self.ui.listpageend.value()
        wildcardlen     = self.ui.wildcardlen.value()
        manualurl       = Func.toStr(self.ui.manualurl.toPlainText())
        stockdata       = Func.toStr(self.ui.stockdata.text())
        encode          = Func.toStr(self.ui.encode.text())
        subjecturlrule  = Func.toStr(self.ui.subjecturlrule.toPlainText())
        subjecturllinkrule = Func.toStr(self.ui.subjecturllinkrule.toPlainText())
        subjectrule     = Func.toStr(self.ui.subjectrule.toPlainText())
        messagerule     = Func.toStr(self.ui.messagerule.toPlainText())
        reverseorder    = (self.ui.reverseorder.isChecked() and [1] or [0])[0]
        onlylinks       = (self.ui.onlylinks.isChecked() and [1] or [0])[0]
        downloadmode    = (self.ui.downloadmode.isChecked() and [1] or [0])[0]
        extension       = Func.toStr(self.ui.extension.text())
        importSQL       = Func.toStr(self.ui.importSQL.toPlainText())
        # serialize listurl to json
        listurl = self.serializeListUrl(autourl, manualurl)
        if robotname and (autourl or manualurl):
            _G['DB'].insert('pre_robots', name=robotname, speed=speed, threads=threads, listurl=listurl, stockdata=stockdata, listpagestart=listpagestart, listpageend=listpageend, wildcardlen=wildcardlen, reverseorder=reverseorder, encode=encode, subjecturlrule=subjecturlrule, subjecturllinkrule=subjecturllinkrule, subjectrule=subjectrule, messagerule=messagerule, onlylinks=onlylinks, downloadmode=downloadmode, extension=extension, importSQL=importSQL)
            self.accept()


class DatabaseUI(QtGui.QDialog):
    def __init__(self, title, flag, parent):
        super(DatabaseUI, self).__init__(parent)

        self.ui = Ui_DatabaseDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)

        _G['dbhost'] and self.ui.dbhost.setText(_G['dbhost'])
        _G['dbname'] and self.ui.dbname.setText(_G['dbname'])
        _G['dbuser'] and self.ui.dbuser.setText(_G['dbuser'])
        _G['dbpw'] and self.ui.dbpw.setText(_G['dbpw'])

        self.connect(self.ui.databaseSave, QtCore.SIGNAL("clicked()"), self.verify)

    def verify(self):
        conn = None
        dbhost  = str(self.ui.dbhost.text())
        dbname  = str(self.ui.dbname.text())
        dbuser  = str(self.ui.dbuser.text())
        dbpw    = str(self.ui.dbpw.text())
        if dbhost and dbname and dbuser and dbpw:
            conn = Connection(host=dbhost,database=dbname,user=dbuser,password=dbpw)
            if conn and conn._db is not None:
                _G['DB'] = conn
                _G['conn'] = conn._db
                _G['dbhost']  = dbhost
                _G['dbname']  = dbname
                _G['dbuser']  = dbuser
                _G['dbpw']    = dbpw
                self.accept()
        if conn==None or conn._db==None:
            self.ui.checklabel.setText(u'<font color="red">* 数据库链接错误.</font>')


class Func:
    def toStr(self, strr):
        if type(strr)==QtCore.QString:
            strr = strr.toLocal8Bit().data()
            strr = self.iConv(strr)
        return strr

    def iConv(self, strr, srcencode='gb2312', dstencode='utf-8'):
        if isinstance(strr, unicode):
            return strr.encode(dstencode)
        elif isinstance(strr, basestring):
            return strr.decode(srcencode).encode(dstencode)
        else:
            return strr

    def toTimestamp(self, val):
        if type(val)==QtCore.QDateTime:
            val = self.toStr(val.toString('yyyy-MM-dd hh:mm:ss'))
            val = time.strptime(val, '%Y-%m-%d %H:%M:%S')
            val = int(time.mktime(val))
        return val

    def fromTimestamp(self, val):
        return str(datetime.datetime.fromtimestamp(int(val)))

    def _variantConv(self, variant, dst):
        """Helper method to cast a QVariant to an integer"""
        res = None
        if not variant.isValid():
            return
        if dst=='int':
            integer, ok = variant.toInt()
            if ok:
                res = integer
        elif dst=='string':
            res = variant.toString()
        return res


class RunTask(QtCore.QThread):
    def __init__(self, taskinfo, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.taskinfo = taskinfo
        self.stoped = False

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
                    _G['DB'].execute("UPDATE `pre_robots_task` SET `nextruntime` = '%d' WHERE `pre_robots_task`.`taskid` = '%d'" % (nextruntime, taskid))
                    self.emit(QtCore.SIGNAL("Updated"), Func.fromTimestamp(nextruntime), taskid)
                else:
                    state = Task_Flag_Stoped

            self.emit(QtCore.SIGNAL("Activated"), state, taskid)
            time.sleep(1)




if __name__ == "__main__":
    _G = {'DB': None, 'conn': None, 'dbhost':'', 'dbname':'', 'dbuser':'', 'dbpw':''}
    ini = IniFile("config.cfg", True)

    # task flag
    Task_Flag_Waiting   = 0
    Task_Flag_Runing    = 1
    Task_Flag_Stoped    = 2

    # helper functions
    Func = Func()

    app = QtGui.QApplication(sys.argv)
    Mainapp = MainUI()

    # show main window
    Mainapp.show()
    # init database connection
    Mainapp.iniDatabaseConn()

    sys.exit(app.exec_())
