import datetime
import strings
from ApiConnect import ApiConnect


class Reservations:
    def __init__(self):
        self.apiC = ApiConnect()
        self.timeSlotData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.timeSlotBackUp = ["Timeslot 1 08:30 09:20", "Timeslot 2 09:20 10:10", "Timeslot 3 10:30 11:20",       # used to display in case of empty slots
                               "Timeslot 4 11:20 12:10", "Timeslot 5 12:10 13:00", "Timeslot 6 13:00 13:50",
                               "Timeslot 7 13:50 14:40", "Timeslot 8 15:00 15:50", "Timeslot 9 15:50 16:40",
                               "Timeslot 10 17:00 17:50", "Timeslot 11 17:50 18:40", "Timeslot 12 18:40 19:30",
                               "Timeslot 13 19:30 20:20", "Timeslot 14 20:20 21:10", "Timeslot 15 21:10 22:00"]

    def __enter_scheduler(self, time_from, time_to, string):
        time = time_from - 1
        for i in range(time, time_to):
            self.timeSlotData[time] = (str(time + 1) + string)
            time += 1

    def get_reservations(self, room, date, rbg):
        self.__fill_radio_button_list(rbg)
        week = datetime.date(date.year(), date.month(), date.day()).isocalendar()[1]
        self.__get_data(room, week, date, strings.booking_url)

    def __fill_radio_button_list(self, rbg):    # clears data and inserts clean time slots
        self.radioButtonData = self.timeSlotBackUp
        q = 0
        for i in rbg.buttons():
            self.timeSlotData[q] = q+1
            i.setText(self.radioButtonData[q])
            i.setEnabled(True)
            q += 1

    def __get_data(self, room, week, date, url):
        body = {"room": room, "weeknummer": week}
        data = self.apiC.get_data(body, url)
        self.__parse_data(data, date)

    def __parse_data(self, data, date):     # inserts data from json into list
        for i in data:
            if i["fields"]["date"][0:2] == str(date.day()) and i["fields"]["date"][-4:] == str(date.year()) or\
                    i["fields"]["date"][1:2] == str(date.day()) and i["fields"]["date"][-4:] == str(date.year()):
                self.__enter_scheduler(int(i["fields"]["timeslotfrom"]), int(i["fields"]["timeslotto"]),
                                       " %s %s %s %s %s" % (str(i["fields"]["timefrom"]), str(i["fields"]["timeto"]),
                                                            str(i["fields"]["room"]), str(i["fields"]["lesson"]),
                                                            str(i["fields"]["username"])))

    def get_time_slot_data(self):
        return self.timeSlotData

    def set_scheduler_table(self, rbg):
        time_slot_data = self.get_time_slot_data()
        j = 0
        for i in rbg.buttons():
            if time_slot_data[j] != j + 1:      # inserts data into view and disables radio buttons that are unavailable
                i.setText(time_slot_data[j])
                i.setEnabled(False)
            j += 1