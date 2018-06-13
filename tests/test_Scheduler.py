from unittest import TestCase
from Scheduler import Scheduler
import requests
from PyQt5 import QtWidgets

class Date:
    @staticmethod
    def year():
        return 2018

    @staticmethod
    def month():
        return 10

    @staticmethod
    def day():
        return 13


class TestScheduler(TestCase): #TODO Not sure yet how to test radio buttons
    def initButtons(self):
        rbg = QtWidgets.QButtonGroup()
        for i in range(1,15):
            rbg.addButton(QtWidgets.QRadioButton)
        return rbg

    def test_getSchedule(self):
        s = Scheduler()
        self.setupUi(self)
        s.get_schedule("H.3.403", Date(), self.initButtons())

    def test_getTimeSlotData(self):
        s = Scheduler()
        self.assertEqual(s.get_time_slot_data(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
