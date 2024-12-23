from collections import Counter, deque
from tqdm import tqdm


def parse_input(in_file):
    data = []
    with open(in_file, "r") as fh:
        for line in fh.read().split('\n'):
            data.append(int(line))
    return data


def secret_number(i):
    prn = 16777216
    i = (i*64 ^ i) % prn
    i = ((i // 32) ^ i) % prn
    i = ((i * 2048) ^ i) % prn
    return i

def part_1(data, iter):
    total = 0
    for i in tqdm(data):
        for _ in range(iter):
            i = secret_number(i)
        total += i
    return total

def part_2(data, iter):
    cnt = Counter()
    fifo = deque(maxlen=4)
    for i in tqdm(data):
        seen_seqs = set()
        for _ in range(iter):
            new = secret_number(i)
            diff = new % 10 - i % 10
            fifo.append(diff)
            tpl = tuple(fifo)
            if len(tpl) == 4 and tpl not in seen_seqs:
                seen_seqs.add(tpl)
                cnt[tpl] += new % 10
            i = new
    return max(cnt, key=cnt.get), max(cnt.values())


data = parse_input("AoC_input/day22.txt")
iter = 2000
#print("Part.1: ", part_1(data, iter))


#data = [1, 2, 3, 2024]
print("Part.2: ", part_2(data, iter))

