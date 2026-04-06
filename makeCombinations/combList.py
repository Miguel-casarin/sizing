def total_to_size(gates_number):
    total_combination = 3 ** gates_number
    combinatios = []
    
    for i in range(total_combination):
        comb = []
        num = i

        for _ in range(gates_number):
            comb.append(num % 3)
            num //= 3

        combinatios.append(list(reversed(comb)))

    return combinatios

# Iterpleta uma combinação e retorna os valores de size
def decode_size(comb):
    mapping = {
        0 : "X1",
        1 : "X2",
        2 : "X4"
    }

    return [mapping[x] for x in comb]

c = total_to_size(6)

caso = 0
for value in c:
    dec = decode_size(value)
    print(f"\n CASO : {caso} -> {dec}\n")
    caso += 1