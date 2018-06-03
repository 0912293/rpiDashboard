import datetime

import apiConnect

class defects():
    def __init__(self):
        self.defectTableData = []

    def __enterDefects(self, description, handled, type):
        self.defectTableData.append(str(type)+": "+str(description)+". Handled:"+str(handled))

    def getDefects(self,room):
        self.__getData(room, datetime.datetime.now(), "http://markb.pythonanywhere.com/roomdefuncts/")

    def getDefunctTypes(self,defectTypeBox):
        defectTypeBox.addItem("notype")
        defectTypeBox.addItem("type 1")
        defectTypeBox.addItem("type 2")
        defectTypeBox.addItem("type 3")

    def __getData(self,room, date, url):
        body = {"room": room}
        print("~~~~~~~~~~~~~~~~~~Defunct")
        data = apiConnect.getData(body, url, date,1)
        self.__parseData(data)

    def __parseData(self,data):
        for i in data:
            self.__enterDefects(i["fields"]["description"], i["fields"]["handled"], i["fields"]["type"])

    def getDefectTableData(self):
        return self.defectTableData