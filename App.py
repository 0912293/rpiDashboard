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
import RPi.GPIO as GPIO  # delete folder for rpi
import threading
from time import strftime
import SaveStuff
from qr import qrCode
from Defects.Defects import Defects
from Time_table.TimeTable import TimeTable
from Reservation.Reservations import Reservations
from ScheduledBackUp import ScheduledBackUp
import strings
from SetupScreenListener import SetupScreenListener
from StatisticScreen import StatisticScreen


class MainUi(QMainWindow, main.Ui_MainWindow, SetupScreenListener):
    def __init__(self, parent=None):
        self.__defects = Defects()
        self.__time_table = TimeTable()
        self.__reservations = Reservations()
        self.__schedule_backup = ScheduledBackUp()
        self.__stat_screen = StatisticScreen()

        self.taken = []  # used to store taken time slots for reservations

        super(MainUi, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()

        self.setup_screen_listener = SetupScreenListener(self.roomNumTbox, self.stackedWidget)

        if not SaveStuff.check(strings.f_config):   # checks if the config file exists
            self.stackedWidget.setCurrentIndex(4)   # if this is the first time running the rpi it will setup the room
            SaveStuff.create(strings.f_config)
            self.savebtn.clicked.connect(self.setup_screen_listener.save_press)
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.get_time_table()

        self.get_time_table()

        self.__defects.get_defunct_types(self.defectTypeBox)

        self.slot = 1
        self.selectedSlot = 1
        self.maxSlots = 15
        self.lcdSlots.display(self.slot)

        self.passCounter = 0

        thread = threading.Thread(target=self.distance_sensor)  # thread for running the distance sensor
        thread.daemon = True
        thread.start()

        thread2 = threading.Thread(target=self.clock)   # thread for running the clock
        thread2.daemon = True
        thread2.start()

        thread3 = threading.Thread(target=self.backup_data)     # thread for running scheduled backups
        thread3.daemon = True
        thread3.start()

        self.start = 0

    def init_ui(self):      # connecting ui to listeners
        QMainWindow.showFullScreen(self)
        self.defectsBtn.clicked.connect(self.menu_buttons)
        self.defectBack.clicked.connect(self.menu_buttons)
        self.generateDefect.clicked.connect(self.qr_buttons)
        self.scheduleBtn.clicked.connect(self.menu_buttons)
        self.scheduleBack.clicked.connect(self.menu_buttons)
        self.generate.clicked.connect(self.qr_buttons)

        self.calendarWidget.clicked.connect(self.get_time_table)

        self.calendarWidgetSchedule.clicked.connect(self.get_reservations)
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

        self.statisticsBtn.clicked.connect(self.menu_buttons)
        self.statisticsBackBtn.clicked.connect(self.menu_buttons)

        self.wakeButton.clicked.connect(self.wakeup)

    def get_time_table(self):   # gets time table data and inserts it
        self.__time_table.get_time_table(SaveStuff.read(strings.f_config)['room'], self.calendarWidget.selectedDate())
        self.set_time_table()

    def get_reservations(self):     # gets reservation data and inserts it
        try:
            self.__reservations.get_reservations(SaveStuff.read(strings.f_config)['room'],
                                                 self.calendarWidgetSchedule.selectedDate(), self.radioButtonGroup)
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
        sender = self.sender()  # checks which button was clicked
        self.reset_time()       # resets sleep timer so the screen doesn't turn off while someone is using it
        if sender is self.scheduleBtn:
            if self.__schedule_backup.check_connection(SaveStuff.read(strings.f_config)['room']) is not False:    # checks if there is a connection otherwise prevent user from making reservations
                self.stackedWidget.setCurrentIndex(2)
                self.get_reservations()
            else:
                self.stackedWidget.setCurrentIndex(1)
                self.error_schedule_event("No connection")
        elif sender is self.defectsBtn:
            if self.__schedule_backup.check_connection(SaveStuff.read(strings.f_config)['room']) is not False:    # checks if there is a connection otherwise prevent user from making reservations
                self.__defects.get_defects(SaveStuff.read(strings.f_config)['room'])
                self.set_defect_table(self.__defects.get_defect_table_data())
                self.stackedWidget.setCurrentIndex(3)
            else:
                self.stackedWidget.setCurrentIndex(1)
                self.error_schedule_event("No connection")
        elif sender is self.defectBack:
            self.defectQr.clear()
            self.get_time_table()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.scheduleBack:
            self.scheduleQr.clear()
            self.get_time_table()
            self.stackedWidget.setCurrentIndex(1)
        elif sender is self.statisticsBtn:
            self.__stat_screen.insert_interactions_into_table(self.interactionTable)
            self.__stat_screen.insert_passing_into_table(self.passTable)
            self.stackedWidget.setCurrentIndex(5)
        elif sender is self.statisticsBackBtn:
            self.get_time_table()
            self.stackedWidget.setCurrentIndex(1)

    def qr_buttons(self):
        sender = self.sender()  # checks which button was clicked
        self.reset_time()  # resets sleep timer so the screen doesn't turn off while someone is using it
        if sender is self.generateDefect:
            if self.__schedule_backup.check_connection(SaveStuff.read(strings.f_config)['room']) is not False:   # checks if there is a connection otherwise prevent user from submiting defects
                qrCode.generate_defect_qr(strings.f_qr_pic, self.defectTypeBox.currentText(),
                                          SaveStuff.read(strings.f_config)['room'])
                pixmap = QPixmap(strings.f_qr_pic)
                self.defectQr.setPixmap(pixmap.scaled(250, 250))
            else:
                self.error_schedule_event("No connection, it's not recommended to submit a defect"
                                          " at the moment please try again later")
        elif sender is self.generate:
            if self.__schedule_backup.check_connection(SaveStuff.read(strings.f_config)['room']) is not False:    # checks if there is a connection otherwise prevent user from making reservations
                if self.check_reservation():
                    qrCode.generate_booking_qr(strings.f_qr_pic, self.calendarWidgetSchedule.selectedDate(),
                                               self.selectedSlot,
                                               self.lcdSlots.intValue(), SaveStuff.read(strings.f_config)['room'])
                    pixmap = QPixmap(strings.f_qr_pic)
                    self.scheduleQr.setPixmap(pixmap.scaled(250, 250))
                else:
                    self.error_schedule_event("Please select a valid slot")
            else:
                self.error_schedule_event("No connection")
                self.get_time_table()
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

    def max_slots(self):    # used to determine the max amount of slots a user can select
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

    def check_disabled_slots(self):     # checks which time slots already have reservations
        q = 1
        self.taken = []
        for i in self.__reservations.get_time_slot_data():
            if i != q:
                self.taken.append(q)
            q += 1

    def check_reservation(self):        # check to see if the reservation is good
        for i in self.taken:
            if i == self.selectedSlot:
                return False
        return True

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
                GPIO.output(PIN_TRIGGER, GPIO.HIGH)     # makes the sonar send a pulse
                time.sleep(0.00001)
                GPIO.output(PIN_TRIGGER, GPIO.LOW)
                while GPIO.input(PIN_ECHO) == 0:
                    pulse_start_time = time.time()      # checks the timer after sending the pulse
                while GPIO.input(PIN_ECHO) == 1:
                    pulse_end_time = time.time()        # checks the time after getting the input back
                pulse_duration = pulse_end_time - pulse_start_time      # calculates the difference in time between sending and recieving the pulse
                distance = round(pulse_duration * 17150, 2)                         # calculates the distance using the rough speed of sound which is 34300 cm/s
                                                                                    #  since the duration is the time it took hitting an object and bouncing back we devide this by 2 making it 17150 cm/s
                if distance < 40 and self.stackedWidget.currentIndex() is 0:        # if someone gets close to the raspberry pi it will wake up and go to the main menu
                    self.get_time_table()
                    self.stackedWidget.setCurrentIndex(1)
                    self.start = time.time()        # starts a timer to go back to sleep after being inactive for a while
                elif distance < 100 and distance is not 0 and self.stackedWidget.currentIndex() is 0:   # checks how many people have walked passed the raspberry pi
                    self.__stat_screen.__passed()
                    time.sleep(0.8)
                if (time.time()) - self.start > 10 and distance > 100 and self.stackedWidget.currentIndex() is not 4:
                    self.stackedWidget.setCurrentIndex(0)       # puts rpi back to sleep after 10 sec atm if no one is near it
        finally:
            print('cleaning')
            GPIO.cleanup()  # clean up of the GPIO pins to ensure an end to our try

    def clock(self):
        while True:
            time.sleep(1)
            self.wakeButton.setText(strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

    def reset_time(self):
        self.start = time.time()

    def wakeup(self):
        self.__stat_screen.interaction()
        self.reset_time()
        self.get_time_table()
        self.stackedWidget.setCurrentIndex(1)

# -------------data stuff-------------

    def set_scheduler_table(self):
        time_slot_data = self.__reservations.get_time_slot_data()
        j = 0
        for i in self.radioButtonGroup.buttons():
            if time_slot_data[j] != j + 1:      # inserts data into view and disables radio buttons that are unavailable
                i.setText(time_slot_data[j])
                i.setEnabled(False)
            j += 1

    def set_time_table(self):
        model = QStringListModel(self.__time_table.get_time_table_data())
        self.listView.setModel(model)       # inserts model into view

    def set_defect_table(self, data):
        model = QStringListModel(data)      # inserts model into view
        self.defectListView.setModel(model)

    def backup_data(self):
        self.get_time_table()
        now = datetime.datetime.now()
        print("Updating schedule:" + str(now))
        self.__schedule_backup.create_schedule(strings.f_backup_schedule, now)
        self.__schedule_backup.update_schedule(SaveStuff.read(strings.f_config)['room'], strings.f_backup_schedule)
        if self.__schedule_backup.check_connection(SaveStuff.read(strings.f_config)['room']) is not False:
            self.backup_time_lbl.setText("Last successful back up made at: " + now.strftime("%d %b") + " " +
                                         str(now.hour) + ":" + str(now.minute))
            self.connection_status_label.setText("Connection status: online")
        else:
            self.connection_status_label.setText("Connection status: offline")
        self.__stat_screen.write_interactions_into_json()
        self.__stat_screen.write_passing_into_json()
        time.sleep(600)     # tries to back up from api every 10 minutes and displays the last successful "pull" and status
        self.backup_data()

# ------------------events-------------

    def error_schedule_event(self, string):     # error event to give feedback to the user if something goes wrong
        reply = QMessageBox.question(self, 'Message',
                                     "An error has occurred: %s" % string, QMessageBox.Ok)

    def closeEvent(self):   # close event which is called after user presses esc
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

    def keyPressEvent(self, e):     # calls close event upon pressing esc
        if e.key() == Qt.Key_Escape:
            self.closeEvent()


def main():
    app = QApplication(sys.argv)
    main = MainUi()
    main.show()
    app.exec_()


if __name__ == '__main__':
    main()
