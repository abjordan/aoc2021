#!/usr/bin/env python3

import numpy as np
import sys

from PIL import Image, ImageDraw

MAX_FOLDS = 10000000

def do_fold(paper, fold):
    axis = fold[0]
    value = fold[1]

    print(f"FOLD ABOUT {axis}={value}")

    if axis == 'y':
        # Fold UP: indices above value get reflected about the point
        for row in range(value+1, paper.shape[0]):
            target_row = value - (row - value)
            #print(f'{row} --> {target_row}')
            for col in range(0, paper.shape[1]):
                if paper[row, col] != 0:
                    paper[target_row, col] = 1
        paper = paper[0:value, :]
    elif axis == 'x':
        # Fold LEFT: indices above value get reflected about the point
        for col in range(value+1, paper.shape[1]):
            target_col = value - (col - value)
            #print(f'{col} --> {target_col}')
            for row in range(0, paper.shape[0]):
                if paper[row, col] != 0:
                    paper[row, target_col] = 1
        paper = paper[:, 0:value]

    return paper


with open(sys.argv[1], 'r') as infile:
    dots = []
    line = infile.readline()
    while line.strip() != '':
        dots.append([ int(v) for v in line.strip().split(',') ])
        line = infile.readline()

    # blank line was the separator
    folds = []
    line = infile.readline()
    while line.strip() != '':
        toks = line.strip().split(' ')
        if not toks[0] == 'fold':
            print('error reading input file')
            sys.exit(1)
        axis,value = toks[2].split('=')
        folds.append([axis, int(value)])
        line = infile.readline()

# X and Y are backwards from a row-major perspective...
cols = max([x for x,y in dots]) + 1
rows = max([y for x,y in dots]) + 1

paper = np.zeros((rows, cols), dtype=int)
for c,r in dots:
    paper[r, c] = 1

#print(paper)
counter = 0
for fold in folds:
    paper = do_fold(paper, fold)
    #print(paper)
    counter += 1
    if counter == MAX_FOLDS:
        print("ENOUGH")
        break

print(np.count_nonzero(paper))

# Draw some blocks - each one will be 10 pixels wide
w = 10 + paper.shape[1] * 10
h = 10 + paper.shape[0] * 10
img = Image.new("RGB", (w,h))
draw = ImageDraw.Draw(img)

for (r, c), value in np.ndenumerate(paper):
    draw.rectangle([c*10, r*10, (c+1)*10, (r+1)*10], "#ffffff" if value == 1 else "#000000")

img.save('output.png')