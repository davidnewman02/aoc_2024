import itertools

import numpy as np
from tqdm import tqdm

from AoC_helpers import parse_input_str_array, STEPS



def part_1(barriers, start):
    pos = start
    steps = np.zeros(barriers.shape)
    steps[start] = 1

    up = (-1, 0)
    ri = (0, 1)
    dn = (1, 0)
    lf = (0, -1)

    directions = itertools.cycle([up, ri, dn, lf])
    direction = next(directions)
    while True:
        try:
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if barriers[new_pos]:
                direction = next(directions)
            else:
                steps[new_pos] = 1
                pos = new_pos
                if pos == start and direction == up:
                    print("Circle!!")
                    break
        except IndexError:
            break
    return steps

def is_loop(barriers, start):
    up = (-1, 0)
    ri = (0, 1)
    dn = (1, 0)
    lf = (0, -1)
    dirs = [up, ri, dn, lf]
    directions = itertools.cycle(dirs)
    direction = next(directions)

    steps = {i: np.zeros(barriers.shape) for i in dirs}
    pos = start

    while True:
        try:
            next_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if next_pos[0] == -1 or next_pos[1] == -1:
                return 0
            if barriers[pos[0] + direction[0], pos[1] + direction[1]]:
                direction = next(directions)
            else:
                if steps[direction][next_pos]:
                    return 1
                steps[direction][next_pos] = 1
                pos = next_pos
        except IndexError:
            return 0

input_arr = parse_input_str_array("AoC_input/day6.txt")
barriers = input_arr == "#"
start = tuple(int(i) for i in np.where(input_arr == "^"))

steps = part_1(barriers, start)
print("Part.1", steps.sum())

total = 0
for new_bar_pos in tqdm(np.argwhere(steps == 1), total=steps.sum()):
    new_bars = barriers.copy()
    new_bars[new_bar_pos[0], new_bar_pos[1]] = True
    total += is_loop(new_bars, start)

print("Part.2", total)


