import numpy as np
from AoC_helpers import parse_input_str_array
from tqdm import tqdm


def parse_input(in_file):
    arr = parse_input_str_array(in_file)
    route = np.zeros(arr.shape)
    route[arr == "S"] = 1
    walls = np.zeros(arr.shape)
    walls[arr == "."] = 1
    walls[arr == "E"] = 1
    ## Trace route
    pos = tuple(np.argwhere(arr == "S")[0])
    for i in range(int(walls.sum())):
        for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (pos[0] + dir[0], pos[1] + dir[1])
            if walls[new_pos] == 1 and route[new_pos] == 0:
                route[new_pos] = i + 2
                pos = new_pos
                break
    return route


def part_1(route, jump_size, cheat_thresh):
    total = 0
    for pos in tqdm(np.argwhere(route > 0)):
        # find all points that we could jump to to make a sufficient saving
        # NB it would be more efficient to check all points within man-dist of
        for cheat in np.argwhere(route > (route[tuple(pos)] + cheat_thresh)):
            man_dist = (abs(pos[0] - cheat[0]) + abs(pos[1] - cheat[1]))
            saving = route[tuple(cheat)] - route[tuple(pos)] - man_dist + 1
            if jump_size >= man_dist and saving > cheat_thresh:
                total += 1
    return total


arr = parse_input("AoC_input/day20.txt")
print("Part.1: ", part_1(arr, 2, 100))
print("Part.2: ", part_1(arr, 20, 100))
