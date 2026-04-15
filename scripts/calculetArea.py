
def map_nand_area(sized_gates):
    maping = {
        "X1" : 0.798,
        "X2" : 1.330,
        "X4" : 2.394
    }

    return[maping[x] for x in sized_gates]

def c_area(cells_dimisions):
    return sum(cells_dimisions)


"""
values = ['X2', 'X2', 'X1', 'X1', 'X1', 'X4']
maping = map_nand_area(values)
print(maping)

cells_total = c_area(maping)
print(cells_total)
"""
