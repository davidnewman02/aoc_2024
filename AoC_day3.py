import math
import re

in_txt = open("AoC_input/day3.txt", "r").read()

def get_total(in_txt):
    return sum(math.prod(map(int, match.groups())) for match in re.finditer("mul\((\d+),(\d+)\)", in_txt))

grand_total = sum(get_total(part) for part in in_txt.split("do") if not part.startswith("n't"))

print("Part 1: ", get_total(in_txt))
print("Part 2: ", grand_total)


