from collections import Counter

import numpy as np


def part_1(in_data):
    unpack = unpacked_str(in_data)
    repacked = repack(unpack)
    return calc_checksum(repacked)


def unpacked_str(in_data):
    cnt = 0
    free = False
    out_arr = []
    for i in in_data:
        if free:
            out_arr.extend([None for _ in range(i)])
        else:
            out_arr.extend([cnt for _ in range(i)])
            cnt += 1
        free = not free
    return out_arr


def repack(packed_data):
    end_idx = 1
    out_arr = []
    for i in packed_data:
        if len(out_arr) == target_length:
            break
        if i is not None:
            out_arr.append(i)
        else:
            while packed_data[-end_idx] is None:
                end_idx += 1

            out_arr.append(packed_data[-end_idx])
            end_idx += 1
    return out_arr


def repack2(packed_data):
    out_vec = np.zeros(len(packed_data))
    cnts = np.zeros(max(i for i in packed_data if i is not None) + 1)
    for i in packed_data:
        if i is not None:
            cnts[i] += 1

    free_blocks = []
    blank_cnt = 0
    for i in range(len(packed_data)):
        if packed_data[i] is None:
            blank_cnt += 1
        elif blank_cnt:
            free_blocks.append((i - blank_cnt, blank_cnt))
            blank_cnt = 0

    packed_arr = np.array(packed_data)
    packed_arr[packed_arr == None] = 0
    excluded_bases = set()
    for idx in range(len(cnts) - 1, 0, -1):
        bsize = cnts[idx]
        max_pos = np.argmax(packed_arr >= idx)
        for free_i in range(len(free_blocks)):
            if free_blocks[free_i][0] >= max_pos:
                break
            if bsize <= free_blocks[free_i][1]:
                excluded_bases.add(idx)
                out_vec[free_blocks[free_i][0]:int(free_blocks[free_i][0] + bsize)] = idx
                free_blocks[free_i] = (
                int(free_blocks[free_i][0] + bsize), int(free_blocks[free_i][1] - bsize))
                break

    for i in range(len(out_vec)):
        if packed_data[i] is not None and packed_data[i] not in excluded_bases:
            out_vec[i] = packed_data[i]

    return out_vec


def calc_checksum(packed):
    return sum(i * v for i, v in zip(packed, range(len(packed))))


def part_2(in_data):
    unpack = unpacked_str(in_data)
    repacked = repack2(unpack)
    return calc_checksum(repacked)


with open("AoC_input/day9.txt", "r") as fh:
    in_data = [int(i) for i in fh.read().strip()]

#print("Part.1: ", part_1(in_data))
print("Part.2: ", part_2(in_data))
