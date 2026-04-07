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

def features_csv():
