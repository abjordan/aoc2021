#!/usr/bin/env python3

import sys

from alive_progress import alive_bar

with open(sys.argv[1], 'r') as infile:
    start = [int(x) for x in infile.readline().strip().split(",")]

# Pretty sure there's a closed form version of this, as there's no 
# interaction between each entry in the array.

# For each fish, it will reproduce every six days once it hits 
# zero for the first time. So the offset for each fish is just
# a shift to the right on the starting point for the exercise.

iterations = int(sys.argv[2])

population = start
new_fish = []
print('Initial state  : {0}'.format(population))
with alive_bar(iterations) as bar:
    for i in range(1, iterations+1):
        for idx, fish in enumerate(population):
            if fish == 0:
                new_fish.append(8)
                population[idx] = 6
            else:
                population[idx] = fish - 1
        population.extend(new_fish)
        new_fish = []
        bar()        

print(f"After {iterations} days, there are {len(population)} fish")