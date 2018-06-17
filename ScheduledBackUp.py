import json
import strings
# from Reservations import Reservations
from Defects import Defects
from ApiConnect import ApiConnect
import datetime
from Db import Db
import SaveStuff


class ScheduledBackUp:
    def __init__(self):
        self.apiC = ApiConnect()
        # self.reserve = Reservations()
        self.defects = Defects()
        self.db = Db()
        self.json_list = None

        self.schedule = None

    def update_schedule(self, room, filename):
        now = datetime.datetime.now()
        week = datetime.date(now.year, now.month, now.day).isocalendar()[1]
        for i in range(3):
            body = {"room": room, "weeknummer": week+i}
            try:
                self.apiC.get_data(body, strings.booking_url)
            except:
                return False
            if "fields" in self.apiC.get_dump():
                SaveStuff.write(json.loads(self.apiC.get_dump()), str(filename+str(i)+".json"))

    def __insert_into(self, filename):
        self.schedule = SaveStuff.read(filename)
        return self.schedule

    def get_schedule(self, filename):  # TODO CHANGE, FOR TESTING ATM
        self.schedule = SaveStuff.read(filename)
        return self.schedule

    @staticmethod
    def create_schedule(filename, date):
        SaveStuff.create(filename+".json")
        SaveStuff.write({"week": datetime.date(date.year, date.month, date.day).isocalendar()[1]},
                        filename+".json")

    def update_defects(self):
        pass
