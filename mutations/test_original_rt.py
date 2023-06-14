from unittest import TestCase
from testcodes.originalCode import code as originalCode
import json

openJSON = open("./temp/RT_Values.json")

dataSaveJSON = json.load(openJSON)

class CodeTest(TestCase):

    # test case for checking non-prime nums
    def test_equal(self):
        for index, val in enumerate(dataSaveJSON):
            self.assertEqual(originalCode(dataSaveJSON[index]['x'], dataSaveJSON[index]['y']), dataSaveJSON[index]['z'])
