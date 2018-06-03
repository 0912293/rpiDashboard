from unittest import TestCase
from reservations import reservations
import requests


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


class TestReservations(TestCase):
    def test_getReservations(self):
        r = reservations()

        r.getReservations("H.3.403", Date())
        for i in r.getTimeTableData():
            print(i)

    def test_getTimeTableData(self):
        r = reservations()
        self.assertEqual(r.getTimeTableData(),[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])


