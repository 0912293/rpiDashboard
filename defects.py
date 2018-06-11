import datetime

import apiConnect

class defects():
    def __init__(self):
        self.defectTableData = []

    def __enter_defects(self, description, handled, type):
        self.defectTableData.append(str(type)+": "+str(description)+". Handled:"+str(handled))

    def get_defects(self, room):
        self.__get_data(room, "http://markb.pythonanywhere.com/roomdefuncts/")

    @staticmethod
    def get_defunct_types(defect_type_box):
        defect_type_box.addItem("notype")
        defect_type_box.addItem("type 1")
        defect_type_box.addItem("type 2")
        defect_type_box.addItem("type 3")

    def __get_data(self, room, url):
        body = {"room": room}
        print("~~~~~~~~~~~~~~~~~~Defunct")
        data = apiConnect.get_data(body, url)
        self.__parse_data(data)

    def __parse_data(self, data):
        for i in data:
            self.__enter_defects(i["fields"]["description"], i["fields"]["handled"], i["fields"]["type"])

    def get_defect_table_data(self):
        return self.defectTableData
