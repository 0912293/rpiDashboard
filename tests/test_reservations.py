from unittest import TestCase
from Reservation.Reservations import Reservations
from PyQt5 import QtWidgets


class Date:
    @staticmethod
    def year():
        return 2018

    @staticmethod
    def month():
        return 7

    @staticmethod
    def day():
        return 16


class TestScheduler(TestCase):
    rbg = QtWidgets.QButtonGroup()

    def initButtons(self):
        for i in range(1, 15):
            b = QtWidgets.QRadioButton()
            b.setObjectName(str(i))
            self.rbg.addButton(b, i)
        return self.rbg

    def test_get_reservations(self):
        s = Reservations()
        s.get_reservations("H.3.403", Date(), self.rbg)
        s.set_scheduler_table(self.rbg)
        for i in self.rbg.buttons():
            print(i.text())
            self.assertEqual(i.text, None)

    def test_get_time_slot_data(self):
        s = Reservations()
        self.assertEqual(s.get_time_slot_data(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
