import numpy as np


data = []
with open("AoC_input/day2.txt", "r") as fh:
    for line in fh:
        data.append(np.array([int(i) for i in line.strip().split()]))

def is_safe(in_arr):
    diffs = in_arr[:-1] - in_arr[1:]
    if (abs(diffs) >= 1).all() and (abs(diffs) <= 3).all() and ((diffs > 0).all() or (diffs < 0).all()):
        return True
    return False

## Pt.1

safe_pt1 = 0
for line in data:
    if is_safe(line):
        safe_pt1 += 1
        continue
print("Pt.1: ", safe_pt1)

## Pt.2

safe_pt2 = 0
for line in data:
    if is_safe(line):
        safe_pt2 += 1
        continue
    for i in range(len(line)):
        pop_line = list(line)
        pop_line.pop(i)
        if is_safe(np.array(pop_line)):
            safe_pt2 += 1
            break
print("Pt.2: ", safe_pt2)




