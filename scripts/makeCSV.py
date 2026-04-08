import csv
import os

csv_dir = './outputCSV'
csv_path = os.path.join(csv_dir, 'tableSTA.csv')

features_csv_path = os.path.join(csv_dir, 'featuresDesign.csv')

def make_csv():
    os.makedirs(csv_dir, exist_ok=True)

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([
            'circuit',
            'design',
            'arrival_1',
            'arrival_2',
            'cells_p1',
            'cells_p2',
            'size_gates',
            'gain_1',
            'gain_2'
        ])

def insert_csv(data):
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

if not os.path.exists(csv_path):
    make_csv()

# Insere os ganhos
def insert_gains(gains1, gains2, csv_file=csv_path):
    with open(csv_file, "r", newline="") as f:
        rows = list(csv.reader(f))

    header = rows[0]
    data_rows = rows[1:]

    gain1_idx = header.index("gain_1")
    gain2_idx = header.index("gain_2")

    for i, row in enumerate(data_rows):
        if i < len(gains1):
            row[gain1_idx] = str(gains1[i])
        if i < len(gains2):
            row[gain2_idx] = str(gains2[i])

    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_rows)
    

def features_csv():
    os.makedirs(csv_dir, exist_ok=True)

    with open(features_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([
            'design',
            'cell',
            'type',
            'fain',
            'faout',
            'nl',
            'deep'
        ])

def isert_features(data):
    with open(features_csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)