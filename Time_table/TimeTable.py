import datetime
import strings
from ApiConnect import ApiConnect
from ScheduledBackUp import ScheduledBackUp


class TimeTable:
    def __init__(self):
        self.__backup = ScheduledBackUp()
        self.__apiC = ApiConnect()
        self.__timeTableData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def __enter_reservation(self, time_from, time_to, string):
        time = time_from - 1
        for i in range(time, time_to):
            self.__timeTableData[time] = (str(time + 1) + string)
            time += 1

    def get_time_table(self, room, date):
        self.__fill_empty_list()
        week = datetime.date(date.year(), date.month(), date.day()).isocalendar()[1]
        try:
            self.__get_data(room, week, date, strings.booking_url)      # tries to get data from api, if this fails it retrieves data from back files
        except:
            data = self.__backup.get_schedule(strings.f_schedule_json)
            schedule = None
            if week-data["week"] <= 2:
                schedule = self.__backup.get_schedule(strings.f_backup_schedule +
                                                      str(week-data["week"]) +".json")
            self.__parse_data(schedule, date)

    def __fill_empty_list(self):
        for i in range(15):
            self.__timeTableData[i] = ("%d Empty" % (i + 1))

    def __get_data(self, room, week, date, url):
        body = {"room": room, "weeknummer": week}
        data = self.__apiC.get_data(body, url)
        self.__parse_data(data, date)

    def __parse_data(self, data, date):
        for i in data:
            if i["fields"]["date"][0:2] == str(date.day()) and i["fields"]["date"][-4:] == str(date.year()) or \
                    i["fields"]["date"][1:2] == str(date.day()) and i["fields"]["date"][-4:] == str(date.year()):
                self.__enter_reservation(int(i["fields"]["timeslotfrom"]), int(i["fields"]["timeslotto"]),
                                         " %s %s %s %s %s" % (str(i["fields"]["timefrom"]), str(i["fields"]["timeto"]),
                                                              str(i["fields"]["room"]), str(i["fields"]["lesson"]),
                                                              str(i["fields"]["username"])))

    def get_time_table_data(self):
        return self.__timeTableData
