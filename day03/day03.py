#!/usr/bin/env python3

import sys
import numpy as np

# Input is a set of binary numbers:
#  00100
#  11110
#  10110
# etc.

with open(sys.argv[1], 'r') as df:
    lines = df.readlines()
    digits = np.array([ [int(x) for x in s.strip()]  for s in lines ])
    
    # Matrix transpose gets us a row that's the first digit of each input line
    # Summing across each row is the number of ones, and if the sum is more than
    # half of the number of lines, then there were more ones than zeros.
    trans = digits.transpose()
    sums = np.sum(trans, axis=1)

    # Do you know how often I have wanted a first-class boolean type for Python?
    gamma_bits = [ 1 if x > (len(lines)/2) else 0 for x in sums ]
    epsilon_bits = [ (2 + ~x) for x in gamma_bits ]
    gamma = int("".join([str(x) for x in gamma_bits]), 2)
    epsilon = int("".join([str(x) for x in epsilon_bits]), 2)
    print(f"gamma: {gamma}\nepsilon: {epsilon}\power consumption: {gamma * epsilon}")
