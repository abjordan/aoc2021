#!/usr/bin/env python

import sys

horizontal = 0
depth = 0

with open(sys.argv[1], 'r') as df:
    for line in df.readlines():
        tok = line.strip().split(" ")
        if tok[0] == "forward":
            horizontal += int(tok[1])
        elif tok[0] == "down":
            depth += int(tok[1])
        elif tok[0] == "up":
            depth -= int(tok[1])
            if depth < 0: depth = 0
        else:
            print(f"Unknown command: {line.strip()}")

print(f"Horizontal: {horizontal}    Depth: {depth}")
print(f"Answer: {horizontal * depth}")