import json
import requests
import strings


class ApiConnect:
    def __init__(self):
        self.data = None
        self.jsondump = None

    def get_data(self, body, url):      # retrieves data from api
        r = requests.post(url, json=body)
        text = r.content
        self.data = json.loads((r.content.decode('utf-8')))
        self.jsondump = json.dumps(self.data, indent=4, sort_keys=True)
        return self.__get_data()

    def __get_data(self):
        return self.data

    def get_dump(self):
        return self.jsondump

    def check_connection(self, body):
        try:
            self.get_data(body, strings.booking_url)
            return True
        except:
            return False
