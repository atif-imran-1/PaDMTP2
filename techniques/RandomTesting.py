import os
import json
import time
import subprocess
import pandas as pd
from prettytable import PrettyTable

def random_testing(pytest_cmd, mutpy_cmd, random_test_cases):
    #   k% test cases for pairwise technique  
    k = 0
    sol_length = len(random_test_cases)
    
    columns = ["k Test Cases", "Total Tests", "Passed Tests", "Failed Tests", "MT Score"]
    
    # Empty DataFrame with column names
    df = pd.DataFrame(columns=columns)
    
    index = 0
    
    rtTable = PrettyTable()
    rtTable.title = 'Random Testing (RT)'
    rtTable.field_names = ["k Test Cases", "Total Tests", "Passed Tests", "Failed Tests", "MT Score"]
    
    start_rt = 0
    end_rt = 0
    
    while k < 100:
        # ================================================== #
        # Separating Dataset
        # ================================================== #
        k += 10
        dataset_size = round((k/100) * sol_length)
        dataset = []
        if k == 100:
            start_rt = time.time()
        
        for index in range(dataset_size):
            dataset.append(random_test_cases[index])
        if k <= 10:
            print("# ======================================================== #")
            print(f"Random Testing (RT) of {k}% Dataset:")
            print("# ======================================================== #\n")
        else:
            print("\n\n\n# ======================================================== #")
            print(f"Random Testing (RT) of {k}% Dataset:")
            print("# ======================================================== #\n")
            
            
        jsonString = json.dumps(dataset)
        jsonFile = open("./temp/RT_Test_Cases.json", 'w')
        jsonFile.write(jsonString)
        jsonFile.close()
        
        rt_output = subprocess.run(pytest_cmd, capture_output=True)
        rt_output = rt_output.stdout.decode()
        rt_output = rt_output.split('=== RT Result Start ===')
        rt_output = rt_output[1].split('=== RT Result End ===')
        rt_output = rt_output[0]
        rt_output = rt_output.split('\r\n')

        rt_passed = rt_output[1]
        rt_passed = rt_passed.split(': ')
        rt_passed = int(rt_passed[1])

        rt_failed = rt_output[2]
        rt_failed = rt_failed.split(': ')
        rt_failed = int(rt_failed[1])
        
        rt_total_tests = rt_passed + rt_failed
        
        print("# ================================= #")
        print("RT Results")
        print("# ================================= #\n")
        
        print(f"Total Tests: {rt_total_tests}")
        print(f"Passed Tests: {rt_passed}")
        print(f"Failed Tests: {rt_failed}\n\n")
        
        print("# ================================= #")
        print("RT Result: Mutation Testing (MT)")
        print("# ================================= #\n")
        
        rt_mt_output = subprocess.check_output(mutpy_cmd, shell=True, universal_newlines=True)
        rt_mt_output = rt_mt_output.split('[*]')
        rt_mt_output = rt_mt_output[-1]
        
        rt_mt_rslt = rt_mt_output.split(": ")
        rt_mt_rslt = rt_mt_rslt[1].split('\n')
        rt_mt_rslt = rt_mt_rslt[0]

        print(rt_mt_output)
        
        tbl_row_data = [f"{k}%", rt_total_tests, rt_passed, rt_failed, rt_mt_rslt]
        df.loc[index] = tbl_row_data
        
        index += 1
        rtTable.add_row([f"{k}%", rt_total_tests, rt_passed, rt_failed, rt_mt_rslt])
        
        if k == 100:
            end_rt = time.time()
            
            total_time_rt = (end_rt - start_rt)

    print(f"\n\n{rtTable}")
    df = df.reset_index(drop=True)
    os.remove("./temp/RT_Test_Cases.json")
    os.remove("./temp/RT_Values.json")
    
    rsltObj = {'RT_DataFrame': df, 'RT_Overhead': total_time_rt}
    
    return rsltObj