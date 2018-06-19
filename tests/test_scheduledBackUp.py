from unittest import TestCase
from ScheduledBackUp import ScheduledBackUp
from datetime import datetime
import os
import json
from ApiConnect import ApiConnect
import strings

class Date:
    @staticmethod
    def year():
        return 2018

    @staticmethod
    def month():
        return 6

    @staticmethod
    def day():
        return 19


class TestScheduledBackUp(TestCase):
    def setUp(self):
        self.sbu = ScheduledBackUp()
        self.api = ApiConnect()

    def test_update_schedule(self):
        da = datetime(Date.year(), Date.month(), Date.day())
        self.sbu.create_schedule("test", da)
        self.sbu.update_schedule("H.3.403", "test")
        data = self.sbu.get_schedule("C:/Users/kevin/PycharmProjects/Raspberry Pi/tests/test.json")
        schedule = None
        week = datetime.date(da).isocalendar()[1]
        if week - data["week"] <= 2:
            schedule = self.sbu.get_schedule("C:/Users/kevin/PycharmProjects/Raspberry Pi/tests/test" +
                                                  str(week - data["week"]) + ".json")
        dump = json.dumps(schedule, indent=4, sort_keys=True)
        self.api.get_data({"room": "H.3.403", "weeknummer": week}, strings.booking_url)

        self.assertEqual(dump, self.api.get_dump())

        self.cleanup()

    @staticmethod
    def cleanup():
        os.remove("C:/Users/kevin/PycharmProjects/Raspberry Pi/tests/test.json")
        for i in range(0,3):
            os.remove("C:/Users/kevin/PycharmProjects/Raspberry Pi/tests/test" +
                                                  str(i) + ".json")
