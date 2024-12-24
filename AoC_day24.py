from operator import and_, or_, xor

op_map = {
    "AND": and_,
    "OR": or_,
    "XOR": xor,
}

op_print = {
    and_: "&",
    or_: "|",
    xor: "^",
}

def parse_input(in_file):
    states = {}
    codes = {}
    with open(in_file, "r") as fh:
        for line in fh.read().split('\n'):
            if ":" in line:
                states[line[:3]] = int(line.strip()[-1])
            elif "-" in line:
                fields = line.strip().split(" ")
                codes[fields[4]] = (fields[0], op_map[fields[1]], fields[2])
    return states, codes


def part_1(states, codes):
    total = 0
    for code in codes:
        def get_value(k):
            k1, op, k2 = codes[k]
            if k1 not in states:
                states[k1] = get_value(k1)
            if k2 not in states:
                states[k2] = get_value(k2)
            #print(k, "=", k1, op_print[op], k2)
            return op(states[k1], states[k2])

        states[code] = get_value(code)
        if code.startswith("z"):
            total += states[code] * 2 ** int(code[1:])
    return total


states, codes = parse_input("AoC_input/day24.txt")
initial_answer = part_1(states, codes)
print("Part.1: ", initial_answer)

print("""
### Part.2
""")

states, codes = parse_input("AoC_input/day24.txt")
swaps = [
    ("z05", "bpf"),
    ("z11", "hcc"),
    ("z35", "fdw"),
    ("hqc", "qcw"),
]
for swp1, swp2 in swaps:
    intermed = codes[swp1]
    codes[swp1] = codes[swp2]
    codes[swp2] = intermed

initial_answer = part_1(states, codes)
#
xin = sum(v * 2 ** int(st[1:]) for st, v in states.items() if st.startswith("x"))
yin = sum(v * 2 ** int(st[1:]) for st, v in states.items() if st.startswith("y"))
target = xin + yin

xbin = bin(xin)
ybin = bin(yin)
initbin = bin(initial_answer)
tarbin = bin(target)

print("xin", bin(xin).replace("b", "b0"), xin)
print("yin", bin(yin).replace("b", "b0"), yin)
print("Cur", bin(initial_answer), initial_answer)
print("Tar", bin(target), target)

## Addition is generically Z_n = (X_n ^ Y_n) ^ (acc-bit)

# Find any z-outputs that are not XORs
for add, code in sorted(codes.items()):
    # We ignore z45 as it's the max
    if add.startswith("z") and code[1] != xor and add != f"z{len(tarbin)-3}":
        print(add, code)

## These should swap with some other ops
## We can find them by hand looking for X_n ^ Y_n in the input table
# z05 <-> bpf
# z11 <-> hcc
# z35 <-> fdw

# After making these swaps we still have an accumulation error on one bit; find it
for i in range(len(tarbin)):
    if tarbin[-i] != initbin[-i]:
        print("Acc error at: ", i-1)
        break
## z24 currently equals (x24 & y24) ^ (acc)
## Need to switch in the x24 ^ y24 operator
# qcw <-> hqc



sorted_swaps = sorted(s for swp in swaps for s in swp)
print("Part.2: ", ",".join(sorted_swaps))

