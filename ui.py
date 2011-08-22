#!/usr/bin/python
#-*-coding:utf-8-*-

# The Main App for Data collector.
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

import simplejson
from common import Func
from models import Robot, Task, Session

from PyQt4 import QtCore, QtGui
from ui_robot import Ui_RobotDialog
from ui_task import Ui_TaskDialog

class TaskUI(QtGui.QDialog):
    def __init__(self, title, parent, taskid=0):
        super(TaskUI, self).__init__(parent)

        self.ui = Ui_TaskDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.taskid = taskid

        self.setWindowTitle(title)
        self.ui.runtime.setMinimumDateTime(QtCore.QDateTime.currentDateTime())

        # get robot list from database
        self.getRobotList()

        if taskid>0:
            self.setTaskInfo()

        self.connect(self.ui.taskSave, QtCore.SIGNAL("clicked()"), self.verify)

    def setTaskInfo(self):
        taskinfo = self.parent.taskList[self.taskid]['taskinfo']
        taskname = taskinfo.taskname
        robotid = taskinfo.robotid
        isloop = (taskinfo.loop==1 and [True] or [False])[0]
        loopperiod = taskinfo.loopperiod
        runtime = Func.fromTimestamp(taskinfo.runtime)

        self.ui.taskname.setText(taskname)
        robotIndex = self.ui.robotid.findData(QtCore.QVariant(robotid))
        self.ui.robotid.setCurrentIndex(robotIndex)
        self.ui.isloop.setChecked(isloop)
        self.ui.loopperiod.setValue(loopperiod)
        runtime = QtCore.QDateTime.fromString(QtCore.QString(runtime), 'yyyy-MM-dd hh:mm:ss')
        self.ui.runtime.setMinimumDateTime(runtime)
        self.ui.runtime.setDateTime(runtime)

    def getRobotList(self):
        try:
            session = Session()
            robotList = session.query(Robot).all()
            self.ui.robotid.addItem(u'-选择采集方案-', QtCore.QVariant(0))
            for i in robotList:
                self.ui.robotid.addItem(i.robotname, QtCore.QVariant(i.robotid))
        except:
            self.parent.ui.statusbar.showMessage(u'* 读取列表数据出错了.')

    def verify(self):
        robotid = Func._variantConv(self.ui.robotid.itemData(self.ui.robotid.currentIndex()), 'int')
        taskname = Func.toStr(self.ui.taskname.text())

        if taskname and robotid:
            session = Session()
            if self.taskid>0:
                task = session.query(Task).filter(Task.taskid==self.taskid).first()
                task.robotid = robotid
                task.taskname = taskname
            else:
                task = Task(robotid, taskname)
            task.loop = (self.ui.isloop.isChecked() and [1] or [0])[0]
            task.loopperiod = self.ui.loopperiod.value()
            task.runtime = Func.toTimestamp(self.ui.runtime.dateTime())
            task.nextruntime = 0

            if not self.taskid>0:
                session.add(task)

            session.commit()
            self.accept()


class RobotUI(QtGui.QDialog):
    def __init__(self, title, parent, robotid=0):
        super(RobotUI, self).__init__(parent)

        self.ui = Ui_RobotDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.robotid = robotid

        self.setWindowTitle(title)

        if robotid>0:
            self.setRobotInfo()

        self.connect(self.ui.robotSave, QtCore.SIGNAL("clicked()"), self.verify)

    def setRobotInfo(self):
        session = Session()
        robot = session.query(Robot).filter(Robot.robotid==self.robotid).first()

        self.ui.robotname.setText(robot.robotname)
        self.ui.timeout.setValue(robot.timeout)
        self.ui.threads.setValue(robot.threads)
        url = simplejson.loads(robot.listurl)
        self.ui.autourl.setText(url['auto'])
        self.ui.manualurl.setPlainText("\n".join(url['manual']))
        self.ui.listpagestart.setValue(robot.listpagestart)
        self.ui.listpageend.setValue(robot.listpageend)
        self.ui.wildcardlen.setValue(robot.wildcardlen)
        self.ui.stockdata.setText(robot.stockdata)
        self.ui.rule_mode_xpath.setChecked(robot.rulemode=='xpath')
        self.ui.rule_mode_regex.setChecked(robot.rulemode=='regex')

        self.ui.subjecturlrule.setPlainText(robot.subjecturlrule)
        self.ui.subjecturllinkrule.setPlainText(robot.subjecturllinkrule)
        self.ui.subjectrule.setPlainText(robot.subjectrule)
        self.ui.messagerule.setPlainText(robot.messagerule)
        self.ui.reversemode.setChecked(robot.reversemode==1)
        self.ui.linkmode.setChecked(robot.linkmode==1)
        self.ui.downloadmode.setChecked(robot.downloadmode==1)

    def verify(self):
        robotname       = Func.toStr(self.ui.robotname.text())
        autourl         = Func.toStr(self.ui.autourl.text())
        manualurl       = Func.toStr(self.ui.manualurl.toPlainText())

        # serialize listurl to json
        listurl = Func.serializeListUrl(autourl, manualurl)

        if robotname and (autourl or manualurl):
            session = Session()
            if self.robotid>0:
                robot = session.query(Robot).filter(Robot.robotid==self.robotid).first()
                robot.robotname = robotname
                robot.listurl = listurl
            else:
                robot = Robot(robotname, listurl)
            robot.timeout = self.ui.timeout.value()
            robot.threads = self.ui.threads.value()
            robot.stockdata = Func.toStr(self.ui.stockdata.text())
            robot.listpagestart = self.ui.listpagestart.value()
            robot.listpageend = self.ui.listpageend.value()
            robot.wildcardlen = self.ui.wildcardlen.value()
            robot.rulemode = (self.ui.rule_mode_xpath.isChecked() and ['xpath'] or ['regex'])[0]
            robot.subjecturlrule = Func.toStr(self.ui.subjecturlrule.toPlainText())
            robot.subjecturllinkrule = Func.toStr(self.ui.subjecturllinkrule.toPlainText())
            robot.subjectrule = Func.toStr(self.ui.subjectrule.toPlainText())
            robot.messagerule = Func.toStr(self.ui.messagerule.toPlainText())
            robot.reversemode = (self.ui.reversemode.isChecked() and [1] or [0])[0]
            robot.linkmode = (self.ui.linkmode.isChecked() and [1] or [0])[0]
            robot.downloadmode = (self.ui.downloadmode.isChecked() and [1] or [0])[0]

            if not self.robotid>0:
                session.add(robot)

            session.commit()
            self.accept()