import json
from unittest import TestCase
import requests
import apiConnect


class TestApiConnect(TestCase):
    def test_api_connection(self):
        body = {"room": "H.3.403"}
        r = requests.post("http://markb.pythonanywhere.com/roomdefuncts/", json=body)
        self.assertEqual(r.status_code,200)

        body1 = {"room": "H.3.403","weeknummer": 22}
        r1 = requests.post("http://markb.pythonanywhere.com/bookingbyroom/", json=body1)
        self.assertEqual(r1.status_code, 200)

    def test_getData(self):
        a = apiConnect
        body = {"room": "H.3.403"}

        r = requests.post("http://markb.pythonanywhere.com/roomdefuncts/", json=body)
        data = json.loads(r.content)

        self.assertEqual(a.get_data(body, "http://markb.pythonanywhere.com/roomdefuncts/"), data)