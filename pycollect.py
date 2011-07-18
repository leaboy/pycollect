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

        self.ConnectEvent()

    def ConnectEvent(self):
        # menu
        self.ui.taskadd.triggered.connect(self.TaskDialog)
        self.ui.robotadd.triggered.connect(self.RobotDialog)
        self.ui.mquit.triggered.connect(QtGui.qApp.quit)

        self.ui.database.triggered.connect(self.DatabaseDialog)

    def TaskDialog(self):
        Dialog = TaskUI(u'添加任务', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            self.SaveRegular(Dialog.senderName(), Dialog.senderCodes())

    def RobotDialog(self):
        Dialog = RobotUI(u'添加采集器', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            self.SaveRegular(Dialog.senderName(), Dialog.senderCodes())

    def DatabaseDialog(self, flag=False):
        Dialog = DatabaseUI(u'数据库配置', flag, self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            ini.set("database", "dbhost", _G['dbhost'])
            ini.set("database", "dbname", _G['dbname'])
            ini.set("database", "dbuser", _G['dbuser'])
            ini.set("database", "dbpw", _G['dbpw'])
            self.ui.statusbar.clearMessage()

    def iniDatabaseConn(self):
        conn = flag = False
        _G['dbhost']  = ini.get("database","dbhost")
        _G['dbname']  = ini.get("database","dbname")
        _G['dbuser']  = ini.get("database","dbuser")
        _G['dbpw']    = ini.get("database","dbpw")

        if _G['dbhost']==None or _G['dbname']==None or _G['dbuser']==None or _G['dbpw']==None:
            flag = True
        else:
            _G['DB'] = Connection(host=_G['dbhost'],database=_G['dbname'],user=_G['dbuser'],password=_G['dbpw'])
            if _G['DB']._db is not None: conn = True
            else: _G['DB'] = None

        if conn==False:
            self.ui.statusbar.showMessage(u'* 数据库链接错误.')
            time.sleep(1)
            self.DatabaseDialog(flag)

    def getTaskList(self):
        if _G['DB']==None: return
        taskList = _G['DB'].query("SELECT t.taskid,t.robotid,t.taskname,t.loop,t.loopperiod,t.runtime,t.nextruntime, r.name FROM `pre_robots_task` t LEFT JOIN `pre_robots` r ON t.robotid = r.robotid")
        for i in taskList:
            i['taskname']   = unicode(i['taskname'])
            i['name']       = unicode(i['name'])
            i['runtime']    = str(datetime.datetime.fromtimestamp(i['runtime']))
            i['nextruntime']= str(datetime.datetime.fromtimestamp(i['nextruntime']))
            item = QtGui.QTreeWidgetItem([i['taskname'], i['name'],i['runtime'], i['nextruntime']])
            self.ui.tasklist.addTopLevelItem(item)


class TaskUI(QtGui.QDialog):
    def __init__(self, title, parent):
        super(TaskUI, self).__init__(parent)

        self.ui = Ui_TaskDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)


class RobotUI(QtGui.QDialog):
    def __init__(self, title, parent):
        super(RobotUI, self).__init__(parent)

        self.ui = Ui_RobotDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)


class DatabaseUI(QtGui.QDialog):
    def __init__(self, title, flag, parent):
        super(DatabaseUI, self).__init__(parent)

        self.ui = Ui_DatabaseDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)
        if flag==False:
            self.ui.dbhost.setText(_G['dbhost'])
            self.ui.dbname.setText(_G['dbname'])
            self.ui.dbuser.setText(_G['dbuser'])
            self.ui.dbpw.setText(_G['dbpw'])

        self.connect(self.ui.databaseSave, QtCore.SIGNAL("clicked()"), self.verify)

    def verify(self):
        _G['dbhost']  = str(self.ui.dbhost.text())
        _G['dbname']  = str(self.ui.dbname.text())
        _G['dbuser']  = str(self.ui.dbuser.text())
        _G['dbpw']    = str(self.ui.dbpw.text())
        if _G['dbhost'] and _G['dbname'] and _G['dbuser'] and _G['dbpw']:
            _G['DB'] = Connection(host=_G['dbhost'],database=_G['dbname'],user=_G['dbuser'],password=_G['dbpw'])
        if _G['DB'] and _G['DB']._db is not None:
            self.accept()
        else:
            _G['DB'] = None
            self.ui.checklabel.setText(u'<font color="red">* 数据库链接错误.</font>')


class func():
    pass


if __name__ == "__main__":
    _G = {'DB': None, 'dbhost':'', 'dbname':'', 'dbuser':'', 'dbpw':''}
    ini = IniFile("config.cfg", True)

    app = QtGui.QApplication(sys.argv)
    Pycollectapp = PycollectUI()

    ''' load stylesheet '''
    styleFile = QtCore.QFile("stylesheet.qss")
    if styleFile.open(QtCore.QIODevice.ReadOnly):
        Pycollectapp.setStyleSheet(str(styleFile.readAll()))
    ''' show main window '''
    Pycollectapp.show()

    ''' init database connection '''
    Pycollectapp.iniDatabaseConn()
    ''' get task list from database '''
    Pycollectapp.getTaskList()

    sys.exit(app.exec_())
