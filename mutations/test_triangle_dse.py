from unittest import TestCase
from testcodes.triangle import compute_area_of_triangle as triangle
import json

openJSON = open("DSE_Values.json")

dataSaveJSON = json.load(openJSON)

class CodeTest(TestCase):

    # test case for checking non-prime nums
    def test_equal(self):
        for index, val in enumerate(dataSaveJSON):
            self.assertEqual(triangle(dataSaveJSON[index]['x'], dataSaveJSON[index]['y']), dataSaveJSON[index]['z'])
