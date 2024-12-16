
import numpy as np

def parse_input_int_array(in_file):
    with open(in_file, "r") as fh:
        return np.array([[int(i) for i in line.strip()] for line in fh.read().split('\n')])

def parse_input_str_array(in_file):
    with open(in_file, "r") as fh:
        return np.array([[i for i in line.strip()] for line in fh.read().split('\n')])

def bounds_check(pos, arr):
    return (0 <= pos[0] < arr.shape[0]) and (0 <= pos[1] < arr.shape[1])

