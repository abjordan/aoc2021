#!/usr/bin/env python3

import functools
import sys

if not len(sys.argv) is 3:
    print("USAGE: day01.py <input-file> <window-size>")
    sys.exit(1)

with open(sys.argv[1], "r") as infile:
    lines = infile.readlines()

numbers = [int(x) for x in lines]

window_size = int(sys.argv[2])

#print(numbers)

windowed = []
for x in range(window_size, len(numbers)+1):
    window = numbers[(x-window_size):x]
    windowed.append(sum(window))
#print(windowed)

delta = []
for x in range(1, len(windowed)):
    delta.append(1 if (windowed[x] - windowed[x-1] > 0) else 0)
print(sum(delta))