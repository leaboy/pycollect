# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Task.ui'
#
# Created: Thu Jul 14 14:45:37 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TaskDialog(object):
    def setupUi(self, TaskDialog):
        TaskDialog.setObjectName("TaskDialog")
        TaskDialog.resize(224, 166)
        TaskDialog.setMinimumSize(QtCore.QSize(224, 166))
        TaskDialog.setMaximumSize(QtCore.QSize(224, 166))
        self.verticalLayout = QtGui.QVBoxLayout(TaskDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(TaskDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.taskname = QtGui.QLineEdit(TaskDialog)
        self.taskname.setObjectName("taskname")
        self.gridLayout.addWidget(self.taskname, 0, 1, 1, 2)
        self.label = QtGui.QLabel(TaskDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.robotid = QtGui.QComboBox(TaskDialog)
        self.robotid.setObjectName("robotid")
        self.gridLayout.addWidget(self.robotid, 1, 1, 1, 2)
        self.label_3 = QtGui.QLabel(TaskDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.isloop = QtGui.QCheckBox(TaskDialog)
        self.isloop.setText("")
        self.isloop.setObjectName("isloop")
        self.gridLayout.addWidget(self.isloop, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(TaskDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_6 = QtGui.QLabel(TaskDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.runtime = QtGui.QDateTimeEdit(TaskDialog)
        self.runtime.setObjectName("runtime")
        self.gridLayout.addWidget(self.runtime, 4, 1, 1, 2)
        self.pushButton = QtGui.QPushButton(TaskDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 1, 1, 1)
        self.label_5 = QtGui.QLabel(TaskDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 2, 1, 1)
        self.loopperiod = QtGui.QSpinBox(TaskDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loopperiod.sizePolicy().hasHeightForWidth())
        self.loopperiod.setSizePolicy(sizePolicy)
        self.loopperiod.setMaximum(31536000)
        self.loopperiod.setSingleStep(10)
        self.loopperiod.setProperty("value", 86400)
        self.loopperiod.setObjectName("loopperiod")
        self.gridLayout.addWidget(self.loopperiod, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(TaskDialog)
        QtCore.QMetaObject.connectSlotsByName(TaskDialog)

    def retranslateUi(self, TaskDialog):
        TaskDialog.setWindowTitle(QtGui.QApplication.translate("TaskDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("TaskDialog", "任务名称", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TaskDialog", "采集方案", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("TaskDialog", "是否循环", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("TaskDialog", "循环周期", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("TaskDialog", "执行时间", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("TaskDialog", "保存", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("TaskDialog", "单位：秒", None, QtGui.QApplication.UnicodeUTF8))

