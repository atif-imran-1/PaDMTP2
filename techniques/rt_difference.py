import json
import pytest
from MSthesis.testcodes.difference import positive_difference as difference

openJSON = open("./temp/RT_Test_Cases.json")

RT_Test_Cases = json.load(openJSON)

RT_Test_Cases_Obj = []

@pytest.mark.parametrize("x, y", RT_Test_Cases)
def test_positive_difference_random_input(x, y):
    # Generate expected output
    expected_output = x - y if x >= y else y - x
        
    # Compare expected output with actual output
    result = difference(x, y)

    RT_Test_Cases_Obj.append({'x': x,'y': y, 'z': result})
    jsonString = json.dumps(RT_Test_Cases_Obj)
    jsonFile = open("./temp/RT_Values.json", 'w')
    jsonFile.write(jsonString)
    jsonFile.close()

    assert result == expected_output, f"Unexpected output for input ({x}, {y}). Expected: {expected_output}, Actual: {result}"

