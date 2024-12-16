import itertools
import operator

from tqdm import tqdm


def parse_file(fn):
    targets = []
    arrs = []
    with open(fn, "r") as fh:
        for line in fh:
            targets.append(int(line.split(":")[0]))
            arrs.append([int(i) for i in line.strip().split(':')[1].split()])
    return arrs, targets


def part1(in_arrs, targets):
    total = 0
    ops = (operator.add, operator.mul)
    for in_arr, target in zip(in_arrs, targets):
        for op_list in itertools.product(ops, repeat=len(in_arr) - 1):
            result = in_arr[0]
            for i, op in enumerate(op_list):
                result = op(result, in_arr[i + 1])
            if result == target:
                total += target
                break
    return total


def part2(in_arrs, targets):
    total = 0
    ops = (operator.add, operator.mul, lambda a, b: int(str(a) + str(b)))
    for in_arr, target in tqdm(zip(in_arrs, targets), total=len(targets)):
        for op_list in itertools.product(ops, repeat=len(in_arr) - 1):
            result = in_arr[0]
            for i, op in enumerate(op_list):
                result = op(result, in_arr[i + 1])
            if result == target:
                total += target
                break
    return total


in_file = "AoC_input/day7.txt"
arrs, targets = parse_file(in_file)

print("Part.1", part1(arrs, targets))
print("Part.2", part2(arrs, targets))
