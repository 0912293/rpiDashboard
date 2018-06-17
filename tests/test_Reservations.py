from unittest import TestCase
from TimeTable import TimeTable
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
        r = TimeTable()

        r.get_time_table("H.3.403", Date())
        for i in r.get_time_table_data():
            print(i)

    def test_getTimeTableData(self):
        r = TimeTable()
        self.assertEqual(r.get_time_table_data(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])


