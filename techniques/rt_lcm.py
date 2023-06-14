import json
import pytest
from MSthesis.testcodes.lcm import compute_lcm as lcm

openJSON = open("./temp/RT_Test_Cases.json")

RT_Test_Cases = json.load(openJSON)

RT_Test_Cases_Obj = []

@pytest.mark.parametrize("x, y", RT_Test_Cases)
def test_compute_lcm_random_input(x, y):
    # Generate expected output
    expected_output = 0
    greater = max(x, y)
    while True:
        if greater % x == 0 and greater % y == 0:
            expected_output = greater
            break
        greater += 1
        
    # Compare expected output with actual output
    result = lcm(x, y)

    RT_Test_Cases_Obj.append({'x': x,'y': y, 'z': result})
    jsonString = json.dumps(RT_Test_Cases_Obj)
    jsonFile = open("./temp/RT_Values.json", 'w')
    jsonFile.write(jsonString)
    jsonFile.close()

    assert result == expected_output, f"Unexpected output for input ({x}, {y}). Expected: {expected_output}, Actual: {result}"

