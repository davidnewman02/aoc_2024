import re
from collections import Counter
from functools import lru_cache, cache


def parse_input(in_file):
    with open(in_file, "r") as fh:
        in_lines = fh.read().split('\n')
    words = tuple({i.strip() for i in in_lines[0].strip().split(',')})
    tests = [i.strip() for i in in_lines[1:] if i]
    return tests, words

@lru_cache
def is_possible(test, words):
    if test == "":
        return 1
    return next((1 for word in words if test.startswith(word) and is_possible(test[len(word) :], words)), 0)

@lru_cache
def cnts(test, words):
    if test == "":
        return 1
    total = 0
    for word in words:
        if test.startswith(word):
            total += cnts(test[len(word) :], words)
    return total

def part_1(tests, words):
    return sum(is_possible(test, words) for test in tests)

def part_2(tests, words):
    return sum(cnts(test, words) for test in tests)

in_file = "AoC_input/day19.txt"
tests, words = parse_input(in_file)
print("Part.1: ", part_1(tests, words))
print("Part.2: ", part_2(tests, words))

