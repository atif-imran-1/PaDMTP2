from unittest import TestCase
from testcodes.hcf import compute_hcf as hcf
import json

openJSON = open("RT_Values.json")

dataSaveJSON = json.load(openJSON)

class CodeTest(TestCase):

    # test case for checking non-prime nums
    def test_equal(self):
        for index, val in enumerate(dataSaveJSON):
            self.assertEqual(hcf(dataSaveJSON[index]['x'], dataSaveJSON[index]['y']), dataSaveJSON[index]['z'])
