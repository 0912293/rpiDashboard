from unittest import TestCase
from defects import defects
import requests

class TestDefects(TestCase):
    def test_getDefects(self):
        d = defects()
        d.get_defects("H.3.403")
        for i in d.get_defect_table_data():
            print(i)

    def test_getDefectTableData(self):
        d = defects()
        self.assertEqual(d.get_defect_table_data(), [])
