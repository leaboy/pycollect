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


ini = IniFile("config.cfg")

class PycollectUI(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(PycollectUI, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # test database setting
        HostIP = ini.get("default","dbhost")
        HostName = ini.get("default","dbname")
        HostImage = ini.get("default","dbuser")
        HostImage = ini.get("default","dbpw")

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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Pycollectapp = PycollectUI()
    Pycollectapp.show()
    sys.exit(app.exec_())
