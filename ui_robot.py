# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Robot.ui'
#
# Created: Thu Jul 14 14:45:33 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RobotDialog(object):
    def setupUi(self, RobotDialog):
        RobotDialog.setObjectName("RobotDialog")
        RobotDialog.resize(537, 465)
        self.verticalLayout = QtGui.QVBoxLayout(RobotDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(RobotDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_7.setMargin(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBox_6 = QtGui.QGroupBox(self.tab_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setStyleSheet("None")
        self.groupBox_6.setFlat(True)
        self.groupBox_6.setCheckable(False)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_6.setContentsMargins(9, 3, 6, 3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_11 = QtGui.QLabel(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QtCore.QSize(120, 0))
        self.label_11.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_11.setObjectName("label_11")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_11)
        self.label_12 = QtGui.QLabel(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName("label_12")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_12)
        self.label_13 = QtGui.QLabel(self.groupBox_6)
        self.label_13.setObjectName("label_13")
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_13)
        self.robotname = QtGui.QLineEdit(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.robotname.sizePolicy().hasHeightForWidth())
        self.robotname.setSizePolicy(sizePolicy)
        self.robotname.setObjectName("robotname")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.robotname)
        self.speed = QtGui.QSpinBox(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speed.sizePolicy().hasHeightForWidth())
        self.speed.setSizePolicy(sizePolicy)
        self.speed.setMaximum(99)
        self.speed.setProperty("value", 1)
        self.speed.setObjectName("speed")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.speed)
        self.threads = QtGui.QSpinBox(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.threads.sizePolicy().hasHeightForWidth())
        self.threads.setSizePolicy(sizePolicy)
        self.threads.setProperty("value", 10)
        self.threads.setObjectName("threads")
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.threads)
        self.horizontalLayout_6.addLayout(self.formLayout_4)
        self.verticalLayout_7.addWidget(self.groupBox_6)
        self.groupBox_8 = QtGui.QGroupBox(self.tab_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_8.sizePolicy().hasHeightForWidth())
        self.groupBox_8.setSizePolicy(sizePolicy)
        self.groupBox_8.setStyleSheet("None")
        self.groupBox_8.setFlat(True)
        self.groupBox_8.setObjectName("groupBox_8")
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_8.setContentsMargins(9, 3, 6, 3)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_30 = QtGui.QLabel(self.groupBox_8)
        self.label_30.setObjectName("label_30")
        self.gridLayout_6.addWidget(self.label_30, 0, 0, 1, 1)
        self.gridLayout_7 = QtGui.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_31 = QtGui.QLabel(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        self.label_31.setMinimumSize(QtCore.QSize(65, 0))
        self.label_31.setMaximumSize(QtCore.QSize(65, 16777215))
        self.label_31.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_31.setObjectName("label_31")
        self.gridLayout_7.addWidget(self.label_31, 0, 0, 1, 1)
        self.autourl_2 = QtGui.QLineEdit(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autourl_2.sizePolicy().hasHeightForWidth())
        self.autourl_2.setSizePolicy(sizePolicy)
        self.autourl_2.setMouseTracking(True)
        self.autourl_2.setAcceptDrops(True)
        self.autourl_2.setObjectName("autourl_2")
        self.gridLayout_7.addWidget(self.autourl_2, 0, 1, 1, 4)
        self.label_32 = QtGui.QLabel(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy)
        self.label_32.setObjectName("label_32")
        self.gridLayout_7.addWidget(self.label_32, 1, 0, 1, 1)
        self.listpagestart_2 = QtGui.QLineEdit(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listpagestart_2.sizePolicy().hasHeightForWidth())
        self.listpagestart_2.setSizePolicy(sizePolicy)
        self.listpagestart_2.setMinimumSize(QtCore.QSize(45, 0))
        self.listpagestart_2.setMaximumSize(QtCore.QSize(45, 16777215))
        self.listpagestart_2.setObjectName("listpagestart_2")
        self.gridLayout_7.addWidget(self.listpagestart_2, 1, 1, 1, 1)
        self.label_33 = QtGui.QLabel(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        self.label_33.setObjectName("label_33")
        self.gridLayout_7.addWidget(self.label_33, 1, 2, 1, 1)
        self.listpageend_2 = QtGui.QLineEdit(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listpageend_2.sizePolicy().hasHeightForWidth())
        self.listpageend_2.setSizePolicy(sizePolicy)
        self.listpageend_2.setMinimumSize(QtCore.QSize(45, 0))
        self.listpageend_2.setMaximumSize(QtCore.QSize(45, 16777215))
        self.listpageend_2.setObjectName("listpageend_2")
        self.gridLayout_7.addWidget(self.listpageend_2, 1, 3, 1, 1)
        self.label_34 = QtGui.QLabel(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy)
        self.label_34.setObjectName("label_34")
        self.gridLayout_7.addWidget(self.label_34, 2, 0, 1, 1)
        self.wildcardlen_2 = QtGui.QLineEdit(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wildcardlen_2.sizePolicy().hasHeightForWidth())
        self.wildcardlen_2.setSizePolicy(sizePolicy)
        self.wildcardlen_2.setMinimumSize(QtCore.QSize(45, 0))
        self.wildcardlen_2.setMaximumSize(QtCore.QSize(45, 16777215))
        self.wildcardlen_2.setObjectName("wildcardlen_2")
        self.gridLayout_7.addWidget(self.wildcardlen_2, 2, 1, 1, 1)
        self.label_35 = QtGui.QLabel(self.groupBox_8)
        self.label_35.setObjectName("label_35")
        self.gridLayout_7.addWidget(self.label_35, 2, 2, 1, 3)
        self.gridLayout_6.addLayout(self.gridLayout_7, 0, 1, 1, 1)
        self.label_36 = QtGui.QLabel(self.groupBox_8)
        self.label_36.setObjectName("label_36")
        self.gridLayout_6.addWidget(self.label_36, 1, 0, 1, 1)
        self.manualurl_2 = QtGui.QPlainTextEdit(self.groupBox_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manualurl_2.sizePolicy().hasHeightForWidth())
        self.manualurl_2.setSizePolicy(sizePolicy)
        self.manualurl_2.setObjectName("manualurl_2")
        self.gridLayout_6.addWidget(self.manualurl_2, 1, 1, 1, 1)
        self.horizontalLayout_8.addLayout(self.gridLayout_6)
        self.verticalLayout_7.addWidget(self.groupBox_8)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.tab_5)
        self.verticalLayout_8.setMargin(6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.groupBox_9 = QtGui.QGroupBox(self.tab_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_9.sizePolicy().hasHeightForWidth())
        self.groupBox_9.setSizePolicy(sizePolicy)
        self.groupBox_9.setStyleSheet("None")
        self.groupBox_9.setFlat(True)
        self.groupBox_9.setCheckable(False)
        self.groupBox_9.setObjectName("groupBox_9")
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_9.setContentsMargins(9, 3, 6, 3)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.gridLayout_8 = QtGui.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_37 = QtGui.QLabel(self.groupBox_9)
        self.label_37.setObjectName("label_37")
        self.gridLayout_8.addWidget(self.label_37, 0, 0, 1, 1)
        self.encode_2 = QtGui.QLineEdit(self.groupBox_9)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.encode_2.sizePolicy().hasHeightForWidth())
        self.encode_2.setSizePolicy(sizePolicy)
        self.encode_2.setMaximumSize(QtCore.QSize(45, 16777215))
        self.encode_2.setObjectName("encode_2")
        self.gridLayout_8.addWidget(self.encode_2, 0, 1, 1, 1)
        self.label_38 = QtGui.QLabel(self.groupBox_9)
        self.label_38.setTextFormat(QtCore.Qt.RichText)
        self.label_38.setObjectName("label_38")
        self.gridLayout_8.addWidget(self.label_38, 1, 0, 1, 1)
        self.subjecturlrule_2 = QtGui.QPlainTextEdit(self.groupBox_9)
        self.subjecturlrule_2.setObjectName("subjecturlrule_2")
        self.gridLayout_8.addWidget(self.subjecturlrule_2, 1, 1, 1, 1)
        self.label_39 = QtGui.QLabel(self.groupBox_9)
        self.label_39.setTextFormat(QtCore.Qt.RichText)
        self.label_39.setObjectName("label_39")
        self.gridLayout_8.addWidget(self.label_39, 2, 0, 1, 1)
        self.subjecturllinkrule_2 = QtGui.QPlainTextEdit(self.groupBox_9)
        self.subjecturllinkrule_2.setObjectName("subjecturllinkrule_2")
        self.gridLayout_8.addWidget(self.subjecturllinkrule_2, 2, 1, 1, 1)
        self.label_40 = QtGui.QLabel(self.groupBox_9)
        self.label_40.setTextFormat(QtCore.Qt.RichText)
        self.label_40.setObjectName("label_40")
        self.gridLayout_8.addWidget(self.label_40, 3, 0, 1, 1)
        self.subjectrule_2 = QtGui.QPlainTextEdit(self.groupBox_9)
        self.subjectrule_2.setObjectName("subjectrule_2")
        self.gridLayout_8.addWidget(self.subjectrule_2, 3, 1, 1, 1)
        self.label_41 = QtGui.QLabel(self.groupBox_9)
        self.label_41.setTextFormat(QtCore.Qt.RichText)
        self.label_41.setObjectName("label_41")
        self.gridLayout_8.addWidget(self.label_41, 4, 0, 1, 1)
        self.messagerule_2 = QtGui.QPlainTextEdit(self.groupBox_9)
        self.messagerule_2.setObjectName("messagerule_2")
        self.gridLayout_8.addWidget(self.messagerule_2, 4, 1, 1, 1)
        self.gridLayout_9 = QtGui.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.reverseorder_2 = QtGui.QCheckBox(self.groupBox_9)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reverseorder_2.sizePolicy().hasHeightForWidth())
        self.reverseorder_2.setSizePolicy(sizePolicy)
        self.reverseorder_2.setObjectName("reverseorder_2")
        self.gridLayout_9.addWidget(self.reverseorder_2, 0, 0, 1, 1)
        self.onlylinks_2 = QtGui.QCheckBox(self.groupBox_9)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.onlylinks_2.sizePolicy().hasHeightForWidth())
        self.onlylinks_2.setSizePolicy(sizePolicy)
        self.onlylinks_2.setObjectName("onlylinks_2")
        self.gridLayout_9.addWidget(self.onlylinks_2, 0, 1, 1, 1)
        self.downloadmode_2 = QtGui.QCheckBox(self.groupBox_9)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadmode_2.sizePolicy().hasHeightForWidth())
        self.downloadmode_2.setSizePolicy(sizePolicy)
        self.downloadmode_2.setObjectName("downloadmode_2")
        self.gridLayout_9.addWidget(self.downloadmode_2, 0, 2, 1, 1)
        self.extension_2 = QtGui.QLineEdit(self.groupBox_9)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extension_2.sizePolicy().hasHeightForWidth())
        self.extension_2.setSizePolicy(sizePolicy)
        self.extension_2.setMinimumSize(QtCore.QSize(0, 0))
        self.extension_2.setMaximumSize(QtCore.QSize(45, 16777215))
        self.extension_2.setText("")
        self.extension_2.setMaxLength(10)
        self.extension_2.setObjectName("extension_2")
        self.gridLayout_9.addWidget(self.extension_2, 0, 3, 1, 1)
        self.label_42 = QtGui.QLabel(self.groupBox_9)
        self.label_42.setObjectName("label_42")
        self.gridLayout_9.addWidget(self.label_42, 0, 4, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_9, 5, 1, 1, 1)
        self.label_43 = QtGui.QLabel(self.groupBox_9)
        self.label_43.setObjectName("label_43")
        self.gridLayout_8.addWidget(self.label_43, 5, 0, 1, 1)
        self.horizontalLayout_9.addLayout(self.gridLayout_8)
        self.verticalLayout_8.addWidget(self.groupBox_9)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_6)
        self.verticalLayout_3.setMargin(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_10 = QtGui.QGroupBox(self.tab_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_10.sizePolicy().hasHeightForWidth())
        self.groupBox_10.setSizePolicy(sizePolicy)
        self.groupBox_10.setStyleSheet("None")
        self.groupBox_10.setFlat(True)
        self.groupBox_10.setCheckable(False)
        self.groupBox_10.setObjectName("groupBox_10")
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.groupBox_10)
        self.horizontalLayout_10.setContentsMargins(9, 3, 6, 3)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.importSQL_2 = QtGui.QPlainTextEdit(self.groupBox_10)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importSQL_2.sizePolicy().hasHeightForWidth())
        self.importSQL_2.setSizePolicy(sizePolicy)
        self.importSQL_2.setObjectName("importSQL_2")
        self.horizontalLayout_10.addWidget(self.importSQL_2)
        self.verticalLayout_3.addWidget(self.groupBox_10)
        self.label_44 = QtGui.QLabel(self.tab_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy)
        self.label_44.setCursor(QtCore.Qt.ArrowCursor)
        self.label_44.setTextFormat(QtCore.Qt.RichText)
        self.label_44.setWordWrap(True)
        self.label_44.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_44.setObjectName("label_44")
        self.verticalLayout_3.addWidget(self.label_44)
        self.tabWidget.addTab(self.tab_6, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(RobotDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_11.addWidget(self.pushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.retranslateUi(RobotDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RobotDialog)

    def retranslateUi(self, RobotDialog):
        RobotDialog.setWindowTitle(QtGui.QApplication.translate("RobotDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_6.setTitle(QtGui.QApplication.translate("RobotDialog", "基础设置>>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("RobotDialog", "采集器名称", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("RobotDialog", "延迟（秒）", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("RobotDialog", "最大线程数", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_8.setTitle(QtGui.QApplication.translate("RobotDialog", "列表页设置>>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_30.setText(QtGui.QApplication.translate("RobotDialog", "自动增长", None, QtGui.QApplication.UnicodeUTF8))
        self.label_31.setText(QtGui.QApplication.translate("RobotDialog", "URL:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_32.setText(QtGui.QApplication.translate("RobotDialog", "从:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_33.setText(QtGui.QApplication.translate("RobotDialog", "到:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_34.setText(QtGui.QApplication.translate("RobotDialog", "通配符长度:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_35.setText(QtGui.QApplication.translate("RobotDialog", "说明: 长度不足时，前面补0.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_36.setText(QtGui.QApplication.translate("RobotDialog", "手工输入", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("RobotDialog", "基本信息", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_9.setTitle(QtGui.QApplication.translate("RobotDialog", "采集设置>>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_37.setText(QtGui.QApplication.translate("RobotDialog", "采集页面编码", None, QtGui.QApplication.UnicodeUTF8))
        self.label_38.setText(QtGui.QApplication.translate("RobotDialog", "列表区域识别规则<br/><font color=\'#ACCAEF\'>截取的地方加上：<br/>[list]</font>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_39.setText(QtGui.QApplication.translate("RobotDialog", "文章链接URL识别规则<br/><font color=\'#ACCAEF\'>截取的地方加上：<br/>[url]、[title]</font>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_40.setText(QtGui.QApplication.translate("RobotDialog", "文章标题识别规则<br/><font color=\'#ACCAEF\'>截取的地方加上：<br/>[title]</font>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_41.setText(QtGui.QApplication.translate("RobotDialog", "文章内容识别规则<br/><font color=\'#ACCAEF\'>截取的地方加上：<br/>[message]</font>", None, QtGui.QApplication.UnicodeUTF8))
        self.reverseorder_2.setText(QtGui.QApplication.translate("RobotDialog", "倒序采集", None, QtGui.QApplication.UnicodeUTF8))
        self.onlylinks_2.setText(QtGui.QApplication.translate("RobotDialog", "不采集内容", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadmode_2.setText(QtGui.QApplication.translate("RobotDialog", "下载模式", None, QtGui.QApplication.UnicodeUTF8))
        self.extension_2.setToolTip(QtGui.QApplication.translate("RobotDialog", "文件后缀，仅下载模式有效", None, QtGui.QApplication.UnicodeUTF8))
        self.label_42.setText(QtGui.QApplication.translate("RobotDialog", "修改文件后缀", None, QtGui.QApplication.UnicodeUTF8))
        self.label_43.setText(QtGui.QApplication.translate("RobotDialog", "其它设置", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QtGui.QApplication.translate("RobotDialog", "采集规则", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_10.setTitle(QtGui.QApplication.translate("RobotDialog", "执行SQL语句>>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_44.setText(QtGui.QApplication.translate("RobotDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#accaef;\">注：采集完成后执行设置的SQL语句保存到数据库<br />数据：</span><span style=\" font-style:italic; color:#accaef;\">[taskid], [robotid], [key], [url], [title], [content], [runtime]</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QtGui.QApplication.translate("RobotDialog", "导出设置", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("RobotDialog", "保存", None, QtGui.QApplication.UnicodeUTF8))
