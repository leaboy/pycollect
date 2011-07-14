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

import re, sys, time, os
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


DB = None
ini = IniFile("config.cfg")

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

    def DatabaseDialog(self):
        Dialog = DatabaseUI(u'数据库配置', self)
        if Dialog.exec_() == QtGui.QDialog.Accepted:
            self.SaveRegular(Dialog.senderName(), Dialog.senderCodes())



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
    def __init__(self, title, parent):
        super(DatabaseUI, self).__init__(parent)

        self.ui = Ui_DatabaseDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)
        self.connect(self.ui.databaseSave, QtCore.SIGNAL("clicked()"), self.verify)

    def verify(self):
        global DB
        dbhost = str(self.ui.dbhost.text())
        dbname = str(self.ui.dbname.text())
        dbuser = str(self.ui.dbuser.text())
        dbpw = str(self.ui.dbpw.text())
        if dbhost and dbname and dbuser and dbpw:
            DB = Connection(host=dbhost,database=dbname,user=dbuser,password=dbpw)
            print DB._db
            return
        if DB==None:
            self.ui.checklabel.setText(u'数据库链接错误')
        self.accept()
        return


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Pycollectapp = PycollectUI()
    Pycollectapp.show()

    # check database setting
    dbhost = ini.get("default","dbhost")
    dbname = ini.get("default","dbname")
    dbuser = ini.get("default","dbuser")
    dbpw = ini.get("default","dbpw")

    if dbhost==None or dbname==None or dbuser==None or dbpw==None:
        Pycollectapp.DatabaseDialog()

    sys.exit(app.exec_())
