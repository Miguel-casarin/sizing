import os

from scripts import extData
from scripts import dir
from scripts import Decoder
from scripts import runSTA
from scripts import readV
from scripts import makeCSV
from scripts import getGains

design_path = "./staOutputs"
files = dir.get_files(design_path)
dir_circuits = 'inputs/'
verilog = "c17.v"
csv_name = verilog.split(".")[0]

csv_dir = './outputCSV'
csv_path = os.path.join(csv_dir, f'{csv_name}.csv')

def get_code(string):
    return string.split("_", 1)[0]

def is_dir_empty(path):
    return not any(os.scandir(path))

def format_cells(cells_dict):
    result = {}
    for cid in sorted(cells_dict.keys()):
        result[cid] = "-".join(str(c) for c in cells_dict[cid])
    return result


def norm_cell_id(x) -> str:
    # Garante comparação consistente entre '4' e 4
    return str(x).strip()

def process_out_path(cells_dict):
    vals = []
    for cid in sorted(cells_dict.keys()):
        vals.extend(cells_dict[cid])

    seen = set()
    critical = []
    for v in vals:
        s = norm_cell_id(v)
        if s not in seen:
            seen.add(s)
            critical.append(s)

    #print(f"Cp -> {critical}")
    return critical

def out_path(circuit_cells, cells_dict):
    design = [norm_cell_id(c) for c in circuit_cells]
    print(f"design cells -> {design}")

    critical_paths = set(process_out_path(cells_dict))  
    dif = [c for c in design if c not in critical_paths]  
    return dif

def circuit_table(csv_dir, csv_path, arrives, paths, gains):
    coluns_list = [
        'circuit',
        'design',
        'power',
        'size_gates',
        'cells_out_path'
    ]

    desing_coluns_list = coluns_list + arrives + paths + gains

    makeCSV.Create_table(desing_coluns_list, csv_dir, csv_path).make_csv()

    
def features_table(csv_name):
    coluns_list = [
        'design',
        'cell',
        'type',
        'fain',
        'faout',
        'nl',
        'deep'
    ]
    
    makeCSV.Create_table(coluns_list, csv_dir, csv_path).make_csv()



# Evita de rodar o sta toda hora
if is_dir_empty(design_path):
    runSTA.run_sta()

gio = readV.Get_IO(f'0_{verilog}', dir_circuits)

# número de saídas do circuito (quantas colunas arrival_i/path_i/gains_i criar)
number_coluns = len(gio.get_outputs())

arrives_coluns = makeCSV.Generete_coluns(number_coluns).create_arrives_coluns()
paths_coluns   = makeCSV.Generete_coluns(number_coluns).create_paths_coluns()
gains_coluns   = makeCSV.Generete_coluns(number_coluns).create_gains_coluns()


circuit_cells = gio.get_cells_ids()

circuit_table(csv_dir, csv_path, arrives_coluns, paths_coluns, gains_coluns)


for sta_file in files:
    full_path = os.path.join(design_path, sta_file)
    rt = extData.Read_timing(full_path)
    
    code = get_code(sta_file)  
    circuit_file = f"{code}_c17.v"
    
    number_gates = readV.number_gates(circuit_file, dir_circuits)
    sized_gates = Decoder.get_sequence(number_gates, int(code))

    arrivals = rt.get_arrival_times()
    cells = rt.get_cells()
    power = rt.get_power()
    
    
    # Formata células como string separada por -
    cells_formatted = format_cells(cells)
    
    # Vou usar a lista de gates para comparar depois aqueles que estão fora do caminho crítico
    design_cells = gio.get_cells_ids()

    out_path_cells = out_path(design_cells, cells)
    #print(out_path_cells)
   
    design_outputs = readV.Get_IO(circuit_file, dir_circuits).get_outputs()

