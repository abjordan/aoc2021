#!/usr/bin/env python3

import networkx as nx
import numpy as np
import sys

input_lines = [list(y) for y in [x.strip() for x in open(sys.argv[1], 'r').readlines()]]

maze_arr = np.array(input_lines, dtype=int)

# Need to turn the maze into a graph
maze = nx.DiGraph()
for idx, x in np.ndenumerate(maze_arr):
    me = "{0:03d}_{1:03d}".format(idx[0], idx[1])

    # Calculate costs to enter each of the neighbors. Note that we 
    # don't need to add edges up or to the left, as we would have 
    # already added them from previous passes through the array.
    #
    # NOTE: The above comment is WRONG, since the edge costs are
    # not symmetric! I'd be much better at this if I could read
    if idx[1] > 0:
        up = "{0:03d}_{1:03d}".format(idx[0], idx[1]-1)
        maze.add_edge(me, up, weight=maze_arr[idx[0], idx[1]-1])

    if idx[1] < (maze_arr.shape[1]-1):
        right = "{0:03d}_{1:03d}".format(idx[0], idx[1]+1)
        maze.add_edge(me, right, weight=maze_arr[idx[0], idx[1]+1])

    if idx[0] < (maze_arr.shape[0]-1):
        down = "{0:03d}_{1:03d}".format(idx[0]+1, idx[1])
        maze.add_edge(me, down, weight=maze_arr[idx[0]+1, idx[1]])

    if idx[0] > 0:
        left = "{0:03d}_{1:03d}".format(idx[0]-1, idx[1])
        maze.add_edge(me, left, weight=maze_arr[idx[0]-1, idx[1]])


start = "{0:03d}_{1:03d}".format(0, 0)
end = "{0:03d}_{1:03d}".format(*[x-1 for x in [*maze_arr.shape]])

# Cheating, since I'm so far behind. This is Dijkstra's, by default,
# and I know I can look the algorithm up if I need to.
shortest_path = nx.shortest_path(maze, source=start, target=end, weight='weight')

indices = [(int(x),int(y)) for x,y in [n.split("_") for n in shortest_path]]
cost = 0
for pos in indices[1:]:
    cost += maze_arr[ pos[0], pos[1] ]
print(cost)