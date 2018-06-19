import json
import strings
# from Reservations import Reservations
from Defects.Defects import Defects
from ApiConnect import ApiConnect
import datetime
import SaveStuff


class ScheduledBackUp:
    def __init__(self):
        self.apiC = ApiConnect()
        self.defects = Defects()
        self.json_list = None
        now = datetime.datetime.now()
        self.week = datetime.date(now.year, now.month, now.day).isocalendar()[1]

        self.schedule = None

    def update_schedule(self, room, filename):
        for i in range(3):                                   # gets data from this week and the next 2 after and inserts them in their own json files
            body = {"room": room, "weeknummer": self.week+i}
            try:
                self.apiC.get_data(body, strings.booking_url)
            except:
                pass
            if "fields" in self.apiC.get_dump() and SaveStuff.check(str(filename+str(i)+".json")) or \
                    "fields" not in self.apiC.get_dump() and not SaveStuff.check(str(filename+str(i)+".json")) or\
                    "fields" in self.apiC.get_dump() and not SaveStuff.check(str(filename+str(i)+".json")):
                SaveStuff.write(json.loads(self.apiC.get_dump()), str(filename + str(i) + ".json"))

    def check_connection(self, room):
        body = {"room": room, "weeknummer": self.week}
        return self.apiC.check_connection(body)

    def get_schedule(self, filename):
        self.schedule = SaveStuff.read(filename)
        return self.schedule

    @staticmethod
    def create_schedule(filename, date):
        SaveStuff.create(filename+".json")
        SaveStuff.write({"week": datetime.date(date.year, date.month, date.day).isocalendar()[1]},
                        filename+".json")
