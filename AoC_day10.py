import numpy as np

from AoC_helpers import parse_input_int_array, bounds_check

STEPS = ((-1, 0), (0, -1), (1, 0), (0, 1))

def part_1(in_arr):
    heads = [tuple(i) for i in np.argwhere(in_arr == 0)]
    return sum(len(step(in_arr, 0, pos, set())) for pos in heads)


def step(in_arr, i, pos, ends):
    if i == MAX_HEIGHT:
        return ends.add(pos)
    for step_x, step_y in STEPS:
        new_pos = (pos[0] + step_x, pos[1] + step_y)
        if bounds_check(new_pos, in_arr) and in_arr[new_pos] == i + 1:
            step(in_arr, i + 1, new_pos, ends)
    return ends


def part_2(in_arr):
    return sum(rate_step(in_arr, 0, pos, 0) for pos in np.argwhere(in_arr == 0))


def rate_step(in_arr, i, pos, total):
    if i == MAX_HEIGHT:
        return total + 1
    for step_x, step_y in STEPS:
        new_pos = (pos[0] + step_x, pos[1] + step_y)
        if bounds_check(new_pos, in_arr) and in_arr[new_pos] == i + 1:
            total = rate_step(in_arr, i + 1, new_pos, total)
    return total


in_arr = parse_input_int_array("AoC_input/day10.txt")
MAX_HEIGHT = 9
print("Part.1: ", part_1(in_arr))
print("Part.2: ", part_2(in_arr))
