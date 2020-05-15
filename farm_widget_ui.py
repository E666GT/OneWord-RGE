# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'farm_widget_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FarmWidget(object):
    def setupUi(self, FarmWidget):
        FarmWidget.setObjectName("FarmWidget")
        FarmWidget.resize(1681, 901)
        self.FarmIntroGroupBox = QtWidgets.QGroupBox(FarmWidget)
        self.FarmIntroGroupBox.setGeometry(QtCore.QRect(20, 10, 1621, 161))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(16)
        self.FarmIntroGroupBox.setFont(font)
        self.FarmIntroGroupBox.setObjectName("FarmIntroGroupBox")
        self.DebugLabel = QtWidgets.QLabel(self.FarmIntroGroupBox)
        self.DebugLabel.setGeometry(QtCore.QRect(20, 30, 401, 111))
        self.DebugLabel.setObjectName("DebugLabel")
        self.GoMainWindowButton = QtWidgets.QPushButton(self.FarmIntroGroupBox)
        self.GoMainWindowButton.setGeometry(QtCore.QRect(410, 20, 131, 51))
        self.GoMainWindowButton.setObjectName("GoMainWindowButton")
        self.FarmInfotextBrowser = QtWidgets.QTextBrowser(self.FarmIntroGroupBox)
        self.FarmInfotextBrowser.setGeometry(QtCore.QRect(550, 20, 1061, 141))
        self.FarmInfotextBrowser.setObjectName("FarmInfotextBrowser")
        self.FarmInfoUpdatepushButton = QtWidgets.QPushButton(self.FarmIntroGroupBox)
        self.FarmInfoUpdatepushButton.setGeometry(QtCore.QRect(1520, 130, 75, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.FarmInfoUpdatepushButton.setFont(font)
        self.FarmInfoUpdatepushButton.setObjectName("FarmInfoUpdatepushButton")
        self.FarmDetailGroupBox = QtWidgets.QGroupBox(FarmWidget)
        self.FarmDetailGroupBox.setGeometry(QtCore.QRect(20, 180, 1621, 711))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(16)
        self.FarmDetailGroupBox.setFont(font)
        self.FarmDetailGroupBox.setObjectName("FarmDetailGroupBox")
        self.FarmDetailScrollArea = QtWidgets.QScrollArea(self.FarmDetailGroupBox)
        self.FarmDetailScrollArea.setGeometry(QtCore.QRect(10, 30, 1601, 681))
        self.FarmDetailScrollArea.setWidgetResizable(True)
        self.FarmDetailScrollArea.setObjectName("FarmDetailScrollArea")
        self.FarmDetailScrollAreaContents = QtWidgets.QWidget()
        self.FarmDetailScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 1582, 5000))
        self.FarmDetailScrollAreaContents.setMinimumSize(QtCore.QSize(0, 5000))
        self.FarmDetailScrollAreaContents.setObjectName("FarmDetailScrollAreaContents")
        self.gridLayoutWidget = QtWidgets.QWidget(self.FarmDetailScrollAreaContents)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1581, 631))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.FarmDetailScrollAreaGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.FarmDetailScrollAreaGridLayout.setContentsMargins(0, 0, 0, 0)
        self.FarmDetailScrollAreaGridLayout.setObjectName("FarmDetailScrollAreaGridLayout")
        self.FarmDetailScrollArea.setWidget(self.FarmDetailScrollAreaContents)
        self.FreshFarmButton = QtWidgets.QPushButton(FarmWidget)
        self.FreshFarmButton.setGeometry(QtCore.QRect(120, 170, 75, 25))
        self.FreshFarmButton.setObjectName("FreshFarmButton")
        self.FreshFarmByHealthOrderButton = QtWidgets.QPushButton(FarmWidget)
        self.FreshFarmByHealthOrderButton.setGeometry(QtCore.QRect(210, 170, 75, 25))
        self.FreshFarmByHealthOrderButton.setObjectName("FreshFarmByHealthOrderButton")

        self.retranslateUi(FarmWidget)
        QtCore.QMetaObject.connectSlotsByName(FarmWidget)

    def retranslateUi(self, FarmWidget):
        _translate = QtCore.QCoreApplication.translate
        FarmWidget.setWindowTitle(_translate("FarmWidget", "Form"))
        self.FarmIntroGroupBox.setTitle(_translate("FarmWidget", "介绍"))
        self.DebugLabel.setText(_translate("FarmWidget", "欢迎回到你的单词农场！不要荒废哦~"))
        self.GoMainWindowButton.setText(_translate("FarmWidget", "浇水去！"))
        self.FarmInfoUpdatepushButton.setText(_translate("FarmWidget", "刷新数据"))
        self.FarmDetailGroupBox.setTitle(_translate("FarmWidget", "农场"))
        self.FreshFarmButton.setText(_translate("FarmWidget", "刷新健康"))
        self.FreshFarmByHealthOrderButton.setText(_translate("FarmWidget", "按健康排序"))
