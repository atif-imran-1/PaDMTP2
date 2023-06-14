import os
import json
import time
import subprocess
import pandas as pd
from prettytable import PrettyTable
from techniques.art_original import apply_art as MyCode_ART
from techniques.art_hcf import apply_art as HCF_ART
from techniques.art_lcm import apply_art as LCM_ART
from techniques.art_difference import apply_art as DIFF_ART

def adaptive_random_testing(code, mutpy_cmd, art_test_cases, program):
    #   k% test cases for pairwise technique  
    k = 0
    sol_length = len(art_test_cases)
    
    columns = ["k Test Cases", "Total Tests", "Passed Tests", "Failed Tests", "MT Score"]
    
    # Empty DataFrame with column names
    df = pd.DataFrame(columns=columns)
    
    index = 0
    
    artTable = PrettyTable()
    artTable.title = 'Adaptive Random Testing (ART)'
    artTable.field_names = ["k Test Cases", "Total Tests", "Passed Tests", "Failed Tests", "MT Score"]
    
    start_art = 0
    end_art = 0

    while k < 100:
        # ================================================== #
        # Separating Dataset
        # ================================================== #
        k += 10
        dataset_size = round((k/100) * sol_length)
        dataset = []
        if k == 100:
            start_art = time.time()
        
        for index in range(dataset_size):
            dataset.append(art_test_cases[index])
        if k <= 10:
            print("# ======================================================== #")
            print(f"Adaptive Random Testing (ART) of {k}% Dataset:")
            print("# ======================================================== #\n")
        else:
            print("\n\n\n# ======================================================== #")
            print(f"Adaptive Random Testing (ART) of {k}% Dataset:")
            print("# ======================================================== #\n")

        art_rslts = {}

        if program == 'MyCode':
            art_rslts = MyCode_ART(code, dataset)
        elif program == 'HCF':
            art_rslts = HCF_ART(code, dataset)
        elif program == 'LCM':
            art_rslts = LCM_ART(code, dataset)
        elif program == 'DIFF':
            art_rslts = DIFF_ART(code, dataset)

        print("# ================================= #")
        print("RT Results")
        print("# ================================= #\n")
        
        art_total_tests = art_rslts[1] + art_rslts[2]
        print(f"Total Tests: {art_total_tests}")
        print(f"Passed Tests: {art_rslts[1]}")
        print(f"Failed Tests: {art_rslts[2]}\n\n")
        
        jsonString = json.dumps(art_rslts[0])
        jsonFile = open("./temp/ART_Values.json", 'w')
        jsonFile.write(jsonString)
        jsonFile.close()

        print("# ================================= #")
        print("RT Result: Mutation Testing (MT)")
        print("# ================================= #\n")
        
        art_mt_output = subprocess.check_output(mutpy_cmd, shell=True, universal_newlines=True)
        art_mt_output = art_mt_output.split('[*]')
        art_mt_output = art_mt_output[-1]
        
        art_mt_rslt = art_mt_output.split(": ")
        art_mt_rslt = art_mt_rslt[1].split('\n')
        art_mt_rslt = art_mt_rslt[0]

        print(art_mt_output)

        tbl_row_data = [f"{k}%", art_total_tests, art_rslts[1], art_rslts[2], art_mt_rslt]
        df.loc[index] = tbl_row_data
        
        index += 1
        artTable.add_row([f"{k}%", art_total_tests, art_rslts[1], art_rslts[2], art_mt_rslt])
        
        if k == 100:
            end_art = time.time()
            
            total_time_art = (end_art - start_art)

    print(f"\n\n{artTable}")
    df = df.reset_index(drop=True)
    os.remove("./temp/ART_Values.json")
    
    rsltObj = {'ART_DataFrame': df, 'ART_Overhead': total_time_art}
    
    return rsltObj