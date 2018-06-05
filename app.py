import pip

try:
    import requests
except ImportError:
    pip.main(['install', 'requests'])
    import requests
from designer import main
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from datetime import time
import sys, os
import datetime
import time
import RPi.GPIO as GPIO
import threading
from time import gmtime, strftime
import savestuff
import qrCode
from defects import defects
from reservations import reservations
from scheduler import Scheduler


class MainUi(QMainWindow, main.Ui_MainWindow):
    def __init__(self, parent=None):
        self.defects = defects()
        self.reservation = reservations()
        self.scheduler = Scheduler()

        self.taken = []

        self.dir = os.path.dirname(__file__)
        self.filename = "C:/Users/kevin/PycharmProjects/Raspberry pi/qr/qr.png"  # uncomment for testing
        self.filename2 = "C:/Users/kevin/PycharmProjects/Raspberry pi/setup.json"
        # self.filename = "/home/pi/RaspberryPi/qr/qr.png"   #uncomment for rpi
        # self.filename2 = "/home/pi/RaspberryPi/setup.json"

        super(MainUi, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

        if os.path.exists(self.filename2) is False:  # ??? not sure why savestuff.check doesnt work
            self.stackedWidget.setCurrentIndex(4)
            savestuff.create()
            self.savebtn.clicked.connect(self.savePress)
            self.room = savestuff.read()
        else:
            self.room = savestuff.read()
            self.stackedWidget.setCurrentIndex(0)
            print(self.room)

        self.selectDict = [self.slot1, self.slot2, self.slot3, self.slot4, self.slot5, self.slot6, self.slot7,
                           self.slot8,
                           self.slot9, self.slot10, self.slot11, self.slot12, self.slot13, self.slot14, self.slot15]

        self.getReservation()

        self.defects.getDefunctTypes(self.defectTypeBox)

        now = datetime.datetime.now()
        self.day = now.day
        self.month = now.month
        self.year = now.year
        self.slot = 1
        self.selectedSlot = 1
        self.maxSlots = 15
        self.lcdSlots.display(self.slot)

        self.passCounter = 0

        thread = threading.Thread(target=self.distanceSensor, args=())
        thread.daemon = True
        thread.start()

        thread2 = threading.Thread(target=self.clock, args=())
        thread2.daemon = True
        thread2.start()

        self.start = 0

    def initUI(self):
        QMainWindow.showFullScreen(self)
        self.scheduleBtn.setToolTip("button 1")
        self.defectsBtn.setToolTip("button 2")
        self.defectsBtn.clicked.connect(self.menuButtons)
        self.defectBack.clicked.connect(self.menuButtons)
        self.generateDefect.clicked.connect(self.menuButtons)
        self.lblCapacity_home.setToolTip("Label 1")
        self.lblTemperature_home.setToolTip("Label 2")
        self.scheduleBtn.clicked.connect(self.menuButtons)
        self.scheduleBack.clicked.connect(self.menuButtons)
        self.generate.clicked.connect(self.menuButtons)
        self.defectsBtn.setText("Defects")
        self.lblCapacity_home.setText("capacity")
        self.lblTemperature_home.setText("temp")

        self.calendarWidget.clicked.connect(self.getReservation)

        self.calendarWidgetSchedule.clicked.connect(self.getSchedule)
        self.slotLeft.clicked.connect(self.scheduleButtons)
        self.slotRight.clicked.connect(self.scheduleButtons)

        self.slot1.clicked.connect(self.radioCheck)
        self.slot2.clicked.connect(self.radioCheck)
        self.slot3.clicked.connect(self.radioCheck)
        self.slot4.clicked.connect(self.radioCheck)
        self.slot5.clicked.connect(self.radioCheck)
        self.slot6.clicked.connect(self.radioCheck)
        self.slot7.clicked.connect(self.radioCheck)
        self.slot8.clicked.connect(self.radioCheck)
        self.slot9.clicked.connect(self.radioCheck)
        self.slot10.clicked.connect(self.radioCheck)
        self.slot11.clicked.connect(self.radioCheck)
        self.slot12.clicked.connect(self.radioCheck)
        self.slot13.clicked.connect(self.radioCheck)
        self.slot14.clicked.connect(self.radioCheck)
        self.slot15.clicked.connect(self.radioCheck)

        self.wakeButton.clicked.connect(self.wakeup)

    def getReservation(self):
        try:
            self.reservation.getReservations(self.room, self.calendarWidget.selectedDate())
        except:
            self.errorScheduleEvent("Failed to retrieve reservations")
        self.setTimeTable()

    def getSchedule(self):
        try:
            self.scheduler.getSchedule(self.room, self.calendarWidgetSchedule.selectedDate(), self.radioButtonGroup)
        except:
            self.errorScheduleEvent("Failed to retrieve bookings")
        self.setSchedulerTable()
        self.maxslots()
        if self.slot > self.maxSlots:
            self.slot = self.maxSlots

    def menuButtons(self):
        sender = self.sender()
        self.resetTime()
        if sender is self.scheduleBtn:
            self.stackedWidget.setCurrentIndex(2)
        elif sender is self.defectsBtn:
            self.defects.getDefects(self.room)
            self.setDefectTable(self.defects.getDefectTableData())
            self.stackedWidget.setCurrentIndex(3)
        elif sender is self.defectBack:
            self.defectQr.clear()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.scheduleBack:
            self.scheduleQr.clear()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.generateDefect:
            qrCode.generateDefectQr(self.filename, self.defectTypeBox.currentText(), self.room)
            pixmap = QPixmap(self.filename)
            self.defectQr.setPixmap(pixmap.scaled(250, 250))
            print("qr set")
        elif sender is self.generate:
            qrCode.generateBookingQr(self.filename, self.calendarWidgetSchedule.selectedDate(), self.selectedSlot,
                                     self.lcdSlots.intValue(), self.room)
            pixmap = QPixmap(self.filename)
            self.scheduleQr.setPixmap(pixmap.scaled(250, 250))
            print("qr set")

    def scheduleButtons(self):
        sender = self.sender()
        self.resetTime()
        self.maxslots()
        if sender is self.slotLeft:
            if self.slot > 1:
                self.slot -= 1
            self.lcdSlots.display(self.slot)
        elif sender is self.slotRight:
            if self.slot < self.maxSlots:
                self.slot += 1
            else:
                self.slot = self.maxSlots
            self.lcdSlots.display(self.slot)


    def radioCheck(self):
        sender = self.sender()
        self.resetTime()
        self.maxslots()
        if sender is self.slot1:
            self.selectedSlot = 1
            self.maxSlots = 15
        elif sender is self.slot2:
            self.selectedSlot = 2
            self.maxSlots = 14
        elif sender is self.slot3:
            self.selectedSlot = 3
            self.maxSlots = 13
        elif sender is self.slot4:
            self.selectedSlot = 4
            self.maxSlots = 12
        elif sender is self.slot5:
            self.selectedSlot = 5
            self.maxSlots = 11
        elif sender is self.slot6:
            self.selectedSlot = 6
            self.maxSlots = 10
        elif sender is self.slot7:
            self.selectedSlot = 7
            self.maxSlots = 9
        elif sender is self.slot8:
            self.selectedSlot = 8
            self.maxSlots = 8
        elif sender is self.slot9:
            self.selectedSlot = 9
            self.maxSlots = 7
        elif sender is self.slot10:
            self.selectedSlot = 10
            self.maxSlots = 6
        elif sender is self.slot11:
            self.selectedSlot = 11
            self.maxSlots = 5
        elif sender is self.slot12:
            self.selectedSlot = 12
            self.maxSlots = 4
        elif sender is self.slot13:
            self.selectedSlot = 13
            self.maxSlots = 3
        elif sender is self.slot14:
            self.selectedSlot = 14
            self.maxSlots = 2
        elif sender is self.slot15:
            self.selectedSlot = 15
            self.maxSlots = 1
        self.maxslots()

    def wakeup(self):
        self.resetTime()
        self.stackedWidget.setCurrentIndex(1)

    def maxslots(self):
        b = False
        c = []
        self.checkDisabledSlots()
        for i in self.taken:
            if i > self.selectedSlot:
                c.append(i)
                b = True
        if b:
            self.maxSlots = min(c) - self.selectedSlot
        if self.slot > self.maxSlots:
            self.slot = self.maxSlots

    def checkDisabledSlots(self):
        q = 1
        self.taken = []
        for i in self.scheduler.getTimeSlotData():
            if i != q:
                self.taken.append(q)
            q += 1

    def distanceSensor(self):
        GPIO.setmode(GPIO.BOARD)
        PIN_TRIGGER = 7
        PIN_ECHO = 11
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        print("Waiting for sensor to settle")
        time.sleep(2)
        print("Calculating distance")
        pulse_start_time = 0
        pulse_end_time = 0
        try:
            while True:
                time.sleep(0.1)
                GPIO.output(PIN_TRIGGER, GPIO.HIGH)
                time.sleep(0.00001)
                GPIO.output(PIN_TRIGGER, GPIO.LOW)
                while GPIO.input(PIN_ECHO) == 0:
                    pulse_start_time = time.time()
                while GPIO.input(PIN_ECHO) == 1:
                    pulse_end_time = time.time()
                pulse_duration = pulse_end_time - pulse_start_time
                distance = round(pulse_duration * 17150, 2)
                self.lblCapacity_home.setText("Distance:" + str(distance) + "cm")
                if distance < 40 and self.stackedWidget.currentIndex() is 0:
                    self.stackedWidget.setCurrentIndex(1)
                    self.start = time.time()
                elif distance < 100 and distance is not 0 and self.stackedWidget.currentIndex() is 0:
                    self.passCounter += 1
                    self.distanceTest.setText(str(self.passCounter))
                    time.sleep(0.8)
                if (time.time()) - self.start > 10 and distance > 80 and self.stackedWidget.currentIndex() is not 4:
                    self.stackedWidget.setCurrentIndex(0)
        finally:
            print('cleaning')
            GPIO.cleanup()

    def clock(self):
        while True:
            time.sleep(1)
            self.wakeButton.setText(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))

    def resetTime(self):
        self.start = time.time()

    def savePress(self):
        savestuff.write(str(self.roomNumTbox.text()))
        self.stackedWidget.setCurrentIndex(0)

    # ----json parse and table fill----

    def setSchedulerTable(self):
        print("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        timeSlotData = self.scheduler.getTimeSlotData()
        j = 0
        for i in self.radioButtonGroup.buttons():
            if timeSlotData[j] != j + 1:
                i.setText(timeSlotData[j])
                i.setEnabled(False)
            j += 1

    def setTimeTable(self):
        model = QStringListModel(self.reservation.getTimeTableData())
        self.listView.setModel(model)

    def setDefectTable(self, data):
        model = QStringListModel(data)
        print(model)
        self.defectListView.setModel(model)

    # -----events
    def errorScheduleEvent(self, string):
        reply = QMessageBox.question(self, 'Message',
                                     "An error has occurred: %s" % string, QMessageBox.Ok)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def closeEvent(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

    # ----debug stuff---Remove later------
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.closeEvent()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()

        text = "x: {0},  y: {1}".format(x, y)
        self.lblCapacity_home.setText(text)

    def buttonClicked(self):
        sender = self.sender()
        if sender is self.scheduleBtn:
            self.lblTemperature_home.setText("scheduleBtn 1")
        elif sender is self.defectsBtn:
            self.lblCapacity_home.setText(sender.text() + ' was pressed')


def main():
    app = QApplication(sys.argv)
    main = MainUi()
    main.show()
    app.exec_()


if __name__ == '__main__':
    main()
