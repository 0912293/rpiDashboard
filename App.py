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
import strings


class MainUi(QMainWindow, main.Ui_MainWindow):
    def __init__(self, parent=None):
        self.defects = Defects()
        self.reservation = Reservations()
        self.scheduler = Scheduler()
        self.db = Db()
        self.schedule_backup = ScheduledBackUp()

        self.taken = []

        super(MainUi, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()

        if not SaveStuff.check(strings.f_config):  # H.3.403
            self.stackedWidget.setCurrentIndex(4)
            SaveStuff.create(strings.f_config)
            self.savebtn.clicked.connect(self.save_press)
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.get_reservation()

        self.get_reservation()

        self.defects.get_defunct_types(self.defectTypeBox)

        self.slot = 1
        self.selectedSlot = 1
        self.maxSlots = 15
        self.lcdSlots.display(self.slot)

        self.passCounter = 0

        thread = threading.Thread(target=self.distance_sensor)
        thread.daemon = True
        thread.start()

        thread2 = threading.Thread(target=self.clock)
        thread2.daemon = True
        thread2.start()

        thread3 = threading.Thread(target=self.backup_schedule)
        thread3.daemon = True
        thread3.start()

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
        self.reservation.get_reservations(SaveStuff.read(strings.f_config)['room'], self.calendarWidget.selectedDate())
        self.set_time_table()

    def get_schedule(self):
        try:
            self.scheduler.get_schedule(SaveStuff.read(strings.f_config)['room'], self.calendarWidgetSchedule.selectedDate(), self.radioButtonGroup)
        except:
            self.error_schedule_event("Failed to retrieve bookings")
        self.set_scheduler_table()
        self.slot = 0
        self.maxSlots = 10
        self.max_slots()
        if self.slot > self.maxSlots:
            self.slot = self.maxSlots

# ---------Button stuff------------

    def menu_buttons(self):
        sender = self.sender()
        self.reset_time()
        if sender is self.scheduleBtn:
            if self.schedule_backup.update_schedule(SaveStuff.read(strings.f_config)['room'], strings.f_backup_schedule) is not False:
                self.get_schedule()
                self.stackedWidget.setCurrentIndex(2)
            else:
                self.error_schedule_event("No connection")
        elif sender is self.defectsBtn:
            self.defects.get_defects(SaveStuff.read(strings.f_config)['room'])
            self.set_defect_table(self.defects.get_defect_table_data())
            self.stackedWidget.setCurrentIndex(3)
        elif sender is self.defectBack:
            self.defectQr.clear()
            self.get_reservation()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.scheduleBack:
            self.scheduleQr.clear()
            self.get_reservation()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.generateDefect:
            if self.schedule_backup.update_schedule(SaveStuff.read(strings.f_config)['room'], strings.f_backup_schedule) is not False:
                qrCode.generate_defect_qr(strings.f_qr_pic, self.defectTypeBox.currentText(), SaveStuff.read(strings.f_config)['room'])
                pixmap = QPixmap(strings.f_qr_pic)
                self.defectQr.setPixmap(pixmap.scaled(250, 250))
                print("qr set")
            else:
                self.error_schedule_event("No connection, it's not recommended to submit a defect"
                                          " at the moment please try again later")
        elif sender is self.generate:
            if self.schedule_backup.update_schedule(SaveStuff.read(strings.f_config)['room'], strings.f_backup_schedule) is not False:
                if self.check_reservation():
                    qrCode.generate_booking_qr(strings.f_qr_pic, self.calendarWidgetSchedule.selectedDate(),
                                               self.selectedSlot,
                                               self.lcdSlots.intValue(), SaveStuff.read(strings.f_config)['room'])
                    pixmap = QPixmap(strings.f_qr_pic)
                    self.scheduleQr.setPixmap(pixmap.scaled(250, 250))
                    print("qr set")
                else:
                    pass
            else:
                self.error_schedule_event("No connection")
                self.get_reservation()
                self.stackedWidget.setCurrentIndex(1)

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

# ----------reservation ui------------

    def radio_check(self):
        sender = self.sender()
        self.reset_time()
        self.max_slots()
        sender_id = self.radioButtonGroup.id(sender)
        self.selectedSlot = sender_id
        self.maxSlots = 16 - sender_id
        self.max_slots()
        self.radioButtonGroup.button(sender_id).setChecked(False)

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

    def check_reservation(self):
        for i in self.taken:
            if i == self.selectedSlot:
                self.error_schedule_event("Please select a valid slot")
                return False

# ----------sensor--------------

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
                    self.get_reservation()
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
            self.wakeButton.setText(strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

    def reset_time(self):
        self.start = time.time()

    def wakeup(self):
        self.reset_time()
        self.get_reservation()
        self.stackedWidget.setCurrentIndex(1)

    def save_press(self):
        data = {'room': str(self.roomNumTbox.text())}
        SaveStuff.write(data, strings.f_config)
        self.stackedWidget.setCurrentIndex(0)

# -------------data stuff-------------

    def set_scheduler_table(self):
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

    def backup_schedule(self):
        now = datetime.datetime.now()
        print("Updating schedule:" + str(now))
        self.schedule_backup.create_schedule(strings.f_backup_schedule, now)
        self.schedule_backup.update_schedule(SaveStuff.read(strings.f_config)['room'], strings.f_backup_schedule)
        # self.sd.enter(5, 1, self.backup_schedule)
        if self.schedule_backup.update_schedule(SaveStuff.read(strings.f_config)['room'], strings.f_backup_schedule) is not False:
            self.backup_time_lbl.setText("Last successful back up made at: " + now.strftime("%d %b") + " " +
                                         str(now.hour) + ":" + str(now.minute))
            self.connection_status_label.setText("Connection status: online")
        else:
            self.connection_status_label.setText("Connection status: offline")
        time.sleep(5)
        self.backup_schedule()

# ------------------events-------------

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

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.closeEvent()


def main():
    app = QApplication(sys.argv)
    main = MainUi()
    main.show()
    app.exec_()


if __name__ == '__main__':
    main()
