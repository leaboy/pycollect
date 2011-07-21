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


class PycollectUI(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(PycollectUI, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # menu
        self.ui.taskadd.triggered.connect(self.TaskDialog)
        self.ui.robotadd.triggered.connect(self.RobotDialog)
        self.ui.mquit.triggered.connect(QtGui.qApp.quit)

        self.ui.database.triggered.connect(self.DatabaseDialog)

    def TaskDialog(self):
        Dialog = TaskUI(u'添加任务', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            self.getTaskList()

    def RobotDialog(self):
        Dialog = RobotUI(u'添加采集器', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            print 'save robot'

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

    def getTaskList(self):
        if _G['conn']==None: return
        self.ui.tasklist.clear()
        taskList = _G['DB'].query("SELECT t.taskid,t.robotid,t.taskname,t.loop,t.loopperiod,t.runtime,t.nextruntime, r.name FROM `pre_robots_task` t LEFT JOIN `pre_robots` r ON t.robotid = r.robotid")
        for i in taskList:
            i['runtime']    = str(datetime.datetime.fromtimestamp(i['runtime']))
            i['nextruntime']= (i['nextruntime'] and [str(datetime.datetime.fromtimestamp(i['nextruntime']))] or ['-'])[0]
            item = QtGui.QTreeWidgetItem([i['taskname'], i['name'],i['runtime'], i['nextruntime']])
            self.ui.tasklist.addTopLevelItem(item)


class TaskUI(QtGui.QDialog):
    def __init__(self, title, parent):
        super(TaskUI, self).__init__(parent)

        self.ui = Ui_TaskDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)
        self.ui.runtime.setMinimumDateTime(QtCore.QDateTime.currentDateTime())

        ''' get robot list from database '''
        self.getRobotList()

        ''' init form field '''
        self.taskname = self.robotid = self.isloop = self.loopperiod = self.runtime = None

        self.connect(self.ui.robotid, QtCore.SIGNAL("currentIndexChanged(int)"), self.SelectRobot)
        self.connect(self.ui.taskSave, QtCore.SIGNAL("clicked()"), self.verify)

    def getRobotList(self):
        if _G['conn']==None: return
        robotList = _G['DB'].query("SELECT * FROM `pre_robots` ORDER BY robotid")
        self.ui.robotid.addItem(u'-选择采集方案-', QtCore.QVariant(0))
        for i in robotList:
            self.ui.robotid.addItem(i['name'], QtCore.QVariant(i['robotid']))

    def SelectRobot(self, index):
        self.robotid = self.ui.robotid.itemData(index).toString()

    def verify(self):
        self.taskname   = Func.toStr(self.ui.taskname.text())
        self.robotid    = int(Func.toStr(self.robotid))
        self.isloop     = (self.ui.isloop.isChecked() and [1] or [0])[0]
        self.loopperiod = self.ui.loopperiod.value()
        self.runtime    = Func.toTimestamp(self.ui.runtime.dateTime())
        if self.taskname and self.robotid:
            _G['DB'].execute("INSERT INTO `pre_robots_task` (`robotid` ,`taskname` ,`loop` ,`loopperiod` ,`runtime`)VALUES ('%s',  '%s',  '%d',  '%d',  '%d')" % (self.robotid, self.taskname, self.isloop, self.loopperiod, self.runtime))
            self.accept()


class RobotUI(QtGui.QDialog):
    def __init__(self, title, parent):
        super(RobotUI, self).__init__(parent)

        self.ui = Ui_RobotDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)

        self.connect(self.ui.robotSave, QtCore.SIGNAL("clicked()"), self.verify)

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

        listurl = self.serializeListUrl(autourl, manualurl)

        print type(robotname), type(speed), type(threads), type(autourl), type(listpagestart), type(listpageend), type(wildcardlen), type(manualurl), type(stockdata)
        print 'val: %s, %d, %d, %s, %d, %d, %d, %s, %s,     %s, %s, %s, %s, %s, %d, %d, %d, %s,     %s' % (robotname, speed, threads, autourl, listpagestart, listpageend, wildcardlen, manualurl, stockdata, encode, subjecturlrule, subjecturllinkrule, subjectrule, messagerule, reverseorder, onlylinks, downloadmode, extension, importSQL)
        #,     %s, %s, %s, %s, %s, %d, %d, %d, %s,     %s
        #, encode, subjecturlrule, subjecturllinkrule, subjectrule, messagerule, reverseorder, onlylinks, downloadmode, extension, importSQL
        if robotname and (autourl or manualurl):
            _G['DB'].execute("INSERT INTO `pycollect`.`pre_robots` (`name`, `listurl`, `stockdata`, `listpagestart`, `listpageend`, `wildcardlen`, `reverseorder`, `encode`, `subjecturlrule`, `subjecturllinkrule`, `subjectrule`, `messagerule`, `onlylinks`, `downloadmode`, `extension`, `importSQL`) VALUES ('%s', '%s', '%s', '%d', '%d', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%s', '%s')" % (robotname, listurl, stockdata, listpagestart, listpageend, wildcardlen, reverseorder, encode, subjecturlrule, subjecturllinkrule, subjectrule, messagerule, onlylinks, downloadmode, extension, importSQL))
            self.accept()

    def serializeListUrl(self, autourl, manualurl):
        manualurlList = manualurl.splitlines()
        listurl = {'auto': autourl, 'manual': manualurl}
        return simplejson.dumps(listurl)


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
        pass


if __name__ == "__main__":
    _G = {'DB': None, 'conn': None, 'dbhost':'', 'dbname':'', 'dbuser':'', 'dbpw':''}
    ini = IniFile("config.cfg", True)
    Func = Func()

    app = QtGui.QApplication(sys.argv)
    Pycollectapp = PycollectUI()

    ''' load stylesheet '''
    #styleFile = QtCore.QFile("stylesheet.qss")
    #if styleFile.open(QtCore.QIODevice.ReadOnly):
    #    Pycollectapp.setStyleSheet(str(styleFile.readAll()))

    ''' show main window '''
    Pycollectapp.show()
    ''' init database connection '''
    Pycollectapp.iniDatabaseConn()
    ''' get task list from database '''
    Pycollectapp.getTaskList()

    sys.exit(app.exec_())
