import pandas as pd 

def walk_csv(csv_file):
    df = pd.read_csv(csv_file)
    
    df['arrival_1'] = pd.to_numeric(df['arrival_1'])
    df['arrival_2'] = pd.to_numeric(df['arrival_2'])

    base_line1 = pd.to_numeric(df.loc[0, 'arrival_1'])   
    base_line2 = pd.to_numeric(df.loc[0, 'arrival_2'])  

    for i, line in df.iterrows():
        design = line['design']
        arivel1 = pd.to_numeric(line['arrival_1'])
        arivel2 = pd.to_numeric(line['arrival_2'])

        gain1 = round(arivel1 - base_line1, 6)
        gain2 = round(arivel2 - base_line2, 6)

        print(f"{design} ganho 1 {gain1} - ganho 2 {gain2}")

csv_path = '../outputCSV/tableSTA.csv'
walk_csv(csv_path)