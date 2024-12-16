import itertools

import numpy
import numpy as np
from AoC_helpers import parse_input_str_array, bounds_check

STEPS = ((-1, 0), (0, -1), (1, 0), (0, 1))


def get_cost(mask_arr):
    area = mask_arr.sum()
    perim = area * 4
    for pos in np.argwhere(mask_arr == 1):
        if pos[0] + 1 < mask_arr.shape[0]:
            perim -= mask_arr[pos[0] + 1, pos[1]] * 2
        if pos[1] + 1 < mask_arr.shape[1]:
            perim -= mask_arr[pos[0], pos[1] + 1] * 2
    return area * perim


def walkabout(pos, target_arr, out_arr, visited_positions):
    out_arr[pos] = 1
    for step_x, step_y in STEPS:
        new_pos = (pos[0] + step_x, pos[1] + step_y)
        if new_pos not in visited_positions \
                and bounds_check(new_pos, out_arr) \
                and target_arr[new_pos] == 1:
            visited_positions.add(new_pos)
            out_arr = walkabout(new_pos, target_arr, out_arr, visited_positions)
    return out_arr


def find_uniq(mask_arr):
    visited_positions = set()
    for pos in np.argwhere(mask_arr == 1):
        pos = tuple(pos)
        if pos in visited_positions:
            continue
        yield walkabout(pos, mask_arr, np.zeros(mask_arr.shape), visited_positions)

def outer_edges(mask_arr):
    """
    Number of outer edges is (4*count - inner_edges)
    """
    total = mask_arr.sum() * 4
    for pos in numpy.argwhere(mask_arr == 1):
        for dir in [(0,1), (1,0), (0, -1), (-1,0)]:
            check_pos = (pos[0] + dir[0], pos[1] + dir[1])
            if bounds_check(check_pos, mask_arr):
                total -= mask_arr[check_pos]
    return total


def part_1(in_arr):
    total = 0
    for chr in np.unique(in_arr):
        mask_arr = np.zeros(in_arr.shape)
        mask_arr[in_arr == chr] = 1
        for uniq_arr in find_uniq(mask_arr):
            total += get_cost(uniq_arr)
    return total


def raster(mask_arr):
    padded_matrix = np.pad(mask_arr, pad_width=1, mode='constant', constant_values=0)

    v_edges = (padded_matrix[1:, :] - padded_matrix[:-1, :])
    v_cnt = abs(v_edges[:, 1:] - v_edges[:, :-1]).sum() / 2

    h_edges = (padded_matrix[:, 1:] - padded_matrix[:, :-1])
    h_cnt = abs(h_edges[1:, :] - h_edges[:-1, :]).sum() / 2
    return (h_cnt + v_cnt)


def corners(mask_arr):
    total = 0
    for pos in numpy.argwhere(mask_arr == 1):
        for crn in [
            ((0,1), (1, 0)),
            ((1, 0), (0, -1)),
            ((0, -1), (-1, 0)),
            ((-1, 0), (0, 1)),
        ]:

            try:
                if mask_arr[(pos[0]+crn[0][0], pos[1]+crn[0][1])] and mask_arr[(pos[0]+crn[1][0], pos[1]+crn[1][1])]:
                    total += 1
            except:
                total += 1
    return total

def part_2(in_arr):
    total = 0
    for chr in np.unique(in_arr):
        mask_arr = np.zeros(in_arr.shape)
        mask_arr[in_arr == chr] = 1
        for uniq_arr in find_uniq(mask_arr):
            area = uniq_arr.sum()
            sides = raster(uniq_arr)
            total += area * sides

    return total


in_arr = parse_input_str_array("AoC_input/day12.txt")
print("Part.1: ", part_1(in_arr))
print("Part.2: ", part_2(in_arr))
