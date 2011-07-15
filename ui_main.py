# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created: Fri Jul 15 11:12:54 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 365)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tasklist = QtGui.QTreeWidget(self.centralwidget)
        self.tasklist.setObjectName("tasklist")
        self.verticalLayout.addWidget(self.tasklist)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 700, 23))
        self.menuBar.setObjectName("menuBar")
        self.main_m_add = QtGui.QMenu(self.menuBar)
        self.main_m_add.setObjectName("main_m_add")
        self.main_m_log = QtGui.QMenu(self.menuBar)
        self.main_m_log.setObjectName("main_m_log")
        self.main_m_help = QtGui.QMenu(self.menuBar)
        self.main_m_help.setObjectName("main_m_help")
        self.main_m_set = QtGui.QMenu(self.menuBar)
        self.main_m_set.setObjectName("main_m_set")
        MainWindow.setMenuBar(self.menuBar)
        self.taskadd = QtGui.QAction(MainWindow)
        self.taskadd.setObjectName("taskadd")
        self.robotadd = QtGui.QAction(MainWindow)
        self.robotadd.setObjectName("robotadd")
        self.mquit = QtGui.QAction(MainWindow)
        self.mquit.setObjectName("mquit")
        self.view = QtGui.QAction(MainWindow)
        self.view.setObjectName("view")
        self.save = QtGui.QAction(MainWindow)
        self.save.setObjectName("save")
        self.about = QtGui.QAction(MainWindow)
        self.about.setObjectName("about")
        self.database = QtGui.QAction(MainWindow)
        self.database.setObjectName("database")
        self.main_m_add.addAction(self.taskadd)
        self.main_m_add.addAction(self.robotadd)
        self.main_m_add.addSeparator()
        self.main_m_add.addAction(self.mquit)
        self.main_m_log.addAction(self.view)
        self.main_m_log.addAction(self.save)
        self.main_m_help.addAction(self.about)
        self.main_m_set.addAction(self.database)
        self.menuBar.addAction(self.main_m_add.menuAction())
        self.menuBar.addAction(self.main_m_log.menuAction())
        self.menuBar.addAction(self.main_m_set.menuAction())
        self.menuBar.addAction(self.main_m_help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tasklist.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "任务名称", None, QtGui.QApplication.UnicodeUTF8))
        self.tasklist.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "采集方案", None, QtGui.QApplication.UnicodeUTF8))
        self.tasklist.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "执行时间", None, QtGui.QApplication.UnicodeUTF8))
        self.tasklist.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "下次执行时间", None, QtGui.QApplication.UnicodeUTF8))
        self.tasklist.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "状态", None, QtGui.QApplication.UnicodeUTF8))
        self.main_m_add.setTitle(QtGui.QApplication.translate("MainWindow", "添加", None, QtGui.QApplication.UnicodeUTF8))
        self.main_m_log.setTitle(QtGui.QApplication.translate("MainWindow", "日志", None, QtGui.QApplication.UnicodeUTF8))
        self.main_m_help.setTitle(QtGui.QApplication.translate("MainWindow", "帮助", None, QtGui.QApplication.UnicodeUTF8))
        self.main_m_set.setTitle(QtGui.QApplication.translate("MainWindow", "系统配置", None, QtGui.QApplication.UnicodeUTF8))
        self.taskadd.setText(QtGui.QApplication.translate("MainWindow", "添加任务", None, QtGui.QApplication.UnicodeUTF8))
        self.robotadd.setText(QtGui.QApplication.translate("MainWindow", "添加采集方案", None, QtGui.QApplication.UnicodeUTF8))
        self.mquit.setText(QtGui.QApplication.translate("MainWindow", "退出", None, QtGui.QApplication.UnicodeUTF8))
        self.view.setText(QtGui.QApplication.translate("MainWindow", "查看日志", None, QtGui.QApplication.UnicodeUTF8))
        self.save.setText(QtGui.QApplication.translate("MainWindow", "导出日志", None, QtGui.QApplication.UnicodeUTF8))
        self.about.setText(QtGui.QApplication.translate("MainWindow", "关于", None, QtGui.QApplication.UnicodeUTF8))
        self.database.setText(QtGui.QApplication.translate("MainWindow", "数据库配置", None, QtGui.QApplication.UnicodeUTF8))

