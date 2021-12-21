#!/usr/bin/env python3

from collections import Counter
import sys

rounds = int(sys.argv[2])

with open(sys.argv[1], 'r') as infile:
    starter = infile.readline().strip()
    blank = infile.readline()
    instructions = [x.strip() for x in infile.readlines()]

pairs = Counter()
elements = Counter()

elements.update(starter)
for i in range(0, len(starter)-1):
    p = starter[i:i+2]
    pairs[p] += 1

print(pairs)
round = 0
for round in range(1, rounds+1):
    print(f'------ Round {round}/{rounds} ------')
    found = Counter()
    new_pairs = Counter()
    for ins in instructions:
        round += 1
        find, arrow, insert = ins.split(' ')
        if pairs[find] > 0:
            found[find] += pairs[find]
            new_p0 = find[0] + insert
            new_p1 = insert + find[1]
            new_pairs[new_p0] += pairs[find]
            new_pairs[new_p1] += pairs[find]
            elements[insert] += pairs[find]
    pairs -= found
    pairs += new_pairs
    #print(pairs)
    #print(f'Length: {sum(elements.values())}')
 
pairs = +pairs

print(f'Most  common element: {elements.most_common()[0]}')
print(f'Least common element: {elements.most_common()[-1]}')
delta = elements.most_common()[0][1] - elements.most_common()[-1][1]
print(f'Difference: {delta}')