
import numpy as np
from collections import Counter
import itertools


def part1(arr, chars):
    out_arr = np.zeros(arr.shape)
    for chr in chars:
        pos = np.argwhere(arr == chr)
        if len(pos) < 1:
            continue
        for node1, node2 in itertools.combinations(pos, 2):
            x1, y1 = (2 * node1[0] - node2[0]), (2 * node1[1] - node2[1])
            try:
                if x1 >= 0 and y1 >= 0 and x1 <= out_arr.shape[0] and y1 <= out_arr.shape[1]:
                    out_arr[x1, y1] = 1
            except:
                pass
            x1, y1 = (2 * node2[0] - node1[0]), (2 * node2[1] - node1[1])
            try:
                if x1 >= 0 and y1 >= 0 and x1 <= out_arr.shape[0] and y1 <= out_arr.shape[1]:
                    out_arr[x1, y1] = 1
            except:
                pass
    return out_arr.sum()


def part2(arr, chars):
    out_arr = np.zeros(arr.shape)
    for chr in chars:
        print(chr)
        pos = np.argwhere(arr == chr)
        if len(pos) < 1:
            continue
        #out_arr[arr == chr] = 1
        for node1, node2 in itertools.combinations(pos, 2):
            x_diff = node1[0] - node2[0]
            y_diff = node1[1] - node2[1]

            # backward
            new_x, new_y = node1[0], node1[1]
            while 0 <= new_x < out_arr.shape[0] and 0 <= new_y < out_arr.shape[1]:
                out_arr[new_x, new_y] = 1
                new_x, new_y = new_x + x_diff, new_y + y_diff

            # forward
            new_x, new_y = node2[0], node2[1]
            while 0 <= new_x < out_arr.shape[0] and 0 <= new_y < out_arr.shape[1]:
                out_arr[new_x, new_y] = 1
                new_x, new_y = new_x - x_diff, new_y - y_diff

    return out_arr.sum()

in_file = "AoC_input/day8.txt"

with open(in_file, "r") as fh:
    in_str = fh.read()
    in_arr = np.array([list(line.strip()) for line in in_str.split('\n')])
    all_chars = set(in_str)
    all_chars.remove("\n")
    all_chars.remove(".")


#print("Part.1: ", part1(in_arr, all_chars))
print("Part.2: ", part2(in_arr, all_chars))

