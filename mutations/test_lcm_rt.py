from unittest import TestCase
from testcodes.lcm import compute_lcm as lcm
import json

openJSON = open("./temp/RT_Values.json")

dataSaveJSON = json.load(openJSON)

class CodeTest(TestCase):

    # test case for checking non-prime nums
    def test_equal(self):
        for index, val in enumerate(dataSaveJSON):
            self.assertEqual(lcm(dataSaveJSON[index]['x'], dataSaveJSON[index]['y']), dataSaveJSON[index]['z'])
