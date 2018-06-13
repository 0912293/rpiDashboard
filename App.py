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
import sys
import os
import datetime
import time
import RPi.GPIO as GPIO
import threading
from time import gmtime, strftime
import SaveStuff
import qrCode
from Defects import Defects
from Reservations import Reservations
from Scheduler import Scheduler
from Db import Db
from ScheduledBackUp import ScheduledBackUp


class MainUi(QMainWindow, main.Ui_MainWindow):
    def __init__(self, parent=None):
        self.defects = Defects()
        self.reservation = Reservations()
        self.scheduler = Scheduler()
        self.db = Db()
        self.schedulebackup = ScheduledBackUp()

        if not SaveStuff.check('db.sqlite'):
            self.db.create()

        self.taken = []

        self.dir = os.path.dirname(__file__)
        self.config = "C:/Users/kevin/PycharmProjects/Raspberry pi/setup.json"  # uncomment for testing
        # self.config = "/home/pi/RaspberryPi/setup.json"  # uncomment for rpi
        self.qr_pic = "C:/Users/kevin/PycharmProjects/Raspberry pi/qr/qr.png"  # uncomment for testing
        # self.qr_pic = "/home/pi/RaspberryPi/qr/qr.png"   # uncomment for rpi
        self.backup_schedule = "C:/Users/kevin/PycharmProjects/Raspberry pi/schedule"  # uncomment for testing
        # self.backup_schedule = "/home/pi/RaspberryPi/schedule.json"  # uncomment for rpi

        super(MainUi, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()

        if not SaveStuff.check(self.config):
            self.stackedWidget.setCurrentIndex(4)
            SaveStuff.create(self.config)
            self.savebtn.clicked.connect(self.save_press)
            self.room = SaveStuff.read(self.config)['room']
        else:
            self.room = SaveStuff.read(self.config)['room']
            self.stackedWidget.setCurrentIndex(0)
            print(self.room)

        self.selectDict = [self.slot1, self.slot2, self.slot3, self.slot4, self.slot5, self.slot6, self.slot7,
                           self.slot8,
                           self.slot9, self.slot10, self.slot11, self.slot12, self.slot13, self.slot14, self.slot15]

        self.get_reservation()

        self.defects.get_defunct_types(self.defectTypeBox)

        now = datetime.datetime.now()
        self.day = now.day
        self.month = now.month
        self.year = now.year
        self.slot = 1
        self.selectedSlot = 1
        self.maxSlots = 15
        self.lcdSlots.display(self.slot)

        self.passCounter = 0

        thread = threading.Thread(target=self.distance_sensor, args=())
        thread.daemon = True
        thread.start()

        thread2 = threading.Thread(target=self.clock, args=())
        thread2.daemon = True
        thread2.start()

        SaveStuff.create(self.backup_schedule+".json")
        SaveStuff.write({"week": datetime.date(self.year, self.month, self.day).isocalendar()[1]},
                        self.backup_schedule+".json")
        self.schedulebackup.update_schedule(self.room, self.backup_schedule)

        self.start = 0

    def init_ui(self):
        QMainWindow.showFullScreen(self)
        self.scheduleBtn.setToolTip("button 1")
        self.defectsBtn.setToolTip("button 2")
        self.defectsBtn.clicked.connect(self.menu_buttons)
        self.defectBack.clicked.connect(self.menu_buttons)
        self.generateDefect.clicked.connect(self.menu_buttons)
        self.lblCapacity_home.setToolTip("Label 1")
        self.lblTemperature_home.setToolTip("Label 2")
        self.scheduleBtn.clicked.connect(self.menu_buttons)
        self.scheduleBack.clicked.connect(self.menu_buttons)
        self.generate.clicked.connect(self.menu_buttons)
        self.defectsBtn.setText("Defects")
        self.lblCapacity_home.setText("capacity")
        self.lblTemperature_home.setText("temp")

        self.calendarWidget.clicked.connect(self.get_reservation)

        self.calendarWidgetSchedule.clicked.connect(self.get_schedule)
        self.slotLeft.clicked.connect(self.schedule_buttons)
        self.slotRight.clicked.connect(self.schedule_buttons)

        self.slot1.clicked.connect(self.radio_check)
        self.slot2.clicked.connect(self.radio_check)
        self.slot3.clicked.connect(self.radio_check)
        self.slot4.clicked.connect(self.radio_check)
        self.slot5.clicked.connect(self.radio_check)
        self.slot6.clicked.connect(self.radio_check)
        self.slot7.clicked.connect(self.radio_check)
        self.slot8.clicked.connect(self.radio_check)
        self.slot9.clicked.connect(self.radio_check)
        self.slot10.clicked.connect(self.radio_check)
        self.slot11.clicked.connect(self.radio_check)
        self.slot12.clicked.connect(self.radio_check)
        self.slot13.clicked.connect(self.radio_check)
        self.slot14.clicked.connect(self.radio_check)
        self.slot15.clicked.connect(self.radio_check)

        self.wakeButton.clicked.connect(self.wakeup)

    def get_reservation(self):
        # try:
        self.reservation.get_reservations(self.room, self.calendarWidget.selectedDate())
        # except:
        #     self.error_schedule_event("Failed to retrieve reservations")
        self.set_time_table()

    def get_schedule(self):
        try:
            self.scheduler.get_schedule(self.room, self.calendarWidgetSchedule.selectedDate(), self.radioButtonGroup)
        except:
            self.error_schedule_event("Failed to retrieve bookings")
        self.set_scheduler_table()
        self.slot = 0
        self.maxSlots = 10
        self.max_slots()
        if self.slot > self.maxSlots:
            self.slot = self.maxSlots

    def menu_buttons(self):
        sender = self.sender()
        self.reset_time()
        if sender is self.scheduleBtn:
            self.stackedWidget.setCurrentIndex(2)
        elif sender is self.defectsBtn:
            self.defects.get_defects(self.room)
            self.set_defect_table(self.defects.get_defect_table_data())
            self.stackedWidget.setCurrentIndex(3)
        elif sender is self.defectBack:
            self.defectQr.clear()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.scheduleBack:
            self.scheduleQr.clear()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.generateDefect:
            qrCode.generate_defect_qr(self.qr_pic, self.defectTypeBox.currentText(), self.room)
            pixmap = QPixmap(self.qr_pic)
            self.defectQr.setPixmap(pixmap.scaled(250, 250))
            print("qr set")
        elif sender is self.generate:
            qrCode.generate_booking_qr(self.qr_pic, self.calendarWidgetSchedule.selectedDate(), self.selectedSlot,
                                       self.lcdSlots.intValue(), self.room)
            pixmap = QPixmap(self.qr_pic)
            self.scheduleQr.setPixmap(pixmap.scaled(250, 250))
            print("qr set")

    def schedule_buttons(self):
        sender = self.sender()
        self.reset_time()
        self.max_slots()
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

    def radio_check(self):
        sender = self.sender()
        self.reset_time()
        self.max_slots()
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
        self.max_slots()

    def wakeup(self):
        self.reset_time()
        self.stackedWidget.setCurrentIndex(1)

    def max_slots(self):
        b = False
        c = []
        self.check_disabled_slots()
        for i in self.taken:
            if i > self.selectedSlot:
                c.append(i)
                b = True
        if b:
            self.maxSlots = min(c) - self.selectedSlot
        if self.slot > self.maxSlots:
            self.slot = self.maxSlots

    def check_disabled_slots(self):
        q = 1
        self.taken = []
        for i in self.scheduler.get_time_slot_data():
            if i != q:
                self.taken.append(q)
            q += 1

    def distance_sensor(self):
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
                if (time.time()) - self.start > 10 and distance > 100 and self.stackedWidget.currentIndex() is not 4:
                    self.stackedWidget.setCurrentIndex(0)
        finally:
            print('cleaning')
            GPIO.cleanup()

    def clock(self):
        while True:
            time.sleep(1)
            self.wakeButton.setText(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))

    def reset_time(self):
        self.start = time.time()

    def save_press(self):
        data = {'room': str(self.roomNumTbox.text())}
        SaveStuff.write(data, self.config)
        self.stackedWidget.setCurrentIndex(0)

    # ----json parse and table fill----

    def set_scheduler_table(self):
        print("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        time_slot_data = self.scheduler.get_time_slot_data()
        j = 0
        for i in self.radioButtonGroup.buttons():
            if time_slot_data[j] != j + 1:
                i.setText(time_slot_data[j])
                i.setEnabled(False)
            j += 1

    def set_time_table(self):
        model = QStringListModel(self.reservation.get_time_table_data())
        self.listView.setModel(model)

    def set_defect_table(self, data):
        model = QStringListModel(data)
        print(model)
        self.defectListView.setModel(model)

    # -----events
    def error_schedule_event(self, string):
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

    def button_clicked(self):
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
