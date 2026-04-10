import re

class Read_timing:
    def __init__(self, sta_file):
        self.sta_file = sta_file 
        
    def get_arrival_times(self):
        arrivals = {}
        path_id = 0
        current_arrival = None
        inside_path = False

        with open(self.sta_file, "r") as f:
            for line in f:
                line = line.strip()

                if line.startswith("Startpoint:"):
                    # salva o caminho anterior
                    if current_arrival is not None:
                        arrivals[path_id] = current_arrival

                    path_id += 1
                    current_arrival = None
                    inside_path = True

                elif "data arrival time" in line and inside_path:
                    if current_arrival is None:  # pega só o primeiro
                        value = float(line.split()[0])
                        if value > 0:
                            current_arrival = value

            # salva o último caminho
            if current_arrival is not None:
                arrivals[path_id] = current_arrival

        return arrivals

    def get_cells(self):
        pcritic_id = 0
        result = {}

        pattern_cells = re.compile(r"_(\d+)_")

        with open(self.sta_file, "r") as f:
            for line in f:
                line = line.strip()

                if line.startswith("Startpoint"):
                    pcritic_id += 1
                    result[pcritic_id] = []
                    continue

                match = pattern_cells.search(line)
                if match and pcritic_id > 0:
                    result[pcritic_id].append(int(match.group(1)))  

        return result
        
    
#file = f"000000.txt"

""""
debug = Read_timing(file)
cells = debug.get_cells()
slack = debug.get_slack()
arival = debug.get_arrival_times()
start_point = debug.get_startpint()
end_point = debug.get_endpoint()
"""

"""""
def debug(sta_file):
    rt = Read_timing(sta_file)

    cells       = rt.get_cells()
    arrivals    = rt.get_arrival_times()
    

    for cid in sorted(cells.keys()):
        print(f"\n=== Caminho crítico {cid} ===")
        arr = arrivals.get(cid, "-")
        print(f"Arrival    : {arr}")
        print("Células:")
        for c in cells[cid]:
            print(
                f"  {c['cell_id']}  {c['type']}{c['size']}  "
                f"delay={c['ac_delay']}  time={c['time']}"
            )
        print("-" * 40)

for sta_file in files:
    full_path = os.path.join(deigns_path, sta_file)
    print("_" * 50)
    print(f"{sta_file}")
    print("_" * 50)
    debug(full_path)

"""""