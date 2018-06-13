import json
import requests


class ApiConnect:
    def __init__(self):
        self.data = None
        self.jsondump = None

    def get_data(self, body, url):
        r = requests.post(url, json=body)
        print('print response')
        text = r.content
        print(text)
        print("\n###########\n")
        self.data = json.loads(text)
        # print(self.data)
        self.jsondump = json.dumps(self.data, indent=4, sort_keys=True)
        print(self.jsondump)
        return self.__get_data()

    def __get_data(self):
        return self.data

    def get_dump(self):
        return self.jsondump
