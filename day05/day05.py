#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

import re
import sys

from collections import defaultdict
from itertools import zip_longest
from PIL import Image

parser = re.compile(r'(?P<x1>\d+),(?P<y1>\d+) -> (?P<x2>\d+),(?P<y2>\d+)')

board = np.zeros((1000,1000))

with open(sys.argv[1], 'r') as inf:
    for line in inf.readlines():
        x1, y1, x2, y2 = [ int(x) for x in parser.match(line.strip()).groups() ]        
        points = None

        x_step = 1 if x2 > x1 else -1
        y_step = 1 if y2 > y1 else -1

        # This could be refactored to make it DRY-er, but I think it's easier
        # to understand what's going on if the steps are a little more explicit
        if (x1 == x2):
            points = zip_longest([x1], range(y1, y2+y_step, y_step), fillvalue=x1)
        elif (y1 == y2):
            points = zip_longest(range(x1, x2+x_step, x_step), [y1], fillvalue=y1)
        else:
            points = zip(range(x1, x2+x_step, x_step), range(y1, y2+y_step, y_step))
    
        for point in points:
            board[point] = board[point] + 1

print(f"Squares with overlapping points: {np.count_nonzero(board > 1)}")

# Let's try drawing a picture?
max_val = board.max()
old_board = board.copy()
print(f"Maximum overlap: {max_val}")
with np.nditer(board, op_flags=['readwrite']) as it:
    for c in it:
        c[...] = (c / max_val)

# See https://matplotlib.org/stable/tutorials/colors/colormaps.html
# for values for the colormap. H/T: https://stackoverflow.com/a/47866630
cm = plt.get_cmap('inferno')
color_img = cm(board)
img = Image.fromarray((color_img[:, :, :3] * 255).astype(np.uint8))
img.save("test.png")
img.show()

print("Computing histogram of values...")
sys.stdout.flush()
counts = defaultdict(int)
for it in np.nditer(old_board):
    val = int(it)
    counts[val] += 1

print("-------------------")
for k,v in counts.items():
    print(f"{int(max_val * (k / 255))}: {v} ")
print("-------------------")