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

#csv_path = '../outputCSV/tableSTA.csv'

circuit = "c17.v"
exemples = "./makeCombinations"

def get_code(string):
    return string.split("_", 1)[0]

def is_dir_empty(path):
    return not any(os.scandir(path))

def format_cells(cells_dict):
    result = {}
    for cid in sorted(cells_dict.keys()):
        result[cid] = "-".join(str(c) for c in cells_dict[cid])
    return result


def _norm_cell_id(x) -> str:
    # Garante comparação consistente entre '4' e 4
    return str(x).strip()

def process_out_path(cells_dict):
    # Achata todas as células dos caminhos críticos e normaliza para string
    vals = []
    for cid in sorted(cells_dict.keys()):
        vals.extend(cells_dict[cid])

    # Remove duplicados SEM perder a ordem
    seen = set()
    critical = []
    for v in vals:
        s = _norm_cell_id(v)
        if s not in seen:
            seen.add(s)
            critical.append(s)

    print(f"Cp -> {critical}")
    return critical

def out_path(circuit_cells, cells_dict):
    # circuit_cells pode já estar em string, mas normalizamos igual
    design = [_norm_cell_id(c) for c in circuit_cells]
    print(f"design cells -> {design}")

    critical_paths = set(process_out_path(cells_dict))  # strings
    dif = [c for c in design if c not in critical_paths]  # mantém ordem do design
    return dif


gio = readV.Get_IO(circuit, exemples)

# número de saídas do circuito (quantas colunas arrival_i/path_i/gains_i criar)
number_coluns = len(gio.get_outputs())

arrives_coluns = makeCSV.Generete_coluns(number_coluns).create_arrives_coluns()
paths_coluns   = makeCSV.Generete_coluns(number_coluns).create_paths_coluns()
gains_coluns   = makeCSV.Generete_coluns(number_coluns).create_gains_coluns()

circuit_cells = gio.get_cells_ids()
print(circuit_cells)


"""""
def circuit_table(csv_name, arrives, paths, gains):
    coluns_list = [
        'circuit',
        'design',
        'size_gates',
        'cells_out_path'
    ]

    desing_coluns_list = coluns_list + arrives + paths + gains

    makeCSV.Create_table.make_csv(desing_coluns_list, )

    
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
    
    makeCSV.Create_table.make_csv(coluns_list, )
"""



# Evita de rodar o sta toda hora
if is_dir_empty(design_path):
    runSTA.run_sta()




for sta_file in files:
    full_path = os.path.join(design_path, sta_file)
    rt = extData.Read_timing(full_path)
    
    code = get_code(sta_file)  
    circuit_file = f"{code}_c17.v"
    
    number_gates = readV.number_gates(circuit_file, dir_circuits)
    sized_gates = Decoder.get_sequence(number_gates, int(code))

    arrivals = rt.get_arrival_times()
    cells = rt.get_cells()
    
    # Formata células como string separada por -
    cells_formatted = format_cells(cells)
    
    
    # Vou usar a lista de gates para comparar depois aqueles que estão fora do caminho crítico
    desig_cells = gio.get_cells_ids()

    teste = out_path(desig_cells, cells)
    print(f"outPath -> {teste}")





    #design_outputs = readV.Get_IO.get_outputs(circuit_file, dir_circuits)

    #print(cells)








"""""
    # Extrai dados dos caminhos críticos (1 e 2)
    arrival_1 = arrivals.get(1, "-")
    arrival_2 = arrivals.get(2, "-")
    cells_p1 = cells_formatted.get(1, "")
    cells_p2 = cells_formatted.get(2, "")
    
    # Formata sizes como string 
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

    addition1, addition2 = getGains.walk_csv(csv_path)

    makeCSV.insert_gains(addition1, addition2)
"""

