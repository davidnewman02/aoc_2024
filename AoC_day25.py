from collections import Counter
import numpy as np
from tqdm import tqdm


def parse_input(in_file):
    block_len = 8
    locks = []
    keys = []

    with open(in_file, "r") as fh:
        lines = fh.read().strip().split('\n')
        for block in range(0, len(lines), block_len):
            if lines[block][0] == "#":
                # Lock
                lk = np.array([list(row) for row in lines[block:block+block_len-1]])
                locks.append((lk == "#").sum(axis=0)-1)
            elif lines[block][0] == ".":
                # key
                k = np.array([list(row) for row in lines[block:block + block_len - 1]])
                keys.append(6-(k == ".").sum(axis=0))
            else:
                raise ValueError

    return locks, keys


def part_1(keys, locks):
    total = 0
    for k in keys:
        for lock in locks:
            if max(k + lock) < 6:
                total += 1
    return total


keys, locks = parse_input("AoC_input/day25.txt")
"""
Unnecessarily heavyweight numpy solution...
"""
print("Part.1: ", part_1(keys, locks))

