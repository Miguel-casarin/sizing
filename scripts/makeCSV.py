import csv
import os

class Create_table:
    def __init__(self, coluns_list, csv_dir, csv_path):
        self.coluns_list = coluns_list
        self.csv_dir = csv_dir
        self.csv_path = csv_path

    def make_csv(self):
        os.makedirs(self.csv_dir, exist_ok=True)
        with open(self.csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(self.coluns_list)


# Aloca o número necessário de colunas para valores que aumentam conforme o design
class Generete_coluns:
    def __init__(self, number_gates):
        self.number_gates = int(number_gates)

    def create_arrives_coluns(self):
        names_list = []
        for i in range(1, self.number_gates + 1):
            names_list.append(f'arrival_{i}')
        return names_list

    def create_paths_coluns(self):
        names_list = []
        for i in range(1, self.number_gates + 1):
            names_list.append(f'path_{i}')
        return names_list

    def create_gains_coluns(self):
        names_list = []
        for i in range(1, self.number_gates + 1):
            names_list.append(f'gains_{i}')
        return names_list


class Edit_csv:
    def __init__(self, csv_path, data):
        self.csv_path = csv_path
        self.data = data

    def insert_csv_data(self):
        with open(self.csv_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.data)

#csv_dir = './outputCSV'
#csv_path = os.path.join(csv_dir, 'tableSTA.csv')

#features_csv_path = os.path.join(csv_dir, 'featuresDesign.csv')


