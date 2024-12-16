from collections import defaultdict


def parse_file(in_file):
    updates = defaultdict(set)
    orders = []
    with open(in_file, "r") as fh:
        for line in fh:
            line = line.strip()
            if "|" in line:
                updates[int(line.split("|")[0])].add(int(line.split("|")[1]))
            elif "," in line:
                orders.append([int(i) for i in line.split(',')])
    return updates, orders


def is_ordered(order, updates):
    for trim, el in enumerate(order):
        if any(el in updates[i] for i in order[trim + 1:]):
            return False
    return True


def get_page_sum(updates, orders):
    return sum(o[len(o) // 2] for o in orders if is_ordered(o, updates))


def get_reordered_sum(ups, ords):
    return sum(sorted(o, key=lambda x: len(ups[x] & set(o)))[len(o) // 2] for o in ords if not is_ordered(o, ups))

updates, orders = parse_file("AoC_input/day5.txt")
print("Part.1: ", get_page_sum(updates, orders))
print("Part.2: ", get_reordered_sum(updates, orders))
