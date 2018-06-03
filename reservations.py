import datetime

import apiConnect

class reservations():
    def __init__(self):
        self.__timeTableData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def __enterReservation(self, timeFrom, timeTo, string):
        time=timeFrom-1
        for i in range(time,timeTo):
            self.__timeTableData[time] = (str(time + 1) + string)
            time += 1

    def getReservations(self, room, date):
        self.__fillEmptyList()
        # date = self.calendarWidget.selectedDate()
        print(date)
        print("get schedule, calendar clicked")
        week = datetime.date(date.year(),date.month(),date.day()).isocalendar()[1]
        self.__getData(room, week, date, "http://markb.pythonanywhere.com/bookingbyroom/")

    def __fillEmptyList(self):
        for i in range(15):
            self.__timeTableData[i] = ("%d Empty" % (i + 1))
            print(i+1)

    def __getData(self, room, week, date, url):
        body = {"room": room, "weeknummer": week}
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\calendar")
        data = apiConnect.getData(body, url, date,0)
        self.__parseData(data, date)

    def __parseData(self, data, date):
        for i in data:
            print("printing day:")
            print(str(date.day()))
            print(i["fields"]["date"][0:2] == str(date.day()))
            if i["fields"]["date"][0:2] == str(date.day()):
                self.__enterReservation(int(i["fields"]["timeslotfrom"]), int(i["fields"]["timeslotto"]),
                                      " %s %s %s %s %s" % (str(i["fields"]["timefrom"]), str(i["fields"]["timeto"]),
                                                           str(i["fields"]["room"]), str(i["fields"]["lesson"]),
                                                           str(i["fields"]["username"])))

    def getTimeTableData(self):
        return self.__timeTableData
