import json
import pytest
from MSthesis.testcodes.originalCode import code as originalCode

openJSON = open("./temp/RT_Test_Cases.json")

RT_Test_Cases = json.load(openJSON)

RT_Test_Cases_Obj = []

@pytest.mark.parametrize("x, y", RT_Test_Cases)
def test_code_random_input(x,y):
    expected_output = x + y if x + y != 0 else (y - x if y > 0 else x - y)
    expected_output = expected_output - x if x > 0 else expected_output + x

    result = originalCode(x, y)
    
    RT_Test_Cases_Obj.append({'x': x,'y': y, 'z': result})
    jsonString = json.dumps(RT_Test_Cases_Obj)
    jsonFile = open("./temp/RT_Values.json", 'w')
    jsonFile.write(jsonString)
    jsonFile.close()
    
    assert result == expected_output, f"Unexpected output for input ({x}, {y}). Expected: {expected_output}, Actual: {result}"

