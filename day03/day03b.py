#!/usr/bin/env python3

import sys
import numpy as np
from numpy.testing._private.utils import break_cycles

# Input is a set of binary numbers:
#  00100
#  11110
#  10110
# etc.

def common_bit(arr, pos):
    vec = arr[:,pos]
    bit = 1 if sum(vec) >= (len(vec)/2) else 0
    return bit 

def check_digit(row, pos, val):
    return (row[pos] == val)

with open(sys.argv[1], 'r') as df:
    lines = df.readlines()
    digits = np.array([ [int(x) for x in s.strip()]  for s in lines ])
    
    orig_digits = np.array(digits)

    offset = 0
    while digits.shape[0] > 1:
        res = common_bit(digits, offset)
        new_digits = np.array([ check_digit(r, offset, res) for r in digits ])
        digits = digits[new_digits]
        offset += 1

    o2 = int(''.join([str(x) for x in digits[0]]), 2)
    print(f"O2 Gen: { o2 }")

    offset = 0
    digits = orig_digits
    while digits.shape[0] > 1:
        res = common_bit(digits, offset)
        new_digits = np.array( [ not check_digit(r, offset, res) for r in digits ])
        digits = digits[new_digits]
        offset += 1

    co2 = int(''.join([str(x) for x in digits[0]]), 2)
    print(f"CO2 Scrubber: { co2 }")

    print(f"Life support rating: { o2 * co2 }")
    