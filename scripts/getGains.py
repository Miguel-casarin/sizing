import pandas as pd 
import csv

def walk_csv(csv_file):
    df = pd.read_csv(csv_file)
    
    df['arrival_1'] = pd.to_numeric(df['arrival_1'])
    df['arrival_2'] = pd.to_numeric(df['arrival_2'])

    base_line1 = pd.to_numeric(df.loc[0, 'arrival_1'])   
    base_line2 = pd.to_numeric(df.loc[0, 'arrival_2'])  

    list_gains1 = []
    list_gains2 = []

    for i, line in df.iterrows():
        #design = line['design']
        arivel1 = pd.to_numeric(line['arrival_1'])
        arivel2 = pd.to_numeric(line['arrival_2'])

        gain1 = round(arivel1 - base_line1, 6)
        gain2 = round(arivel2 - base_line2, 6)
        
        list_gains1.append(gain1)
        list_gains2.append(gain2)
    
    return list_gains1, list_gains2
        

csv_path = '../outputCSV/tableSTA.csv'


def first_csv_line(table):
    with open(table, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        first_line = next(reader)

    return first_line


def filter_values(line, column, number_outputs):
    base_lines = {}

    for i in range(1, number_outputs+1):
        string = f'{column}_{i}'

        for key in line:
            if key.startswith(string):
                base_lines[key] = line[key]

    return base_lines

def calculet_adiction(csv_file, dic_baselines, number_outputs, ndigits=6):
    arrival_cols = [f"arrival_{i}" for i in range(1, number_outputs + 1)]
    df = pd.read_csv(csv_file, usecols=arrival_cols)

    dic_gains = {}

    for i in range(1, number_outputs + 1):
        arrives = f"arrival_{i}"
        gains_col = f"gains_{i}"  

        baseline = pd.to_numeric(dic_baselines[arrives], errors="coerce")
        values = pd.to_numeric(df[arrives], errors="coerce")  

        dic_gains[gains_col] = (values - baseline).round(ndigits).tolist()

    return dic_gains

