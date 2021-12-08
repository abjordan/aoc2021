#!/usr/bin/env python3

import sys
import numpy as np


with open(sys.argv[1], 'r') as infile:
    initial = np.array([int(x) for x in infile.readline().strip().split(',')])

# Cost is abs( p[x] - target )
# Need to find armin(sum( p - target ), target)

min_cost_a = float('inf')
min_idx_a = -1
min_cost_b = float('inf')
min_idx_b = -1

def cost_func_b(x, i):
    n = abs(x - i)
    return n*(n+1) / 2   # 7th grade algebra strikes again!

for i in range(min(initial), max(initial)):
    cost_a = sum(abs(initial - i))
    #print(f"{i}: {cost}")
    if cost_a < min_cost_a:
        min_cost_a = cost_a
        min_idx_a = i

    # If you're surprised that this is performant enough to 
    # solve the challenge input, well... so am I, frankly.
    cost_b = sum( np.array([cost_func_b(x, i) for x in initial]))
    if cost_b < min_cost_b:
        min_cost_b = cost_b
        min_idx_b = i

print(f"Part A - Minimum cost: {min_cost_a} at offset {min_idx_a}")
print(f"Part B - Minimum cost: {int(min_cost_b)} at offset {min_idx_b}")