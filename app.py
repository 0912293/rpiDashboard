from designer import main
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from datetime import time
import urllib.request
import json
import qrcode
import sys,os
import datetime
import time
import RPi.GPIO as GPIO
import threading
from time import gmtime, strftime

class MainUi(QMainWindow, main.Ui_MainWindow):
    def __init__(self, parent=None):
        self.jsonData = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        super(MainUi, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.getData()
        self.getTimeTable()

        now = datetime.datetime.now()
        self.day = now.day
        self.month = now.month
        self.year = now.year
        self.slot = 1
        self.selectedSlot = 0
        self.maxSlots = 15
        self.lcdDay.display(self.day)
        self.lcdMonth.display(self.month)
        self.lcdSlots.display(self.slot)

        self.room = "WN4.101"
        self.passCounter = 0

        self.dir = os.path.dirname(__file__)
        #self.filename = "C:/Users/kevin/PycharmProjects/RaspberryPi/qr/qr.png"  # uncomment for testing
        self.filename= "/home/pi/RaspberryPi/qr/qr.png"   #uncomment for rpi
        self.stackedWidget.setCurrentIndex(0)

        thread = threading.Thread(target=self.distanceSensor, args=())
        thread.daemon = True
        thread.start()

        thread2 = threading.Thread(target=self.clock, args=())
        thread2.daemon = True
        thread2.start()

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

        self.monthLeft.clicked.connect(self.scheduleButtons)
        self.monthRight.clicked.connect(self.scheduleButtons)
        self.dayLeft.clicked.connect(self.scheduleButtons)
        self.dayRight.clicked.connect(self.scheduleButtons)
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

    def menuButtons(self):
        sender = self.sender()
        if sender is self.scheduleBtn:
            self.stackedWidget.setCurrentIndex(2)
        elif sender is self.defectsBtn:
            self.stackedWidget.setCurrentIndex(3)
        elif sender is self.defectBack:
            self.defectQr.clear()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.scheduleBack:
            self.scheduleQr.clear()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.generateDefect:
            print("boop")
            self.generateQr(1)
            self.pixmap = QPixmap(self.filename)
            print(self.pixmap)
            self.defectQr.setPixmap(self.pixmap.scaled(250,250))
            print("qr set")
        elif sender is self.generate:
            print("boop")
            self.generateQr(0)
            self.pixmap = QPixmap(self.filename)
            self.scheduleQr.setPixmap(self.pixmap.scaled(250,250))
            print("qr set")

    def scheduleButtons(self):
        sender = self.sender()
        if sender is self.dayLeft:
            if self.day >1:
                self.day -= 1
            self.lcdDay.display(self.day)
        elif sender is self.dayRight:
            if self.day <31:
                self.day += 1
            self.lcdDay.display(self.day)
        elif sender is self.monthLeft:
            if self.month >1:
                self.month -= 1
            self.lcdMonth.display(self.month)
        elif sender is self.monthRight:
            if self.month <12:
                self.month += 1
            self.lcdMonth.display(self.month)
        elif sender is self.slotLeft:
            if self.slot >1:
                self.slot -= 1
            self.lcdSlots.display(self.slot)
        elif sender is self.slotRight:
            if self.slot <self.maxSlots:
                self.slot += 1
            self.lcdSlots.display(self.slot)

    def radioCheck(self):
        sender = self.sender()
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
        self.stackedWidget.setCurrentIndex(1)

    def maxslots(self):
        if self.slot>self.maxSlots:
            self.slot=self.maxSlots
        self.lcdSlots.display(self.slot)

    def generateQr(self,type):
        print(self.filename)
        if type == 0:
            print(self.lcdDay.intValue())
            print(self.lcdMonth.intValue())
            print(self.year)
            print(self.lcdSlots.intValue())
            print(self.selectedSlot)
            print(int(self.selectedSlot)+int(self.lcdSlots.intValue()-1))
            pix = qrcode.make(
                '{"Reservation": {"TimeSlotFrom": %s, "TimeSlotTo": %s, "Date": "%s-%s-%s", "Room": "%s"}}'%(self.selectedSlot,
                                                                                                             int(self.selectedSlot)+int(self.lcdSlots.intValue()-1),
                                                                                                             self.lcdDay.intValue(),self.lcdMonth.intValue(),self.year,self.room))
            pix.save(self.filename)
            print("qr generated")
        elif type == 1:
            pix2 = qrcode.make('{"Defunct": {"Type": "EquipMissing", "Room": "WN4.101"}}')
            pix2.save(self.filename)
            print("qr generated")

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
                self.lblCapacity_home.setText("Distance:"+str(distance)+"cm")
                if distance<200 and self.stackedWidget.currentIndex() is 0:
                    self.stackedWidget.setCurrentIndex(1)
                    start = time.time()
                elif distance<50 and distance is not 0:
                    self.passCounter += 1
                    self.distanceTest.setText(str(self.passCounter))
                    time.sleep(0.5)
                if start-time.time() > 3 and distance>200:
                    self.stackedWidget.setCurrentIndex(0)
        finally:
            print('cleaning')
            GPIO.cleanup()

    def clock(self):
        while True:
            time.sleep(1)
            self.wakeButton.setText(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))

#----json parse and table fill----

    def getData(self):
        contents = urllib.request.urlopen(
            "http://markb.pythonanywhere.com/reservation").read()
        data = json.loads(contents.decode('utf-8'))
        print(json.dumps(data, indent=4, sort_keys=True))
        self.parseData(data)

    def fillEmptyList(self):
        for i in range(15):
            self.jsonData[i] = ("%d Empty"%(i+1))
            print(i+1)

    def enterReservation(self, timeFrom, timeTo, string):
        time=timeFrom-1
        for i in range(time,timeTo):
            self.jsonData[time] = (str(time+1)+string)
            time += 1

    def parseData(self, data):
        self.fillEmptyList()
        for i in data:
            self.enterReservation(int(i["timeslot_from"]), int(i["timeslot_to"])," %s %s %s %s %s"%(str(i["time_from"]),str(i["time_to"]),str(i["room"]),str(i["lesson"]),str(i["username"])))

    def getTimeTable(self):
        model = QStringListModel(self.jsonData)
        self.listView.setModel(model)

#-----upon close event
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

#----debug stuff---Remove later------
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
#------END--of--debug stuff---


def main():
    app = QApplication(sys.argv)
    main = MainUi()
    main.show()
    app.exec_()


if __name__ == '__main__':
    main()
