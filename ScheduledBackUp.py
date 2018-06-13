import json

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
        # self.db.clean_table('schedule')
        for i in range(3):
            print("weeks")
            print(week+i)
            body = {"room": room, "weeknummer": week+i}
            self.apiC.get_data(body, "http://markb.pythonanywhere.com/bookingbyroom/")
            # self.json_list = self.json_list + json.loads(self.apiC.get_dump())
            SaveStuff.write(json.loads(self.apiC.get_dump()), str(filename+str(i)+".json"))
        # self.__insert_into(filename)

    def __insert_into(self, filename):
        self.schedule = SaveStuff.read(filename)
        return self.schedule

    def get_schedule(self, filename):  # TODO CHANGE, FOR TESTING ATM
        self.schedule = SaveStuff.read(filename)
        return self.schedule


    def update_defects(self):
        pass

    # def update_schedule(self, room):
    #     now = datetime.datetime.now()
    #     week = datetime.date(now.year, now.month, now.day).isocalendar()[1]
    #     self.db.clean_table('schedule')
    #     for i in range(3):
    #         print("weeks")
    #         print(week + i)
    #         body = {"room": room, "weeknummer": week + i}
    #         self.apiC.get_data(body, "http://markb.pythonanywhere.com/bookingbyroom/")
    #         self.db.insert_into_schedule(week + i, self.apiC.get_dump())
    #     self.db.get_all_from_schedule()