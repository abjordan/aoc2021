#!/usr/bin/env python3

import numpy as np
import sys

with open(sys.argv[1], 'r') as infile:
    lines = infile.readlines()
    lines = [ [int(x) for x in s.strip()] for s in lines ]
    heightmap = np.array(lines)
    #print(heightmap)

    low_points = []

    acc = 0
    rows, cols = heightmap.shape
    for (r,c), val in np.ndenumerate(heightmap):
        left = heightmap[r, c-1] if (c-1 >= 0) else float('inf')
        up = heightmap[r-1, c] if (r-1 >= 0) else float('inf')
        right = heightmap[r, c+1] if (c+1 < cols) else float('inf')
        down = heightmap[r+1, c] if (r+1 < rows) else float('inf')

        if val < min([up, left, right, down]):
            #print(f"Found low point: ({r},{c}) {val}: {left}, {up}, {right}, {down}")
            acc += (val + 1)
            low_points.append((r, c))

    print(f'Sum of low point risk values: {acc}')

    print(f'Low points: {low_points}')

    def scan(start):
        #print(f'    Scanning from {start}')
        ri, ci = start
        new_pts = set([])
        # Scan left 
        ci -= 1
        while ci >= 0:
            if heightmap[ri, ci] != 9:
                new_pts.add( (ri, ci) )
                ci -= 1
            else:
                break
        # Scan right
        ri, ci = start
        ci += 1
        while ci < cols:
            if heightmap[ri, ci] != 9:
                new_pts.add( (ri, ci) )
                ci += 1
            else:
                break
        # Scan up
        ri, ci = start
        ri -= 1
        while ri >= 0:
            if heightmap[ri, ci] != 9:
                new_pts.add( (ri, ci) )
                ri -= 1
            else:
                break
        # Scan down
        ri, ci = start
        ri += 1
        while ri < rows:
            if heightmap[ri, ci] != 9:
                new_pts.add( (ri, ci) )
                ri += 1 
            else:
                break

        #print(f"    Found new points: {new_pts}")
        return new_pts

    # Ok - to calculate the basin, you do a flood of the matrix 
    # from the low point until you hit a 9
    basins = []
    for low_point in low_points:
        basin = set([low_point])

        new_points = scan(low_point)
        while len(new_points) > 0:
            seed =  new_points.pop()
            basin.add(seed)
            more = scan(seed)
            basin.update(more)
            really_new = more - basin            
            if len(really_new) > 0:
                new_points.update(really_new)
        basins.append(basin)

    sizes = [ len(basin) for basin in basins ]
    print(np.prod(sorted(sizes, reverse=True)[0:3]))
