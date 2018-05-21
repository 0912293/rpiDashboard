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
import urllib.request
import json
import qrcode
import sys,os
import datetime
import time
import RPi.GPIO as GPIO
import threading
from time import gmtime, strftime
import savestuff

class MainUi(QMainWindow, main.Ui_MainWindow):
    def __init__(self, parent=None):
        self.timeTableData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.defectTableData = []
        self.dir = os.path.dirname(__file__)
        self.filename = "C:/Users/kevin/PycharmProjects/Raspberry pi/qr/qr.png"  # uncomment for testing
        self.filename2 = "C:/Users/kevin/PycharmProjects/Raspberry pi/setup.json"
        #self.filename = "/home/pi/RaspberryPi/qr/qr.png"   #uncomment for rpi
        #self.filename2 = "/home/pi/RaspberryPi/setup.json"


        super(MainUi, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

        if os.path.exists(self.filename2) is False:     # ??? not sure why savestuff.check doesnt work
            self.stackedWidget.setCurrentIndex(4)
            savestuff.create()
            self.savebtn.clicked.connect(self.savePress)
            self.room = savestuff.read()
        else:
            self.room = savestuff.read()
            self.stackedWidget.setCurrentIndex(0)
            print(self.room)

        self.fillEmptyList()
        self.getSchedule()
        self.setTimeTable()


        now = datetime.datetime.now()
        self.day = now.day
        self.month = now.month
        self.year = now.year
        self.slot = 1
        self.selectedSlot = 1
        self.maxSlots = 15
        self.lcdDay.display(self.day)
        self.lcdMonth.display(self.month)
        self.lcdSlots.display(self.slot)

        self.passCounter = 0

        thread = threading.Thread(target=self.distanceSensor, args=())
        thread.daemon = True
        thread.start()

        thread2 = threading.Thread(target=self.clock, args=())
        thread2.daemon = True
        thread2.start()

        self.start = 0

        self.getDefunctTypes()



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

        self.calendarWidget.clicked.connect(self.getSchedule)

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
        self.resetTime()
        if sender is self.scheduleBtn:
            self.stackedWidget.setCurrentIndex(2)
        elif sender is self.defectsBtn:
            self.getDefects()
            self.setDefectTable()
            self.stackedWidget.setCurrentIndex(3)
        elif sender is self.defectBack:
            self.defectQr.clear()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.scheduleBack:
            self.scheduleQr.clear()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.generateDefect:
            self.generateQr(1)
            self.pixmap = QPixmap(self.filename)
            print(self.pixmap)
            self.defectQr.setPixmap(self.pixmap.scaled(250,250))
            print("qr set")
        elif sender is self.generate:
            self.generateQr(0)
            self.pixmap = QPixmap(self.filename)
            self.scheduleQr.setPixmap(self.pixmap.scaled(250,250))
            print("qr set")

    def scheduleButtons(self):
        sender = self.sender()
        self.resetTime()
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
        self.getReservations()

    def updateScheduler(self):
        self.getSchedule()

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
        if self.slot>self.maxSlots:
            self.slot=self.maxSlots
        self.lcdSlots.display(self.slot)

    def generateQr(self,type):
        print(self.filename+'qr/qr.png')
        if type == 0:
            print(self.lcdDay.intValue())
            print(self.lcdMonth.intValue())
            print(self.year)
            print(self.lcdSlots.intValue())
            print(self.selectedSlot)
            print(int(self.selectedSlot)+int(self.lcdSlots.intValue()-1))
            pix = qrcode.make(
                '{"reservation": {"timeslotfrom": %s, "timeslotto": %s, "date": "%s-%s-%s", "room": "%s"}}' % (self.selectedSlot,
                                                                                                             int(self.selectedSlot)+int(self.lcdSlots.intValue()-1),
                                                                                                               self.lcdDay.intValue(),self.lcdMonth.intValue(),self.year,self.room))
            pix.save(self.filename)
            print("qr generated")
        elif type == 1:
            pix2 = qrcode.make('{"defunct": {"type": "%s", "room": "%s"}}' % (self.defectTypeBox.currentText(), self.room))
            pix2.save(self.filename)
            print("qr generated")

    def getDefunctTypes(self):
        self.defectTypeBox.addItem("notype")
        self.defectTypeBox.addItem("type 1")
        self.defectTypeBox.addItem("type 2")
        self.defectTypeBox.addItem("type 3")

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
                if distance<40 and self.stackedWidget.currentIndex() is 0:
                    self.stackedWidget.setCurrentIndex(1)
                    self.start = time.time()
                elif distance<100 and distance is not 0 and self.stackedWidget.currentIndex() is 0:
                    self.passCounter += 1
                    self.distanceTest.setText(str(self.passCounter))
                    time.sleep(0.8)
                if (time.time())-self.start > 10 and distance > 80 and self.stackedWidget.currentIndex() is not 4:
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

#----json parse and table fill----

    def getReservations(self):
        date = self.day + self.month
        self.getData(date, "http://markb.pythonanywhere.com/reservation/", 2)

    def getSchedule(self):
        self.fillEmptyList()
        date = self.calendarWidget.selectedDate()
        print("get schedule, calendar clicked")
        week = datetime.date(date.year(),date.month(),date.day()).isocalendar()[1]
        self.getData(week, "http://markb.pythonanywhere.com/bookingbyroom/", 0,date)
        self.setTimeTable()

    def getData(self, week, url, type, date):
        body = None
        if type == 0:
            body = {"room":self.room,"weeknummer": week}
        elif type == 1:
            body = {"room":self.room}
        elif type == 2:
            body = {"room":self.room,"weeknummer":week}
        try:
            r = requests.post(url, json=body)
            print('print response')
            text = r.content
            print(text)
            print("\n###########\n")
            data = json.loads(text)
            print(json.dumps(data, indent=4, sort_keys=True))
            self.parseData(data,type,date)
        except:
            self.parseData({},type=10)

    def getDefects(self):
        self.getData(datetime.datetime.now(), "http://markb.pythonanywhere.com/roomdefuncts/", 1,datetime)


    def fillEmptyList(self):
        for i in range(15):
            self.timeTableData[i] = ("%d Empty" % (i + 1))
            print(i+1)

    def enterReservation(self, timeFrom, timeTo, string):
        time=timeFrom-1
        for i in range(time,timeTo):
            self.timeTableData[time] = (str(time + 1) + string)
            time += 1

    def enterDefects(self, description, handled, type):
        self.defectTableData.append(str(type)+": "+str(description)+". Handled:"+str(handled))

    def parseData(self, data, type, date):
        if type == 0:
            for i in data:
                print("printing day:")
                print(i["fields"]["date"][3:5] +" or "+ i["fields"]["date"][-2:]+" or "+
                        i["fields"]["date"][-1:] +" or "+ i["fields"]["date"][4:5])
                print(str(date.day()))
                print(i["fields"]["date"][3:5] == str(date.day()) or i["fields"]["date"][-2:] == str(date.day()) or
                        i["fields"]["date"][-1:] == str(date.day()) or i["fields"]["date"][4:5] == str(date.day()))
                                                                                                                                #TODO change if statement once db is fixed and only uses 1 date format
                if i["fields"]["date"][3:5] == str(date.day()) or i["fields"]["date"][-2:] == str(date.day()) or \
                        i["fields"]["date"][-1:] == str(date.day()) or i["fields"]["date"][4:5] == str(date.day()):
                    self.enterReservation(int(i["fields"]["timeslotfrom"]), int(i["fields"]["timeslotto"]),
                                      " %s %s %s %s %s"%(str(i["fields"]["timefrom"]),str(i["fields"]["timeto"]),
                                                         str(i["fields"]["room"]),str(i["fields"]["lesson"]),
                                                         str(i["fields"]["username"])))
        elif type == 1:
            for i in data:
                self.enterDefects(i["fields"]["description"],i["fields"]["handled"],i["fields"]["type"])
        elif type == 2:
            print("2")
            #self.updateScheduler()
        elif type == 10:
            self.enterReservation(0,10,"error has occured")
            self.errorScheduleEvent("type %s" % type)


    def updateScheduler(self):
        print("Waiting for implementation somewhere else")  # waiting for api to give back schedule for selected day

    def setTimeTable(self):
        model = QStringListModel(self.timeTableData)
        self.listView.setModel(model)

    def setDefectTable(self):
        model = QStringListModel(self.defectTableData)
        print(model)
        self.defectListView.setModel(model)

#-----events
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
