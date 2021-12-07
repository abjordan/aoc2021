#!/usr/bin/env python3

import functools
import sys

from alive_progress import alive_bar
from collections import Counter


iterations = int(sys.argv[2])

with open(sys.argv[1], 'r') as infile:
    start = [int(x) for x in infile.readline().strip().split(",")]

# Pretty sure there's a closed form version of this, as there's no 
# interaction between each entry in the array. This will probably
# be important before very long

# Since the fish don't interact, we can split fish out into 
# cohorts based on their start date, as soon as they have
# their first baby. These cohorts will be synchronized, so
# they should be memoizable, based on how many fish were in 
# the initial population and the remaining days. In fact,
# they can spit out a full new cohort!

# list of pairs: (internal_clock, count)
cohorts = []
c = Counter(start)
for clock_val in sorted(c.keys()):
    cohorts.append((clock_val, c[clock_val]))

# Each cohort will reproduce once every seven days and create a new cohort 
# that reproduces at that time.
with alive_bar(iterations) as bar:
    for i in range(1, iterations+1):
        new_cohort_size = 0
        for idx, cohort in enumerate(cohorts):
            if cohort[0] == 0:
                new_cohort_size += cohort[1]   # each fishy has one baby fishy
                cohorts[idx] = (6, cohort[1])
            else:
                cohorts[idx] = (cohort[0] - 1, cohort[1])
        if new_cohort_size != 0:
            cohorts.append((8, new_cohort_size))
        bar()
    
fish_count = functools.reduce(lambda a, b: a+b, [c[1] for c in cohorts])
print(f"After {iterations} days, there are {fish_count} fish")

# Brute force version:
# population = start
# new_fish = []
# print('Initial state  : {0}'.format(population))
# with alive_bar(iterations+1) as bar:
#     bar()
#     for i in range(1, iterations+1):
#         for idx, fish in enumerate(population):
#             if fish == 0:
#                 new_fish.append(8)
#                 population[idx] = 6
#             else:
#                 population[idx] = fish - 1
#         population.extend(new_fish)
#         print(f"{population}")
#         new_fish = []
#         bar()
# 
# print(f"After {iterations} days, there are {len(population)} fish")