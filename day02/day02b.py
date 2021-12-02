#!/usr/bin/env python

import sys

horizontal = 0
depth = 0
aim = 0

with open(sys.argv[1], 'r') as df:
    for line in df.readlines():
        tok = line.strip().split(" ")
        if tok[0] == "forward":
            horizontal += int(tok[1])
            depth += aim * int(tok[1])
        elif tok[0] == "down":
            aim += int(tok[1])
        elif tok[0] == "up":
            aim -= int(tok[1])
        else:
            print(f"Unknown command: {line.strip()}")

print(f"Horizontal: {horizontal}    Depth: {depth}")
print(f"Answer: {horizontal * depth}")