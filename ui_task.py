# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Task.ui'
#
# Created: Wed Aug 24 10:47:54 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TaskDialog(object):
    def setupUi(self, TaskDialog):
        TaskDialog.setObjectName("TaskDialog")
        TaskDialog.resize(399, 457)
        self.verticalLayout = QtGui.QVBoxLayout(TaskDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(TaskDialog)
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(-1, 3, 6, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(84, 0))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.taskname = QtGui.QLineEdit(self.groupBox)
        self.taskname.setObjectName("taskname")
        self.gridLayout.addWidget(self.taskname, 0, 1, 1, 2)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.robotid = QtGui.QComboBox(self.groupBox)
        self.robotid.setObjectName("robotid")
        self.gridLayout.addWidget(self.robotid, 1, 1, 1, 2)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.isloop = QtGui.QCheckBox(self.groupBox)
        self.isloop.setText("")
        self.isloop.setObjectName("isloop")
        self.gridLayout.addWidget(self.isloop, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.runtime = QtGui.QDateTimeEdit(self.groupBox)
        self.runtime.setObjectName("runtime")
        self.gridLayout.addWidget(self.runtime, 4, 1, 1, 2)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 2, 1, 1)
        self.loopperiod = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loopperiod.sizePolicy().hasHeightForWidth())
        self.loopperiod.setSizePolicy(sizePolicy)
        self.loopperiod.setMinimum(3600)
        self.loopperiod.setMaximum(31536000)
        self.loopperiod.setSingleStep(60)
        self.loopperiod.setProperty("value", 86400)
        self.loopperiod.setObjectName("loopperiod")
        self.gridLayout.addWidget(self.loopperiod, 3, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(TaskDialog)
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setContentsMargins(-1, 3, 6, 3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.taskSave = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taskSave.sizePolicy().hasHeightForWidth())
        self.taskSave.setSizePolicy(sizePolicy)
        self.taskSave.setObjectName("taskSave")
        self.gridLayout_3.addWidget(self.taskSave, 3, 1, 1, 1)
        self.plainTextEdit = QtGui.QPlainTextEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_3.addWidget(self.plainTextEdit, 2, 1, 1, 3)
        self.label_14 = QtGui.QLabel(self.groupBox_2)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 2, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sqlite_layout = QtGui.QWidget(self.groupBox_2)
        self.sqlite_layout.setObjectName("sqlite_layout")
        self.gridLayout_2 = QtGui.QGridLayout(self.sqlite_layout)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.sqlite_dbname = QtGui.QLineEdit(self.sqlite_layout)
        self.sqlite_dbname.setObjectName("sqlite_dbname")
        self.gridLayout_2.addWidget(self.sqlite_dbname, 0, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.sqlite_layout)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.sqlite_layout)
        self.mysql_layout = QtGui.QWidget(self.groupBox_2)
        self.mysql_layout.setObjectName("mysql_layout")
        self.gridLayout_4 = QtGui.QGridLayout(self.mysql_layout)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_10 = QtGui.QLabel(self.mysql_layout)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 1)
        self.mysql_dbhost = QtGui.QLineEdit(self.mysql_layout)
        self.mysql_dbhost.setObjectName("mysql_dbhost")
        self.gridLayout_4.addWidget(self.mysql_dbhost, 0, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.mysql_layout)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 1, 0, 1, 1)
        self.label_12 = QtGui.QLabel(self.mysql_layout)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 2, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.mysql_layout)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 3, 0, 1, 1)
        self.mysql_dbuser = QtGui.QLineEdit(self.mysql_layout)
        self.mysql_dbuser.setObjectName("mysql_dbuser")
        self.gridLayout_4.addWidget(self.mysql_dbuser, 1, 1, 1, 1)
        self.mysql_dbpw = QtGui.QLineEdit(self.mysql_layout)
        self.mysql_dbpw.setEchoMode(QtGui.QLineEdit.Password)
        self.mysql_dbpw.setObjectName("mysql_dbpw")
        self.gridLayout_4.addWidget(self.mysql_dbpw, 2, 1, 1, 1)
        self.mysql_dbname = QtGui.QLineEdit(self.mysql_layout)
        self.mysql_dbname.setObjectName("mysql_dbname")
        self.gridLayout_4.addWidget(self.mysql_dbname, 3, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.mysql_layout)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 1, 1, 1, 3)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.dbtype_sqlite = QtGui.QRadioButton(self.groupBox_2)
        self.dbtype_sqlite.setObjectName("dbtype_sqlite")
        self.verticalLayout_3.addWidget(self.dbtype_sqlite)
        self.dbtype_mysql = QtGui.QRadioButton(self.groupBox_2)
        self.dbtype_mysql.setChecked(True)
        self.dbtype_mysql.setObjectName("dbtype_mysql")
        self.verticalLayout_3.addWidget(self.dbtype_mysql)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 1, 1, 3)
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.connTest = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connTest.sizePolicy().hasHeightForWidth())
        self.connTest.setSizePolicy(sizePolicy)
        self.connTest.setObjectName("connTest")
        self.gridLayout_3.addWidget(self.connTest, 3, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 3, 3, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_3)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(TaskDialog)
        QtCore.QMetaObject.connectSlotsByName(TaskDialog)
        TaskDialog.setTabOrder(self.taskname, self.robotid)
        TaskDialog.setTabOrder(self.robotid, self.isloop)
        TaskDialog.setTabOrder(self.isloop, self.loopperiod)
        TaskDialog.setTabOrder(self.loopperiod, self.runtime)

    def retranslateUi(self, TaskDialog):
        TaskDialog.setWindowTitle(QtGui.QApplication.translate("TaskDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("TaskDialog", "任务配置>>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("TaskDialog", "任务名称", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TaskDialog", "采集方案", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("TaskDialog", "是否循环", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("TaskDialog", "循环周期", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("TaskDialog", "执行时间", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("TaskDialog", "单位：秒", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("TaskDialog", "存储方案>>", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSave.setText(QtGui.QApplication.translate("TaskDialog", "保存", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("TaskDialog", "执行SQL语句", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("TaskDialog", "文件地址", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("TaskDialog", "数据库地址", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("TaskDialog", "数据库用户名", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("TaskDialog", "数据库密码", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("TaskDialog", "数据库名称", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("TaskDialog", "数据库连接信息", None, QtGui.QApplication.UnicodeUTF8))
        self.dbtype_sqlite.setText(QtGui.QApplication.translate("TaskDialog", "SQLite", None, QtGui.QApplication.UnicodeUTF8))
        self.dbtype_mysql.setText(QtGui.QApplication.translate("TaskDialog", "MySQL", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("TaskDialog", "数据库类型", None, QtGui.QApplication.UnicodeUTF8))
        self.connTest.setText(QtGui.QApplication.translate("TaskDialog", "测试连接", None, QtGui.QApplication.UnicodeUTF8))

