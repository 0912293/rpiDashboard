import datetime

import apiConnect


class Scheduler:
    def __init__(self):
        self.timeSlotData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.timeSlotBackUp = ["Timeslot 1 08:30 09:20", "Timeslot 2 09:20 10:10", "Timeslot 3 10:30 11:20",
                               "Timeslot 4 11:20 12:10", "Timeslot 5 12:10 13:00", "Timeslot 6 13:00 13:50",
                               "Timeslot 7 13:50 14:40", "Timeslot 8 15:00 15:50", "Timeslot 9 15:50 16:40",
                               "Timeslot 10 17:00 17:50", "Timeslot 11 17:50 18:40", "Timeslot 12 18:40 19:30",
                               "Timeslot 13 19:30 20:20", "Timeslot 14 20:20 21:10", "Timeslot 15 21:10 22:00"]

    def __enterScheduler(self, timeFrom, timeTo, string):
        time=timeFrom-1
        for i in range(time,timeTo):
            self.timeSlotData[time] = (str(time + 1) + string) #(string,timeFrom,timeTo)
            print(self.timeSlotData[time])
            time += 1

    def getSchedule(self, room, date, rbg):
        self.__fillRadioButtonList(rbg)
        print('------------------------------------------------')
        print(date)
        print("get schedule, getReservations calendar clicked")
        week = datetime.date(date.year(), date.month(), date.day()).isocalendar()[1]
        self.__getData(room, week, date, "http://markb.pythonanywhere.com/bookingbyroom/")

    def __fillRadioButtonList(self, rbg):
        self.radioButtonData = self.timeSlotBackUp
        print("RadioButtons")
        q = 0
        for i in rbg.buttons():
            self.timeSlotData[q] = q+1
            print(self.radioButtonData[q])
            i.setText(self.radioButtonData[q])
            i.setEnabled(True)
            q += 1
        print("xxxxxxxx")

    def __getData(self, room, week, date, url):
        body = {"room": room, "weeknummer": week}
        print("/////////////////////////Schedule")
        data = apiConnect.getData(body, url, date, 2)
        self.__parseData(data,date)

    def __parseData(self, data, date):
        for i in data:
            if i["fields"]["date"][0:2] == str(date.day()):
                self.__enterScheduler(int(i["fields"]["timeslotfrom"]), int(i["fields"]["timeslotto"]),
                                    " %s %s %s %s %s" % (str(i["fields"]["timefrom"]), str(i["fields"]["timeto"]),
                                                         str(i["fields"]["room"]), str(i["fields"]["lesson"]),
                                                         str(i["fields"]["username"])))

    def getTimeSlotData(self):
        return self.timeSlotData
