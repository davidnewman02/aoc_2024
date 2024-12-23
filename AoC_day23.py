from collections import defaultdict, Counter

from tqdm import tqdm


def parse_input(in_file):
    data = defaultdict(set)
    with open(in_file, "r") as fh:
        cpus = fh.read().split('\n')
        for line in cpus:
            data[line[:2]].add(line[3:])
            data[line[3:]].add(line[:2])
    return data


def part_1(data):
    seen = set()
    for k in sorted(data):
        if not k.startswith("t"):
            continue
        for k2 in data[k]:
            for k3 in data[k2].intersection(data[k]):
                seen.add(tuple(sorted([k, k2, k3])))
    return len(seen)


def part_2(data):
    best_set = ()
    for k in sorted(data):
        cnt = Counter()
        for k2 in data[k]:
            cnt.update(data[k2])
        cnt.pop(k)
        key_cnt = Counter(cnt.values())

        if key_cnt[11] == 12:
            out = [k] + [i for i, v in cnt.items() if v == 11]
            return ",".join(sorted(out))

data = parse_input("AoC_input/day23.txt")
print("Part.1: ", part_1(data))
print("Part.2: ", part_2(data))
