import numpy as np

from AoC_helpers import parse_input_str_array

def prep_data(in_file):
    XMAS = "XMAS"
    arr = parse_input_str_array(in_file)
    masks = np.zeros((len(XMAS), *arr.shape))
    for i, letter in enumerate(XMAS):
        masks[i, :, :] = (arr == letter)
    return masks


def count_linear(arrs):
    stack = np.stack([arrs[0, :-3, :], arrs[1, 1:-2, :], arrs[2, 2:-1, :], arrs[3, 3:, :]])
    return np.logical_and.reduce(stack).sum()


def count_diag(arrs):
    stack = np.stack([arrs[0, :-3, :-3], arrs[1, 1:-2, 1:-2], arrs[2, 2:-1, 2:-1], arrs[3, 3:, 3:]])
    return np.logical_and.reduce(stack).sum()


def part_1(in_arr):
    total = 0

    total += count_linear(in_arr)  # Horizontal - fwd
    total += count_linear(in_arr[:, ::-1, :])  # Horizontal - rev
    total += count_linear(np.swapaxes(in_arr, 1, 2))  # Vertical   - fwd
    total += count_linear(np.swapaxes(in_arr, 1, 2)[:, ::-1, :])  # Vertical   - rev

    total += count_diag(in_arr)  # diag-down-right
    total += count_diag(in_arr[:, ::-1, :])  # diag-down-left
    total += count_diag(in_arr[:, :, ::-1])  # diag-up-fwd
    total += count_diag(in_arr[:, ::-1, ::-1])  # diag-up-rev
    return total


def part_2(in_arr):
    total = 0
    for a_x, a_y in np.argwhere(in_arr[2, :-1, :-1]):
        if a_x == 0 or a_y == 0:
            # Skip the leading edges, we skip the trailing edges with `:-1`
            continue
        for idxs in [(1, 1, 3, 3), (1, 3, 1, 3), (3, 1, 3, 1), (3, 3, 1, 1)]:
            ul = in_arr[idxs[0], a_x - 1, a_y + 1]
            ur = in_arr[idxs[1], a_x + 1, a_y + 1]
            ll = in_arr[idxs[2], a_x - 1, a_y - 1]
            lr = in_arr[idxs[3], a_x + 1, a_y - 1]
            x_mas = ll + ul + lr + ur
            if x_mas == 4:
                total += 1
    return total


arrs = prep_data("AoC_input/day4.txt")
print("Part.1: ", part_1(arrs))
print("Part.2: ", part_2(arrs))
