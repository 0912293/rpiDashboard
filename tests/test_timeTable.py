from unittest import TestCase
from TimeTable import TimeTable


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


class TestTimeTable(TestCase):
    def test_get_time_table(self):
        TT = TimeTable()
        TT.get_time_table("H.3.403", Date)
        self.assertNotEqual(TT.get_time_table_data(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
