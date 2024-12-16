import re

import numpy as np


def parse_file(in_file):
    data = []
    with open(in_file, "r") as fh:
        data.extend([int(g) for g in re.findall(r"-?\d+", line)] for line in fh.read().split('\n') if line)

    return data


def part_1(data, grid_size, num_iter):
    out_arr = np.zeros(grid_size, dtype=int)
    for pos in data:
        x_pos = (pos[1] + pos[3] * num_iter) % grid_size[0]
        y_pos = (pos[0] + pos[2] * num_iter) % grid_size[1]
        out_arr[x_pos, y_pos] += 1
    quad1 = out_arr[:grid_size[0] // 2, :grid_size[1] // 2]
    quad2 = out_arr[1+(grid_size[0] // 2):, :grid_size[1] // 2]
    quad3 = out_arr[:grid_size[0] // 2, 1+(grid_size[1] // 2):]
    quad4 = out_arr[1+(grid_size[0] // 2):, 1+(grid_size[1] // 2):]
    return quad1.sum() * quad2.sum() * quad3.sum() * quad4.sum()


def print_arr(in_arr):
    for row in in_arr:
        print("".join(["." if i == 0 else "#" for i in row]))

def find_line(in_arr, thresh):
    for row in in_arr:
        longest_grp = np.diff(np.where(row == 0)).max() - 1
        if longest_grp > thresh:
            return True
    return False

def part_2(data, grid_size):
    for num_iter in range(10000):
        if not num_iter % 1000: print(f"Iter: {num_iter}")
        out_arr = np.zeros(grid_size, dtype=int)
        for pos in data:
            x_pos = (pos[1] + pos[3] * num_iter) % grid_size[0]
            y_pos = (pos[0] + pos[2] * num_iter) % grid_size[1]
            out_arr[x_pos, y_pos] += 1
        """
        A tree must have a contiguous horizontal line of >=16 non-zero elements
        """
        thresh = 16
        # if find_line(out_arr, thresh):
        if np.max(np.diff(np.where(out_arr == 0), axis=1)) > thresh:
            print(f"""============== ITER {num_iter} ================""")
            print_arr(out_arr)
            return num_iter

in_file = "AoC_input/day14.txt"
data = parse_file(in_file)
#grid_size = (7, 11)
grid_size = (103, 101)
num_iter = 100

print("Part.1: ", part_1(data, grid_size, num_iter))
print("Part.2: ", part_2(data, grid_size))


