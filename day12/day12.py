#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
import sys

def spelunk(world, current, path_to_here, visited, doubled):
    path_to_here.append(current)
    if not current.isupper():
        visited.add(current)

    if current == 'end':
        return [path_to_here]
    
    paths_from_here = []
    for next in list(world[current]):    # neighbors
        if next.isupper():
            paths_from_here.extend(spelunk(world, next, path_to_here.copy(), visited.copy(), doubled))
        elif next not in visited:
            paths_from_here.extend(spelunk(world, next, path_to_here.copy(), visited.copy(), doubled))
        elif doubled is False and next != 'start':
            paths_from_here.extend(spelunk(world, next, path_to_here.copy(), visited.copy(), True))
    
    return paths_from_here

if __name__ == '__main__':

    allow_double = len(sys.argv) < 3

    world = nx.Graph()
    with open(sys.argv[1], 'r') as infile:
        for line in infile.readlines():
            toks = line.strip().split('-')
            src = toks[0]
            dst = toks[1]
            world.add_nodes_from(toks)
            world.add_edge(src, dst)

    # Find all paths that start at `start` and end at `end`
    # but only visit any particular big cave (uppercase) once
    paths = spelunk(world, 'start', [], set(['start']), allow_double)
    #for path in paths:
    #    print('\t' + ','.join(path))

    print(f'Found {len(paths)} paths')