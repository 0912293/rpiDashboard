from ApiConnect import ApiConnect
import SaveStuff
import strings
import json
from datetime import datetime
from PyQt5 import QtWidgets

class StatisticScreen:
    def __init__(self):
        self.__apiC = ApiConnect()
        self.__interactions = 0
        self.__passed = 0
        self.interactions_json = None
        self.interactions_data = None
        self.passed_json = None
        self.passed_data = None

    def interaction(self):
        self.__interactions += 1
        print(str(self.__interactions))

    def passing(self):
        self.__passed += 1
        print(str(self.__passed))

    def __create_interactions_into_json(self):
        date = datetime.today()
        SaveStuff.create_(strings.f_interactions_json, json.dumps([{"interactions": {"date": {"day": str(date.day),
                                                                   "month": str(date.month), "year": str(date.year)},
                                                                                     "count": self.__interactions}}]))

    def write_interactions_into_json(self):
        date = datetime.today()
        if SaveStuff.check(strings.f_interactions_json):
            if not self.__read_interactions_into_json():
                self.interactions_json += ([{"interactions": {"date": {"day": str(date.day), "month":
                                            str(date.month), "year": str(date.year)}, "count": self.__interactions}}])
            SaveStuff.write(self.interactions_json, strings.f_interactions_json)
            self.__get_interaction_data()
        else:
            self.__create_interactions_into_json()

    def __read_interactions_into_json(self):
        self.interactions_json = SaveStuff.read(strings.f_interactions_json)
        date = datetime.today().date()
        print(date)
        for i in self.interactions_json:
            iDate = datetime(int(i["interactions"]["date"]["year"]), int(i["interactions"]["date"]["month"]),
                             int(i["interactions"]["date"]["day"])).date()
            print(iDate)
            if iDate == date:
                self.__interactions += i["interactions"]["count"]
                i["interactions"]["count"] = self.__interactions
                return True
        return False

    def __get_interaction_data(self):
        interactions_data = []
        date = datetime.today().date()
        for i in self.interactions_json:
            iDate = datetime(int(i["interactions"]["date"]["year"]), int(i["interactions"]["date"]["month"]),
                             int(i["interactions"]["date"]["day"])).date()
            delta = date - iDate
            if 0 <= delta.days <= 6:
                interactions_data.append((iDate, i["interactions"]["count"]))
        self.interactions_data = interactions_data

    def insert_interactions_into_table(self, table):
        count = 0
        for i in self.interactions_data:
            table.setItem(0, count, QtWidgets.QTableWidgetItem(str(i[0])))
            table.setItem(1, count, QtWidgets.QTableWidgetItem(str(i[1])))
            count += 1

    def __create_passing_into_json(self):
        date = datetime.today()
        SaveStuff.create_(strings.f_passing_json, json.dumps([{"passed": {"date": {"day": str(date.day),
                                                               "month": str(date.month), "year": str(date.year)},
                                                                                "count": self.__passed}}]))

    def write_passing_into_json(self):
        date = datetime.today()
        if SaveStuff.check(strings.f_passing_json):
            if not self.__read_passing_into_json():
                self.passed_json += ([{"passed": {"date": {"day": str(date.day), "month":
                                      str(date.month), "year": str(date.year)}, "count": self.__passed}}])
            SaveStuff.write(self.passed_json, strings.f_passing_json)
        else:
            self.__create_passing_into_json()
        self.__get_passing_data()

    def __read_passing_into_json(self):
        self.passed_json = SaveStuff.read(strings.f_passing_json)
        date = datetime.today().date()
        for i in self.passed_json:
            iDate = datetime(int(i["passed"]["date"]["year"]), int(i["passed"]["date"]["month"]),
                             int(i["passed"]["date"]["day"])).date()
            if iDate == date:
                self.__passed += i["passed"]["count"]
                i["passed"]["count"] = self.__passed
                return True
        return False

    def __get_passing_data(self):
        passed_data = []
        date = datetime.today().date()
        for i in self.passed_json:
            iDate = datetime(int(i["passed"]["date"]["year"]), int(i["passed"]["date"]["month"]),
                             int(i["passed"]["date"]["day"])).date()
            delta = date - iDate
            print(delta.days)
            if 0 <= delta.days <= 6:
                passed_data.append((iDate, i["passed"]["count"]))
        self.passed_data = passed_data

    def insert_passing_into_table(self, table):
        count = 0
        for i in self.passed_data:
            table.setItem(0, count, QtWidgets.QTableWidgetItem(str(i[0])))
            table.setItem(1, count, QtWidgets.QTableWidgetItem(str(i[1])))
            count += 1