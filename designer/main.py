# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, -20, 1921, 1061))
        self.stackedWidget.setObjectName("stackedWidget")
        self.sleep = QtWidgets.QWidget()
        self.sleep.setObjectName("sleep")
        self.wakeButton = QtWidgets.QPushButton(self.sleep)
        self.wakeButton.setGeometry(QtCore.QRect(0, 10, 1921, 1041))
        self.wakeButton.setObjectName("wakeButton")
        self.stackedWidget.addWidget(self.sleep)
        self.home = QtWidgets.QWidget()
        self.home.setObjectName("home")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.home)
        self.calendarWidget.setGeometry(QtCore.QRect(731, 20, 1181, 681))
        self.calendarWidget.setObjectName("calendarWidget")
        self.scheduleBtn = QtWidgets.QPushButton(self.home)
        self.scheduleBtn.setGeometry(QtCore.QRect(730, 720, 491, 341))
        self.scheduleBtn.setObjectName("scheduleBtn")
        self.defectsBtn = QtWidgets.QPushButton(self.home)
        self.defectsBtn.setGeometry(QtCore.QRect(1420, 720, 491, 341))
        self.defectsBtn.setObjectName("defectsBtn")
        self.lblCapacity_home = QtWidgets.QLabel(self.home)
        self.lblCapacity_home.setGeometry(QtCore.QRect(1250, 740, 141, 31))
        self.lblCapacity_home.setObjectName("lblCapacity_home")
        self.lblTemperature_home = QtWidgets.QLabel(self.home)
        self.lblTemperature_home.setGeometry(QtCore.QRect(1250, 930, 141, 31))
        self.lblTemperature_home.setObjectName("lblTemperature_home")
        self.listView = QtWidgets.QListView(self.home)
        self.listView.setGeometry(QtCore.QRect(0, 20, 701, 1041))
        self.listView.setObjectName("listView")
        self.stackedWidget.addWidget(self.home)
        self.schedule = QtWidgets.QWidget()
        self.schedule.setObjectName("schedule")
        self.generate = QtWidgets.QPushButton(self.schedule)
        self.generate.setGeometry(QtCore.QRect(730, 720, 491, 341))
        self.generate.setObjectName("generate")
        self.scheduleQr = QtWidgets.QLabel(self.schedule)
        self.scheduleQr.setGeometry(QtCore.QRect(1200, 340, 500, 500))
        self.scheduleQr.setObjectName("scheduleQr")
        self.scheduleBack = QtWidgets.QPushButton(self.schedule)
        self.scheduleBack.setGeometry(QtCore.QRect(1420, 720, 491, 341))
        self.scheduleBack.setObjectName("scheduleBack")
        self.lblCapacity = QtWidgets.QLabel(self.schedule)
        self.lblCapacity.setGeometry(QtCore.QRect(1250, 740, 141, 41))
        self.lblCapacity.setObjectName("lblCapacity")
        self.lblTemperature = QtWidgets.QLabel(self.schedule)
        self.lblTemperature.setGeometry(QtCore.QRect(1250, 930, 131, 41))
        self.lblTemperature.setObjectName("lblTemperature")
        self.lcdDay = QtWidgets.QLCDNumber(self.schedule)
        self.lcdDay.setGeometry(QtCore.QRect(760, 70, 411, 201))
        self.lcdDay.setObjectName("lcdDay")
        self.lblDay = QtWidgets.QLabel(self.schedule)
        self.lblDay.setGeometry(QtCore.QRect(910, 30, 91, 31))
        self.lblDay.setObjectName("lblDay")
        self.lcdMonth = QtWidgets.QLCDNumber(self.schedule)
        self.lcdMonth.setGeometry(QtCore.QRect(1480, 70, 411, 201))
        self.lcdMonth.setObjectName("lcdMonth")
        self.lblMonth = QtWidgets.QLabel(self.schedule)
        self.lblMonth.setGeometry(QtCore.QRect(1640, 30, 91, 31))
        self.lblMonth.setObjectName("lblMonth")
        self.dayLeft = QtWidgets.QPushButton(self.schedule)
        self.dayLeft.setGeometry(QtCore.QRect(750, 300, 131, 171))
        self.dayLeft.setObjectName("dayLeft")
        self.monthLeft = QtWidgets.QPushButton(self.schedule)
        self.monthLeft.setGeometry(QtCore.QRect(1490, 300, 131, 171))
        self.monthLeft.setObjectName("monthLeft")
        self.dayRight = QtWidgets.QPushButton(self.schedule)
        self.dayRight.setGeometry(QtCore.QRect(1030, 300, 131, 171))
        self.dayRight.setObjectName("dayRight")
        self.monthRight = QtWidgets.QPushButton(self.schedule)
        self.monthRight.setGeometry(QtCore.QRect(1770, 300, 131, 171))
        self.monthRight.setObjectName("monthRight")
        self.lblSlots = QtWidgets.QLabel(self.schedule)
        self.lblSlots.setGeometry(QtCore.QRect(1280, 10, 300, 140))
        self.lblSlots.setObjectName("lblSlots")
        self.lcdSlots = QtWidgets.QLCDNumber(self.schedule)
        self.lcdSlots.setGeometry(QtCore.QRect(1175, 100, 300, 140))
        self.lcdSlots.setObjectName("lcdSlots")
        self.slotRight = QtWidgets.QPushButton(self.schedule)
        self.slotRight.setGeometry(QtCore.QRect(1330, 300, 131, 171))
        self.slotRight.setObjectName("slotRight")
        self.slotLeft = QtWidgets.QPushButton(self.schedule)
        self.slotLeft.setGeometry(QtCore.QRect(1200, 300, 131, 171))
        self.slotLeft.setObjectName("slotLeft")
        self.slot1 = QtWidgets.QRadioButton(self.schedule)
        self.slot1.setGeometry(QtCore.QRect(20, 40, 561, 50))
        self.slot1.setObjectName("slot1")
        self.slot1.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot1.setChecked(True)
        self.slot2 = QtWidgets.QRadioButton(self.schedule)
        self.slot2.setGeometry(QtCore.QRect(20, 100, 561, 50))
        self.slot2.setObjectName("slot2")
        self.slot2.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot3 = QtWidgets.QRadioButton(self.schedule)
        self.slot3.setGeometry(QtCore.QRect(20, 160, 561, 50))
        self.slot3.setObjectName("slot3")
        self.slot3.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot4 = QtWidgets.QRadioButton(self.schedule)
        self.slot4.setGeometry(QtCore.QRect(20, 220, 561, 50))
        self.slot4.setObjectName("slot4")
        self.slot4.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot5 = QtWidgets.QRadioButton(self.schedule)
        self.slot5.setGeometry(QtCore.QRect(20, 280, 561, 50))
        self.slot5.setObjectName("slot5")
        self.slot5.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot6 = QtWidgets.QRadioButton(self.schedule)
        self.slot6.setGeometry(QtCore.QRect(20, 340, 561, 50))
        self.slot6.setObjectName("slot6")
        self.slot6.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot7 = QtWidgets.QRadioButton(self.schedule)
        self.slot7.setGeometry(QtCore.QRect(20, 400, 561, 50))
        self.slot7.setObjectName("slot7")
        self.slot7.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot8 = QtWidgets.QRadioButton(self.schedule)
        self.slot8.setGeometry(QtCore.QRect(20, 460, 561, 50))
        self.slot8.setObjectName("slot8")
        self.slot8.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot9 = QtWidgets.QRadioButton(self.schedule)
        self.slot9.setGeometry(QtCore.QRect(20, 520, 561, 50))
        self.slot9.setObjectName("slot9")
        self.slot9.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot10 = QtWidgets.QRadioButton(self.schedule)
        self.slot10.setGeometry(QtCore.QRect(20, 580, 561, 50))
        self.slot10.setObjectName("slot10")
        self.slot10.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot11 = QtWidgets.QRadioButton(self.schedule)
        self.slot11.setGeometry(QtCore.QRect(20, 640, 561, 50))
        self.slot11.setObjectName("slot11")
        self.slot11.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot12 = QtWidgets.QRadioButton(self.schedule)
        self.slot12.setGeometry(QtCore.QRect(20, 700, 561, 50))
        self.slot12.setObjectName("slot12")
        self.slot12.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot13 = QtWidgets.QRadioButton(self.schedule)
        self.slot13.setGeometry(QtCore.QRect(20, 760, 561, 50))
        self.slot13.setObjectName("slot13")
        self.slot13.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot14 = QtWidgets.QRadioButton(self.schedule)
        self.slot14.setGeometry(QtCore.QRect(20, 820, 561, 50))
        self.slot14.setObjectName("slot14")
        self.slot14.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot15 = QtWidgets.QRadioButton(self.schedule)
        self.slot15.setGeometry(QtCore.QRect(20, 880, 561, 50))
        self.slot15.setStyleSheet("QRadioButton::indicator { width: 50px; height: 50px;}")
        self.slot15.setObjectName("slot15")
        self.stackedWidget.addWidget(self.schedule)
        self.defect = QtWidgets.QWidget()
        self.defect.setObjectName("defect")
        self.defectQr = QtWidgets.QLabel(self.defect)
        self.defectQr.setGeometry(QtCore.QRect(1200, 340, 500, 500))
        self.defectQr.setObjectName("defectQr")
        self.defectBack = QtWidgets.QPushButton(self.defect)
        self.defectBack.setGeometry(QtCore.QRect(1420, 720, 491, 341))
        self.defectBack.setObjectName("defectBack")
        self.generateDefect = QtWidgets.QPushButton(self.defect)
        self.generateDefect.setGeometry(QtCore.QRect(730, 720, 491, 341))
        self.generateDefect.setObjectName("generateDefect")
        self.listView_2 = QtWidgets.QListView(self.defect)
        self.listView_2.setGeometry(QtCore.QRect(0, 20, 701, 1041))
        self.listView_2.setObjectName("listView_2")
        self.stackedWidget.addWidget(self.defect)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.scheduleQr.setText(_translate("MainWindow", "QR Placeholder"))
        self.defectQr.setText(_translate("MainWindow", "QR Placeholder"))
        self.wakeButton.setText(_translate("MainWindow", "Time Placeholder"))
        self.scheduleBtn.setText(_translate("MainWindow", "Schedule"))
        self.defectsBtn.setText(_translate("MainWindow", "Defects"))
        self.lblSlots.setText(_translate("MainWindow", "Slots"))
        self.lblCapacity_home.setText(_translate("MainWindow", "Capacity Placeholder"))
        self.lblTemperature_home.setText(_translate("MainWindow", "Temperature Placeholder"))
        self.generate.setText(_translate("MainWindow", "Generate"))
        self.scheduleBack.setText(_translate("MainWindow", "Back"))
        self.lblCapacity.setText(_translate("MainWindow", "Capacity Placeholder"))
        self.lblTemperature.setText(_translate("MainWindow", "Temperature Placeholder"))
        self.lblDay.setText(_translate("MainWindow", "Day"))
        self.lblMonth.setText(_translate("MainWindow", "Month"))
        self.dayLeft.setText(_translate("MainWindow", "<"))
        self.monthLeft.setText(_translate("MainWindow", "<"))
        self.slotLeft.setText(_translate("MainWindow", "<"))
        self.dayRight.setText(_translate("MainWindow", ">"))
        self.monthRight.setText(_translate("MainWindow", ">"))
        self.slotRight.setText(_translate("MainWindow", ">"))
        self.slot1.setText(_translate("MainWindow", "slot 1"))
        self.slot2.setText(_translate("MainWindow", "slot 2"))
        self.slot3.setText(_translate("MainWindow", "slot 3"))
        self.slot4.setText(_translate("MainWindow", "slot 4"))
        self.slot5.setText(_translate("MainWindow", "slot 5"))
        self.slot6.setText(_translate("MainWindow", "slot 6"))
        self.slot7.setText(_translate("MainWindow", "slot 7"))
        self.slot8.setText(_translate("MainWindow", "slot 8"))
        self.slot9.setText(_translate("MainWindow", "slot 9"))
        self.slot10.setText(_translate("MainWindow", "slot 10"))
        self.slot11.setText(_translate("MainWindow", "slot 11"))
        self.slot12.setText(_translate("MainWindow", "slot 12"))
        self.slot13.setText(_translate("MainWindow", "slot 13"))
        self.slot14.setText(_translate("MainWindow", "slot 14"))
        self.slot15.setText(_translate("MainWindow", "slot 15"))
        self.defectBack.setText(_translate("MainWindow", "Back"))
        self.generateDefect.setText(_translate("MainWindow", "Generate"))

