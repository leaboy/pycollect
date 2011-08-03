#!/usr/bin/python
#-*-coding:utf-8-*-

# The Main App for Data collector.
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

from common import Func
from database import Connection

from PyQt4 import QtCore, QtGui
from ui_robot import Ui_RobotDialog
from ui_task import Ui_TaskDialog
from ui_database import Ui_DatabaseDialog

class TaskUI(QtGui.QDialog):
    def __init__(self, title, parent):
        super(TaskUI, self).__init__(parent)

        self.ui = Ui_TaskDialog()
        self.ui.setupUi(self)
        self.parent = parent

        self.setWindowTitle(title)
        self.ui.runtime.setMinimumDateTime(QtCore.QDateTime.currentDateTime())

        # get robot list from database
        self.getRobotList()

        # init form field
        self.taskname = None
        self.robotid = self.isloop = self.loopperiod = self.runtime = 0

        self.connect(self.ui.robotid, QtCore.SIGNAL("currentIndexChanged(int)"), self.SelectRobot)
        self.connect(self.ui.taskSave, QtCore.SIGNAL("clicked()"), self.verify)

    def getRobotList(self):
        try:
            _G = self.parent.getConnection()
            robotList = _G['DB'].query("SELECT * FROM `pre_robots` ORDER BY robotid")
            self.ui.robotid.addItem(u'-选择采集方案-', QtCore.QVariant(0))
            for i in robotList:
                self.ui.robotid.addItem(i['name'], QtCore.QVariant(i['robotid']))
        except:
            self.parent.ui.statusbar.showMessage(u'* 数据库链接错误.')

    def SelectRobot(self, index):
        self.robotid = Func._variantConv(self.ui.robotid.itemData(index), 'string')

    def verify(self):
        self.taskname   = Func.toStr(self.ui.taskname.text())
        self.robotid    = int(Func.toStr(self.robotid))
        self.isloop     = (self.ui.isloop.isChecked() and [1] or [0])[0]
        self.loopperiod = self.ui.loopperiod.value()
        self.runtime    = Func.toTimestamp(self.ui.runtime.dateTime())
        if self.taskname and self.robotid:
            _G = self.parent.getConnection()
            _G['DB'].insert('pre_robots_task', robotid=self.robotid, taskname=self.taskname, loop=self.isloop, loopperiod=self.loopperiod, runtime=self.runtime)
            self.accept()


class RobotUI(QtGui.QDialog):
    def __init__(self, title, parent):
        super(RobotUI, self).__init__(parent)

        self.ui = Ui_RobotDialog()
        self.ui.setupUi(self)
        self.parent = parent

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
        rule_mode_xpath = (self.ui.rule_mode_xpath.isChecked() and [1] or [0])[0]
        rule_mode_regex = (self.ui.rule_mode_regex.isChecked() and [1] or [0])[0]
        rulemode        = (rule_mode_xpath==1 and ['xpath'] or ['regex'])[0]
        subjecturlrule  = Func.toStr(self.ui.subjecturlrule.toPlainText())
        subjecturllinkrule = Func.toStr(self.ui.subjecturllinkrule.toPlainText())
        subjectrule     = Func.toStr(self.ui.subjectrule.toPlainText())
        messagerule     = Func.toStr(self.ui.messagerule.toPlainText())
        reverseorder    = (self.ui.reverseorder.isChecked() and [1] or [0])[0]
        linkmode        = (self.ui.linkmode.isChecked() and [1] or [0])[0]
        downloadmode    = (self.ui.downloadmode.isChecked() and [1] or [0])[0]
        importSQL       = Func.toStr(self.ui.importSQL.toPlainText())
        # serialize listurl to json
        listurl = Func.serializeListUrl(autourl, manualurl)
        if robotname and (autourl or manualurl):
            _G = self.parent.getConnection()
            _G['DB'].insert('pre_robots', name=robotname, speed=speed, threads=threads, listurl=listurl, stockdata=stockdata, listpagestart=listpagestart, listpageend=listpageend, wildcardlen=wildcardlen, reverseorder=reverseorder, rulemode=rulemode, subjecturlrule=subjecturlrule, subjecturllinkrule=subjecturllinkrule, subjectrule=subjectrule, messagerule=messagerule, linkmode=linkmode, downloadmode=downloadmode, importSQL=importSQL)
            self.accept()


class DatabaseUI(QtGui.QDialog):
    def __init__(self, title, flag, parent):
        super(DatabaseUI, self).__init__(parent)

        self.ui = Ui_DatabaseDialog()
        self.ui.setupUi(self)
        self.parent = parent

        self.setWindowTitle(title)

        _G = self.parent.getConnection()
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
                _G = self.parent.getConnection()
                _G['DB'] = conn
                _G['conn'] = conn._db
                _G['dbhost']  = dbhost
                _G['dbname']  = dbname
                _G['dbuser']  = dbuser
                _G['dbpw']    = dbpw
                self.accept()
        if conn==None or conn._db==None:
            self.ui.checklabel.setText(u'<font color="red">* 数据库链接错误.</font>')