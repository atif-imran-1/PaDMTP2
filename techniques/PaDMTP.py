import os
import math
import time
import json
import random
import subprocess
import pandas as pd
from decimal import Decimal
from techniques.tracing import path_trace
from prettytable import PrettyTable


def padmtp_algo(code, constraints, mutPyObj):
    #   k% test cases for pairwise technique  
    k = 0
    sol_length = len(constraints)
    
    padmtpTable = PrettyTable()
    padmtpTable.title = 'PaDMTP'
    padmtpTable.field_names = ["k Test Cases", "True MRs", "False MRs", "MT Score"]

    priTable = PrettyTable()
    priTable.title = 'Prioritized Test Cases'
    priTable.field_names = ["x", "y", "Path Length"]
    
    columns = ["k Test Cases", "True MRs", "False MRs", "MT Score"]
    
    # Empty DataFrame with column names
    padmtp_table = pd.DataFrame(columns=columns)
    
    index = 0

    start_padmtp = 0
    end_padmtp = 0
    
    while k < 100:
        # ================================================== #
        # Separating Dataset
        # ================================================== #
        k += 10
        dataset_size = round((k/100) * sol_length)
        dataset = []
        
        if k == 100:
            start_padmtp = time.time()
        
        for index in range(dataset_size):
            dataset.append(constraints[index])

        # ================================================== #
        # Source Test Case Execution (STCE)
        # ================================================== #
        stce_result = []
        for index, value in enumerate(dataset):
            data = {'x': value['x'], 'y': value['y']}
            path_trace_obj = path_trace(code, data)
            stce_result.append(path_trace_obj)
            
        if k <= 10:
            print("# ====================================================================== #")
            print(f"Source Test Case Execution (STCE) of {k}% Dataset:")
            print("# ====================================================================== #\n")
        else:
            print("\n\n\n# ====================================================================== #")
            print(f"Source Test Case Execution (STCE) of {k}% Dataset:")
            print("# ====================================================================== #\n")

        stce_val = int(0)

        for x in stce_result:
            stce_val += int(x['z'])
        
        print("STCE (Sum of Results):", stce_val, "\n")
        
        mr_values = {}
        
        with open('./temp/MR_Values.json', 'w') as f:
            pass

        print("# ============================================================ #")
        print("Metamorphic Relations")
        print("# ============================================================ #\n")
        
        
        print("# ======================================================= #")
        print("1: Additive (Add a Positive Constant)")
        print("# ======================================================= #\n")
        
        
        additive_vals = []
        ind = random.randint(1, 9)

        for sel in dataset:
            additive_vals.append({'x': sel['x'] + ind, 'y': sel['y'] + ind})
        
        additive_result = []
        
        for index, value in enumerate(additive_vals):
            data = {'x': value['x'], 'y': value['y']}
            path_trace_obj = path_trace(code, data)
            additive_result.append(path_trace_obj)

        mr_temp_values = []
        
        additive_val = int(0)

        for val in additive_result:
            additive_val += int(val['z'])
            mr_temp_values.append({'x': val['x'], 'y': val['y'], 'z': val['z']})

        mr_values['additive'] = {}
        mr_values['additive'] = mr_temp_values

        print("Additive Value:", additive_val, "\n")

        additive_mr = False
        if stce_val == additive_val:
            print("EPA & Additive Values are Equal\n")
            additive_mr = True

        elif stce_val < additive_val:
            print("Additive Value has Increased\n")
            additive_mr = True

        elif stce_val > additive_val:
            print("Additive Value has Decreased\n")
            additive_mr = False
        
        
        print("# ======================================================= #")
        print("2: Inclusive (Add a New Element)")
        print("# ======================================================= #\n")
        
        
        inclusive_vals = []
        for sel in dataset:
            inclusive_vals.append({'x': sel['x'], 'y': sel['y'], 'inc': random.randint(0, len(dataset))})
        
        inclusive_result = []

        for index, value in enumerate(inclusive_vals):
            data = {'x': value['x'], 'y': value['y'], 'inc': value['inc']}
            path_trace_obj = path_trace(code, data)
            inclusive_result.append(path_trace_obj)

        mr_temp_values = []
        
        inclusive_val = int(0)

        for val in inclusive_result:
            inclusive_val += int(val['z'])
            mr_temp_values.append({'x': val['x'], 'y': val['y'], 'z': val['z']})

        mr_values['inclusive'] = {}
        mr_values['inclusive'] = mr_temp_values

        print("Inclusive Value:", inclusive_val, "\n")

        inclusive_mr = False
        if stce_val == inclusive_val:
            print("EPA & Inclusive Values are Equal\n")
            inclusive_mr = True

        elif stce_val < inclusive_val:
            print("Inclusive Value has Increased\n")
            inclusive_mr = True

        elif stce_val > inclusive_val:
            print("Inclusive Value has Decreased\n")
            inclusive_mr = False
        
        
        print("# ======================================================= #")
        print("3: Permutative (Permutate a Value)")
        print("# ======================================================= #\n")
        
        permutative_vals = []
        for sel in dataset:
            random_val = random.randint(0, 1)
            num_x = int(0)
            num_y = int(0)

            if random_val == 0:
                if sel['x'] < 0:
                    num_x = sel['x'] * -1
                else:
                    num_x = sel['x']

                perm = Decimal(math.perm(sol_length , num_x))
                sig_num = '{:.3e}'.format(perm)
                sig_num = sig_num.split('e+')
                sig_num = float(sig_num[0])
                sig_num *= 10
                sig_num = str(sig_num)
                sig_num = sig_num.split('.')
                num_x = int(sig_num[0])
                num_y = sel['y']

            elif random_val == 1:
                if sel['y'] < 0:
                    num_y = sel['y'] * -1
                else:
                    num_y = sel['y']

                perm = Decimal(math.perm(sol_length , num_y))
                sig_num = '{:.3e}'.format(perm)
                sig_num = sig_num.split('e+')
                sig_num = float(sig_num[0])
                sig_num *= 10
                sig_num = str(sig_num)
                sig_num = sig_num.split('.')
                num_x = sel['x']
                num_y = int(sig_num[0])

            permutative_vals.append({'x': num_x, 'y': num_y})
        
        permutative_result = []
        
        for index, value in enumerate(permutative_vals):
            data = {'x': value['x'], 'y': value['y']}
            path_trace_obj = path_trace(code, data)
            permutative_result.append(path_trace_obj)

        mr_temp_values = []
        
        permutative_value = int(0)

        for val in permutative_result:
            permutative_value += int(val['z'])
            mr_temp_values.append({'x': val['x'], 'y': val['y'], 'z': val['z']})

        mr_values['permutative'] = {}
        mr_values['permutative'] = mr_temp_values

        print("Permutative Value:", permutative_value, "\n")

        permutative_mr = False
        if stce_val == permutative_value:
            print("EPA & Permutative Values are Equal\n")
            permutative_mr = True

        elif stce_val < permutative_value:
            print("Permutative Value has Increased\n")
            permutative_mr = False

        elif stce_val > permutative_value:
            print("Permutative Value has Decreased\n")
            permutative_mr = False
        
        
        print("# ======================================================= #")
        print("4: Multiplicative (Multiply by a Positive Constant)")
        print("# ======================================================= #\n")
        
        
        multiplicative_vals = []
        multiple = random.randint(1, 9)
        for sel in dataset:
            multiplicative_vals.append({'x': sel['x'] * multiple, 'y': sel['y'] * multiple})
            
        multiplicative_result = []
        
        for index, value in enumerate(multiplicative_vals):
            data = {'x': value['x'], 'y': value['y'], 'index': index}
            path_trace_obj = path_trace(code, data)
            multiplicative_result.append(path_trace_obj)

        mr_temp_values = []
        
        multiplicative_value = int(0)

        for val in multiplicative_result:
            multiplicative_value += int(val['z'])
            mr_temp_values.append({'x': val['x'], 'y': val['y'], 'z': val['z']})

        mr_values['multiplicative'] = {}
        mr_values['multiplicative'] = mr_temp_values

        print("Multiplicative Value:", multiplicative_value, "\n")

        multiplicative_mr = False
        if stce_val == multiplicative_value:
            print("EPA & Multiplicative Values are Equal\n")
            multiplicative_mr = True

        elif stce_val < multiplicative_value:
            print("Multiplicative Value has Increased\n")
            multiplicative_mr = True

        elif stce_val > multiplicative_value:
            print("Multiplicative Value has Decreased\n")
            multiplicative_mr = False

        # ======================================================== #
        # Results: Metamorphic Relations
        # ======================================================== #
        
        
        # Specify the Column Names while initializing the Table
        mrTable = PrettyTable()
        mrTable.title = "Results: Metamorphic Relations (MRs)"
        mrTable.field_names = ["Metamorphic Relations", "r1", "r2", "Our_Result"]
        mrTable.add_row(["Additive", "Add a positive constant", "Increase or Remain", additive_mr])
        mrTable.add_row(["Inclusive", "Add a new Element ", "Increase or Remain", inclusive_mr])
        mrTable.add_row(["Permutative", "Permutate a Value", "Remain", permutative_mr])
        mrTable.add_row(["Multiplicative", "Multiply by a constant ", "Increase or Remain", multiplicative_mr])
        
        print(f"\n{mrTable}\n")
        
        table_data = []
        for row in mrTable:
            row.border = False
            row.header = False
            row.title = False
            
            value = row.get_string(fields=["Our_Result"]).strip()
            value = value.split('\n ')
            value = value[1]
            
            table_data.append(value)

        true_MRs = int(0)
        false_MRs = int(0)
        
        for x in table_data:
            if x == 'True':
                true_MRs += 1
            elif x == 'False':
                false_MRs += 1
        
        # Metamorphic Relations: Saving Values to File

        jsonString = json.dumps(mr_values)
        jsonFile = open("./temp/MR_Values.json", 'w')
        jsonFile.write(jsonString)
        jsonFile.close()

        print("# ======================================================= #")
        print("PaDMTP Result: Mutation Testing (MT)")
        print("# ======================================================= #\n")
        
        
        padmtp_mt_output = subprocess.check_output(mutPyObj, shell=True, universal_newlines=True)
        padmtp_mt_output = padmtp_mt_output.split('[*]')
        padmtp_mt_output = padmtp_mt_output[-1]
        
        padmtp_mt_rslt = padmtp_mt_output.split(": ")
        padmtp_mt_rslt = padmtp_mt_rslt[1].split('\n')
        padmtp_mt_rslt = padmtp_mt_rslt[0]

        print(padmtp_mt_output)
        
        tbl_row_data = [f"{k}%", true_MRs, false_MRs, padmtp_mt_rslt]
        padmtpTable.add_row(tbl_row_data)
        
        padmtp_table.loc[index] = tbl_row_data
        index += 1
        

        if k == 100:
            sortedData = []

            for index, value in enumerate(stce_result):
                sortedData.append({'x': stce_result[index]['x'], 'y': stce_result[index]['y'], 'length': stce_result[index]['length']})

            # Create DataFrame
            prioritizedTestCases = pd.DataFrame(sortedData) 
            prioritizedTestCases = prioritizedTestCases.sort_values(by=['length'], ascending=False)
            prioritizedTestCases = prioritizedTestCases.reset_index()
            prioritizedTestCases = prioritizedTestCases.drop(['index'], axis=1)
            
            for index, value in prioritizedTestCases.iterrows():
                priTable.add_row([value['x'], value['y'], value['length']])

            end_padmtp = time.time()
            
            total_time_padmtp = (end_padmtp - start_padmtp)

    print(f"{padmtpTable}\n\n")
    print(f"{priTable}\n\n")
    padmtp_table = padmtp_table.reset_index(drop=True)
    os.remove("./temp/MR_Values.json")

    rsltObj = {'PaDMTP_DataFrame': padmtp_table, 'PaDMTP_Overhead_STCP': total_time_padmtp, 'PaDMTP_Overhead_STCG': 0}
    
    return rsltObj