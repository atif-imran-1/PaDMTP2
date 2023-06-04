from unittest import TestCase
from testcodes.difference import positive_difference as difference
import json

openJSON = open("MR_Values.json")

dataJSON = json.load(openJSON)

dataSaveJSON = []
for i in dataJSON['additive']:
    dataSaveJSON.append(i)

for i in dataJSON['inclusive']:
    dataSaveJSON.append(i)

for i in dataJSON['permutative']:
    dataSaveJSON.append(i)

for i in dataJSON['multiplicative']:
    dataSaveJSON.append(i)


class CodeTest(TestCase):

    # test case for checking non-prime nums
    def test_equal(self):
        for index, val in enumerate(dataSaveJSON):
            self.assertEqual(difference(dataSaveJSON[index]['x'], dataSaveJSON[index]['y']), dataSaveJSON[index]['z'])
