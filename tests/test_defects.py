from unittest import TestCase
from defects import defects
import requests

class TestDefects(TestCase):
    def test_getDefects(self):
        d = defects()
        d.getDefects("H.3.403")
        for i in d.getDefectTableData():
            print(i)

    def test_getDefectTableData(self):
        d = defects()
        self.assertEqual(d.getDefectTableData(),[])
