import strings
from ApiConnect import ApiConnect


class Defects:
    def __init__(self):
        self.apiC = ApiConnect()
        self.__defect_table_data = []

    def __enter_defects(self, description, handled, type):
        self.__defect_table_data.append(str(type) + ": " + str(description) + ". Handled:" + str(handled))

    def get_defects(self, room):
        self.__get_data(room, strings.defect_url)

    @staticmethod
    def get_defunct_types(defect_type_box):     # currently a hard coded list but would've like for this to be retrieved from api if that was a possibility
        defect_type_box.addItem("notype")
        defect_type_box.addItem("type 1")
        defect_type_box.addItem("type 2")
        defect_type_box.addItem("type 3")

    def __get_data(self, room, url):
        body = {"room": room}
        data = self.apiC.get_data(body, url)
        self.__parse_data(data)

    def __parse_data(self, data):   # enters defects into model
        for i in data:
            self.__enter_defects(i["fields"]["description"], i["fields"]["handled"], i["fields"]["type"])

    def get_defect_table_data(self):
        return self.__defect_table_data     # returns model
