import json
import pytest
from MSthesis.testcodes.hcf import compute_hcf as hcf

openJSON = open("./temp/RT_Test_Cases.json")

RT_Test_Cases = json.load(openJSON)

RT_Test_Cases_Obj = []

@pytest.mark.parametrize("x, y", RT_Test_Cases)
def test_compute_hcf_random_input(x, y):
    # Generate expected output
    expected_output = 0
    smaller = min(x, y)
    for i in range(1, smaller + 1):
        if x % i == 0 and y % i == 0:
            expected_output = i
    # Compare expected output with actual output
    result = hcf(x, y)

    RT_Test_Cases_Obj.append({'x': x,'y': y, 'z': result})
    jsonString = json.dumps(RT_Test_Cases_Obj)
    jsonFile = open("./temp/RT_Values.json", 'w')
    jsonFile.write(jsonString)
    jsonFile.close()

    assert result == expected_output, f"Unexpected output for input ({x}, {y}). Expected: {expected_output}, Actual: {result}"

