from unittest import TestCase
from testcodes.difference import positive_difference as difference
import json

openJSON = open("ART_Values.json")

dataSaveJSON = json.load(openJSON)

class CodeTest(TestCase):

    # test case for checking non-prime nums
    def test_equal(self):
        for index, val in enumerate(dataSaveJSON):
            self.assertEqual(difference(dataSaveJSON[index]['x'], dataSaveJSON[index]['y']), dataSaveJSON[index]['z'])
