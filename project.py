import os
import subprocess
import random
import constraint
import json
import time
import math
from decimal import Decimal
import pandas as pd
from IPython.display import display
import plotly.express as px
from prettytable import PrettyTable
from tracing import path_trace


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def dynamic_symbolic_execution(code, inputs):
    symbolic_inputs = [None, None]

    stack = [code]
    while stack:
        current_func = stack.pop()
        try:
            result = current_func(*inputs)
        except Exception as e:
            # print(f"An exception occurred: {e}")
            continue

        if isinstance(result, int) == False:
            stack.append(result)

        for i, input in enumerate(inputs):
            if isinstance(input, int):
                symbolic_inputs[i] = input
                    
    return {'x': symbolic_inputs[0], 'y': symbolic_inputs[1], 'z': result}



def padmt_algo(code, constraints, mutPyObj, srcCode):
    #   k% test cases for pairwise technique  
    k = 0
    sol_length = len(constraints)
    
    padmtTable = PrettyTable()
    padmtTable.title = 'PaDMT'
    padmtTable.field_names = ["k Test Cases", "True MRs", "False MRs", "MT Score"]
    
    dseTable = PrettyTable()
    dseTable.title = 'Dynamic Symbolic Execution (DSE)'
    dseTable.field_names = ["k Test Cases", "DSE Value", "DSE vs PaDMTP", "MT Score"]
    
    priTable = PrettyTable()
    priTable.title = 'Prioritized Test Cases'
    priTable.field_names = ["x", "y", "Path Length", "PaDMTP"]
    
    poTable = PrettyTable()
    poTable.title = 'Overhead of Source Test Case Generation'
    poTable.field_names = ["k Test Cases", "PaDMTP", "DSE", "PO Value"]
    
    while k < 100:
        # ================================================== #
        # Separating Dataset
        # ================================================== #
        k += 10
        dataset_size = round((k/100) * sol_length)
        dataset = []
        
        start_padmt = time.time()
        
        for index in range(dataset_size):
            dataset.append(constraints[index])
            
        # ================================================== #
        # Execution Path Analysis
        # ================================================== #
        epa_result = []
        for index, value in enumerate(dataset):
            data = {'x': value['x'], 'y': value['y']}
            path_trace_obj = path_trace(code, data)
            epa_result.append(path_trace_obj)
            
        if k <= 10:
            print(f"Execution Path Analysis (EPA) of {k}% Dataset:\n")
        else:
            print(f"\n\n\nExecution Path Analysis (EPA) of {k}% Dataset:\n")

        padmt_val = int(0)

        for x in epa_result:
            padmt_val += int(x['pad-mt'])
        
        print("EPA Value:", padmt_val, "\n")
        
        mr_values = {}
        
        with open('./temp/MR_Values.json', 'w') as f:
            pass
        
        
        print("# ======================================================== #")
        print("Metamorphic Relations")
        print("# ======================================================== #\n")
        
        
        print("# ======================================================== #")
        print("1: Additive (Add a Positive Constant)")
        print("# ======================================================== #\n")
        
        
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
            additive_val += int(val['pad-mt'])
            mr_temp_values.append({'x': val['x'], 'y': val['y'], 'z': val['z']})

        mr_values['additive'] = {}
        mr_values['additive'] = mr_temp_values

        print("Additive Value:", additive_val, "\n")

        additive_mr = False
        if padmt_val == additive_val:
            print("EPA & Additive Values are Equal\n")
            additive_mr = True

        elif padmt_val < additive_val:
            print("Additive Value has Increased\n")
            additive_mr = True

        elif padmt_val > additive_val:
            print("Additive Value has Decreased\n")
            additive_mr = False
        
        
        print("# ======================================================== #")
        print("2: Inclusive (Add a New Element)")
        print("# ======================================================== #\n")
        
        
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
            inclusive_val += int(val['pad-mt'])
            mr_temp_values.append({'x': val['x'], 'y': val['y'], 'z': val['z']})

        mr_values['inclusive'] = {}
        mr_values['inclusive'] = mr_temp_values

        print("Inclusive Value:", inclusive_val, "\n")

        inclusive_mr = False
        if padmt_val == inclusive_val:
            print("EPA & Inclusive Values are Equal\n")
            inclusive_mr = True

        elif padmt_val < inclusive_val:
            print("Inclusive Value has Increased\n")
            inclusive_mr = True

        elif padmt_val > inclusive_val:
            print("Inclusive Value has Decreased\n")
            inclusive_mr = False
        
        
        print("# ======================================================== #")
        print("3: Permutative (Permutate a Value)")
        print("# ======================================================== #\n")
        
        # perm = Decimal(math.perm(sol_length, dataset_size))
        # random_val = random.randint(0, 2)

        # perm = Decimal(math.perm( , sol_length))
        # sig_num = '{:.3e}'.format(perm)
        # val = sig_num.split('.')
        # val = int(val[0])
        
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
#             permutative_vals.append({'x': int(1 / sel['x']), 'y': int(1 / sel['y'])})
        
        permutative_result = []\
        
        for index, value in enumerate(permutative_vals):
            data = {'x': value['x'], 'y': value['y']}
            path_trace_obj = path_trace(code, data)
            permutative_result.append(path_trace_obj)

        mr_temp_values = []
        
        permutative_value = int(0)

        for val in permutative_result:
            permutative_value += int(val['pad-mt'])
            mr_temp_values.append({'x': val['x'], 'y': val['y'], 'z': val['z']})

        mr_values['permutative'] = {}
        mr_values['permutative'] = mr_temp_values

        print("Permutative Value:", permutative_value, "\n")

        permutative_mr = False
        if padmt_val == permutative_value:
            print("EPA & Permutative Values are Equal\n")
            permutative_mr = True

        elif padmt_val < permutative_value:
            print("Permutative Value has Increased\n")
            permutative_mr = False

        elif padmt_val > permutative_value:
            print("Permutative Value has Decreased\n")
            permutative_mr = False
        
        
        print("# ======================================================== #")
        print("4: Multiplicative (Multiply by a Positive Constant)")
        print("# ======================================================== #\n")
        
        
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
            multiplicative_value += int(val['pad-mt'])
            mr_temp_values.append({'x': val['x'], 'y': val['y'], 'z': val['z']})

        mr_values['multiplicative'] = {}
        mr_values['multiplicative'] = mr_temp_values

        print("Multiplicative Value:", multiplicative_value, "\n")

        multiplicative_mr = False
        if padmt_val == multiplicative_value:
            print("EPA & Multiplicative Values are Equal\n")
            multiplicative_mr = True

        elif padmt_val < multiplicative_value:
            print("Multiplicative Value has Increased\n")
            multiplicative_mr = True

        elif padmt_val > multiplicative_value:
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
        
        
        print("# ======================================================== #")
        print("PaDMTP Result: Mutation Testing (MT)")
        print("# ======================================================== #\n")
        
        
        padmt_mt_output = subprocess.check_output(mutPyObj[0], shell=True, universal_newlines=True)
        padmt_mt_output = padmt_mt_output.split('[*]')
        padmt_mt_output = padmt_mt_output[-1]
        
        padmt_mt_rslt = padmt_mt_output.split(": ")
        padmt_mt_rslt = padmt_mt_rslt[1].split('\n')
        padmt_mt_rslt = padmt_mt_rslt[0]

        print(padmt_mt_output)
        
        padmtTable.add_row([f"{k}%", true_MRs, false_MRs, padmt_mt_rslt])
        
        end_padmt = time.time()
        
        print("# ======================================================== #")
        print("Dynamic Symbolic Execution (DSE)")
        print("# ======================================================== #\n")
        
        start_dse = time.time()
        
        dse_selected = []
        dse_result = []
        
        dse_index = []
        
        for x in range(len(dataset)):
            ind = random.randint(0, len(dataset) - 1)
    
            while(ind in dse_index):
                ind = random.randint(0, len(dataset) - 1)
            dse_index.append(ind)
            dse_selected.append(dataset[ind])
        
        
        for index, value in enumerate(dse_selected):
            inputs = [value['x'], value['y']]
            result = dynamic_symbolic_execution(code, inputs)
            dse_result.append(result)
            
        dse_val = int(0)        
        dse_values = []

        for x in dse_result:
            dse_val += int(x['z'])
            dse_values.append({'x': val['x'], 'y': val['y'], 'z': val['z']})
        
        print("Dynamic Symbolic Execution Value:", dse_val, "\n")

        with open('./temp/DSE_Values.json', 'w') as f:
            pass

        
        # Random Testing: Saving Values to File

        jsonString = json.dumps(dse_values)
        jsonFile = open("./temp/DSE_Values.json", 'w')
        jsonFile.write(jsonString)
        jsonFile.close()
        
        
        print("# ======================================================== #")
        print("DSE Result: Mutation Testing (MT)")
        print("# ======================================================== #\n")
        
        
        dse_mt_output = subprocess.check_output(mutPyObj[3], shell=True, universal_newlines=True)
        dse_mt_output = dse_mt_output.split('[*]')
        dse_mt_output = dse_mt_output[-1]
        
        dse_mt_rslt = dse_mt_output.split(": ")
        dse_mt_rslt = dse_mt_rslt[1].split('\n')
        dse_mt_rslt = dse_mt_rslt[0]

        print(dse_mt_output)
        
        dse_vs_padmt = dse_val/padmt_val
        
        if(dse_vs_padmt < 0):
            dse_vs_padmt *= -1
        
        dseTable.add_row([f"{k}%", dse_val, dse_vs_padmt, dse_mt_rslt])
        
        end_dse = time.time()
        
        if k == 100:
            sortedData = []

            for index, value in enumerate(epa_result):
                sortedData.append({'x': epa_result[index]['x'], 'y': epa_result[index]['y'], 'length': epa_result[index]['length'], 'padmt': epa_result[index]['pad-mt']})

            # Create DataFrame
            prioritizedTestCases = pd.DataFrame(sortedData) 
            prioritizedTestCases = prioritizedTestCases.sort_values(by=['padmt'], ascending=False)
            prioritizedTestCases = prioritizedTestCases.reset_index()
            prioritizedTestCases = prioritizedTestCases.drop(['index'], axis=1)
            
            for index, value in prioritizedTestCases.iterrows():
                priTable.add_row([value['x'], value['y'], value['length'], value['padmt']])
                
            
            total_time_padmt = (end_padmt - start_padmt)
            total_time_dse = (end_dse - start_dse)

            po_val = (total_time_padmt - total_time_dse) / total_time_padmt

#             if po_val < 0:
#                 po_val *= -1

            total_time_padmt *= 1000
            total_time_dse *= 1000

            poTable.add_row([f"{k}%", "%.2f" % total_time_padmt, "%.2f" % total_time_dse, "%.2f" % po_val])
        
    print(f"{padmtTable}\n\n")
    print(f"{dseTable}\n\n")
    print(f"{priTable}\n\n")
    print(f"{poTable}\n\n")
    
    tables = {'padmt': padmtTable, 'dse': dseTable}
    
    kTestCases = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
    colNames = ['K Test Cases', 'PaDMT', 'DSE']
    tableData = []
    faultRate = []

    for index, table in enumerate(tables):
        faultRate = []
        for row in tables[table]:
            row.border = False
            row.header = False
            val = row.get_string(fields=["MT Score"]).strip()
            val = val.split(' \n ')
            faultRate.append(val[1].strip())
        tableData.append(faultRate)

    dfData = []

    for index, value in enumerate(kTestCases):
        dfData.append([value, tableData[0][index], tableData[3][index]])
    
    df = pd.DataFrame(dfData, columns=colNames)
    
    padmtFig = px.line(
        df, 
        x='K Test Cases', 
        y=[df['PaDMT'], df['DSE']], 
        text='value',
        labels={
            "value": "Fault Detection Rate",
            "variable": "Test Type"
        },
    )
    padmtFig.update_traces(textposition="bottom center")
    padmtFig.update_layout(
        autosize=False,
        width=950,
        height=350,
        margin=dict(l=0, r=0, t=0, b=0),
        autotypenumbers='convert types'
    )
    padmtFig.show()
    
    os.remove("./temp/DSE_Values.json")
    os.remove("./temp/MR_Values.json")
        
