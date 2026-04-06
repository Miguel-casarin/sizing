import os

from scripts import extData
from scripts import dir
from scripts import Decoder
from scripts import runSTA
from scripts import readV
from scripts import makeCSV

design_path = "./staOutputs"
files = dir.get_files(design_path)
dir_circuits = 'inputs/'

def get_code(string):
    return string.split("_", 1)[0]

def is_dir_empty(path):
    return not any(os.scandir(path))

def format_cells(cells_dict):
    """Formata células por caminho crítico: p1: 1-2-3, p2: 4-5-6"""
    result = {}
    for cid in sorted(cells_dict.keys()):
        cell_ids = [c['cell_id'].strip('_') for c in cells_dict[cid]]
        result[cid] = '-'.join(cell_ids)
    return result

# Evita de rodar o sta toda hora
if is_dir_empty(design_path):
    runSTA.run_sta()
    
for sta_file in files:
    full_path = os.path.join(design_path, sta_file)
    rt = extData.Read_timing(full_path)
    
    code = get_code(sta_file)  
    circuit_file = f"{code}_c17.v"
    
    # Passa os parâmetros corretos
    number_gates = readV.number_gates(circuit_file, dir_circuits)
    sized_gates = Decoder.get_sequence(number_gates, int(code))

    arrivals = rt.get_arrival_times()
    cells = rt.get_cells()
    
    # Formata células como string separada por -
    cells_formatted = format_cells(cells)
    
    # Extrai dados dos caminhos críticos (1 e 2)
    arrival_1 = arrivals.get(1, "-")
    arrival_2 = arrivals.get(2, "-")
    cells_p1 = cells_formatted.get(1, "")
    cells_p2 = cells_formatted.get(2, "")
    
    # Formata sizes como string (se sized_gates for lista)
    if isinstance(sized_gates, list):
        size_gates = '-'.join(str(s) for s in sized_gates)
    else:
        size_gates = str(sized_gates)

    # Monta dados para CSV
    data = [
        'c17',           # circuit
        code,            # design
        arrival_1,       # arrival_1
        arrival_2,       # arrival_2
        cells_p1,        # cells_p1
        cells_p2,        # cells_p2
        size_gates       # size_gates
    ]
    
    # Insere no CSV
    makeCSV.insert_csv(data)
    
    print(f"✓ {sta_file} adicionado ao CSV")

