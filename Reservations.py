import datetime
import json

from ApiConnect import ApiConnect
from ScheduledBackUp import ScheduledBackUp

class Reservations:
    def __init__(self):
        self.backup = ScheduledBackUp()
        self.apiC = ApiConnect()
        self.__timeTableData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def __enter_reservation(self, time_from, time_to, string):
        time = time_from - 1
        for i in range(time, time_to):
            self.__timeTableData[time] = (str(time + 1) + string)
            time += 1

    def get_reservations(self, room, date):
        self.__fill_empty_list()
        # date = self.calendarWidget.selectedDate()
        print(date)
        print("get schedule, calendar clicked")
        week = datetime.date(date.year(), date.month(), date.day()).isocalendar()[1]
        try:
            self.__get_data(room, week, date, "http://markb.pythonanywhere.com/bookingbyroo/")  # TODO
        except:
            print("PROBLEM WITH NETWORK, PRINTING BACKUP DATA FROM JSON")
            # data = json.loads(self.backup.get_schedule("C:/Users/kevin/PycharmProjects/Raspberry pi/schedule.json")) # TODO REMOVE, FOR TESTING
            data = self.backup.get_schedule("C:/Users/kevin/PycharmProjects/Raspberry pi/schedule.json")
            print(week-data["week"])
            schedule = None
            if week-data["week"] <= 2:
                schedule = self.backup.get_schedule("C:/Users/kevin/PycharmProjects/Raspberry pi/schedule" +
                                                    str(week-data["week"])+".json")
            try:
                self.__parse_data(schedule, date)
            except:
                print("shit is not ok")

    def __fill_empty_list(self):
        for i in range(15):
            self.__timeTableData[i] = ("%d Empty" % (i + 1))
            print(i+1)

    def __get_data(self, room, week, date, url):
        body = {"room": room, "weeknummer": week}
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\calendar")
        data = self.apiC.get_data(body, url)
        self.__parse_data(data, date)

    def __parse_data(self, data, date):
        for i in data:
            print("printing day:")
            print(str(date.day()))
            print(i["fields"]["date"][0:2] == str(date.day()))
            if i["fields"]["date"][0:2] == str(date.day()) and i["fields"]["date"][-4:] == str(date.year()) or \
                    i["fields"]["date"][1:2] == str(date.day()) and i["fields"]["date"][-4:] == str(date.year()):
                self.__enter_reservation(int(i["fields"]["timeslotfrom"]), int(i["fields"]["timeslotto"]),
                                         " %s %s %s %s %s" % (str(i["fields"]["timefrom"]), str(i["fields"]["timeto"]),
                                                              str(i["fields"]["room"]), str(i["fields"]["lesson"]),
                                                              str(i["fields"]["username"])))

    def get_time_table_data(self):
        return self.__timeTableData
