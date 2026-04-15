import os

from scripts import extData
from scripts import dir
from scripts import Decoder
from scripts import runSTA
from scripts import readV
from scripts import makeCSV
from scripts import calculetArea
from scripts import getGains

design_path = "./staOutputs"
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
        'circuit_area',
        'cells_out_path'
    ]

    desing_coluns_list = coluns_list + arrives + paths + gains
    makeCSV.Create_table(desing_coluns_list, csv_dir, csv_path).make_csv()

def build_arrival_values(arrivals: dict, number_coluns: int):
    """
    arrivals é dict onde a chave é o índice da coluna.
    Suporta chaves 0-based (0..n-1) ou 1-based (1..n).
    Retorna lista alinhada com arrival_0..arrival_{n-1}.
    """
    vals = [""] * number_coluns
    if not isinstance(arrivals, dict) or number_coluns <= 0:
        return vals

    keys = []
    for k in arrivals.keys():
        try:
            keys.append(int(k))
        except Exception:
            pass

    if not keys:
        return vals

    # Detecta se é 1-based: não tem 0 e tem 'n' como chave típica
    one_based = (0 not in keys) and (number_coluns in keys)

    for k, v in arrivals.items():
        try:
            idx = int(k)
        except Exception:
            continue

        if one_based:
            idx -= 1  # converte 1..n -> 0..n-1

        if 0 <= idx < number_coluns:
            vals[idx] = v

    return vals

def build_path_values(cells_dict: dict, number_coluns: int):
    """
    cells_dict é dict onde a chave é o índice da coluna (mesma ideia do arrivals).
    Valor pode ser lista de cell_ids (ou algo stringável).
    Retorna lista alinhada com path_0..path_{n-1} (strings do tipo '1-2-3').
    """
    vals = [""] * number_coluns
    if not isinstance(cells_dict, dict) or number_coluns <= 0:
        return vals

    keys = []
    for k in cells_dict.keys():
        try:
            keys.append(int(k))
        except Exception:
            pass

    if not keys:
        return vals

    one_based = (0 not in keys) and (number_coluns in keys)

    for k, path_cells in cells_dict.items():
        try:
            idx = int(k)
        except Exception:
            continue

        if one_based:
            idx -= 1

        if not (0 <= idx < number_coluns):
            continue

        # normaliza para "a-b-c"
        if isinstance(path_cells, (list, tuple)):
            vals[idx] = "-".join(norm_cell_id(c) for c in path_cells)
        else:
            vals[idx] = str(path_cells)

    return vals

def build_row(csv_name, code, power, size_gates, out_path_cells_str, arrival_vals, path_vals, number_coluns):
    return [
        csv_name,
        code,
        power,
        size_gates,
        out_path_cells_str,
        *arrival_vals,
        *path_vals,
        *([""] * number_coluns), 
    ]

# Evita de rodar o sta toda hora
if is_dir_empty(design_path):
    runSTA.run_sta()

files = dir.get_files(design_path)

gio = readV.Get_IO(f'0_{verilog}', dir_circuits)
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
   

    if isinstance(sized_gates, list):
        size_gates = '-'.join(str(s) for s in sized_gates)
    else:
        size_gates = str(sized_gates)

    # Calculo da área 
    cells_area = calculetArea.map_nand_area(sized_gates)
    print(f"AREA DIMISIONS {cells_area}")

    arrivals = rt.get_arrival_times()  # dict: chave = índice da coluna
    cells = rt.get_cells()             # dict: chave = índice da coluna (paths)

    power = rt.get_power()

    design_cells = gio.get_cells_ids()
    out_path_cells = out_path(design_cells, cells)
    out_path_cells_str = "-".join(out_path_cells)

    arrival_vals = build_arrival_values(arrivals, number_coluns)
    path_vals = build_path_values(cells, number_coluns)

    data_to_fill = build_row(
        csv_name=csv_name,
        code=code,
        power=power,
        size_gates=size_gates,
        out_path_cells_str=out_path_cells_str,
        arrival_vals=arrival_vals,
        path_vals=path_vals,
        number_coluns=number_coluns
    )

    makeCSV.Edit_csv(csv_path, data_to_fill).insert_csv_data()

    #ad_gains = getGains.run_gains(csv_path, colun = "gains", )

