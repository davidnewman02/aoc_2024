from functools import lru_cache
from collections import Counter, defaultdict


def parse_input(in_file):
    with open(in_file, "r") as fh:
        return [int(i) for i in fh.read().strip().split()]


def part_2(in_arr, num_blinks):
    cnt = Counter(in_arr)
    for _ in range(num_blinks):
        cnt = blink_cnt(cnt)
    return sum(cnt.values())


@lru_cache(maxsize=200_000)
def cache_str(k):
    if k == 0:
        return 1, None
    s = str(k)
    if not len(s) % 2:
        return int(s[:len(s) // 2]), int(s[len(s) // 2:])
    else:
        return k * 2024, None


def blink_cnt(in_cnt):
    out_cnt = defaultdict(int)
    for k, v in in_cnt.items():
        k1, k2 = cache_str(k)
        out_cnt[k1] += v
        if k2 is not None:
            out_cnt[k2] += v
    return out_cnt


in_arr = parse_input("AoC_input/day11.txt")
print("Part.1: ", part_2(in_arr, 25))
print("Part.2: ", part_2(in_arr, 75))
