from unittest import TestCase
from Defects import Defects
import requests

class TestDefects(TestCase):
    def test_getDefects(self):
        d = Defects()
        d.get_defects("H.3.403")
        for i in d.get_defect_table_data():
            print(i)
            self.assertNotEqual(i, None)

    def test_getDefectTableData(self):
        d = Defects()
        self.assertEqual(d.get_defect_table_data(), [])
