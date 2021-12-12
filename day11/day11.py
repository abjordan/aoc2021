#!/usr/bin/env python3

import numpy as np
import sys

def bump_neighbors(state, r, c):
    if r-1 >= 0:
        for ci in range(max(c-1, 0), min(c+2, state.shape[1])):
            state[ r-1, ci ] += 1

    for ci in range(max(c-1, 0), min(c+2, state.shape[1])):
        if ci == c: continue
        state[ r, ci ] += 1

    if r+1 < state.shape[1]:
        for ci in range(max(c-1, 0), min(c+2, state.shape[1])):
            state[ r+1, ci ] += 1        

def evolve(state):
    #print("---- PRE  ----")
    #print(state)

    flashed = np.zeros_like(state, dtype=bool)

    # Energy of all octopi += 1
    state = state + np.ones_like(state)
    
    # Anybody with energy > 9 flashes; have to repeat this until it 
    # converges (i.e., no new flashes)
    last_flashed = None
    num_flashed = 0
    rounds = 0
    while num_flashed != last_flashed:
        rounds += 1
        last_flashed = num_flashed
        for (r,c), val in np.ndenumerate(state):
            if val > 9:
                #print(f'FLASHED: {r}, {c} {flashed[r,c]}')
                if flashed[r, c] == False:
                    flashed[r, c] = True
                    num_flashed += 1
                    bump_neighbors(state, r, c)
    print(f'Converged with {num_flashed} flash(es) after {rounds} rounds')

    # Anybody that flashed gets their energy reset to 0
    state[flashed] = 0
    #print("---- POST ----")
    #print(state)

    return num_flashed, state

if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print('USAGE: day11.py input_file iterations')
        sys.exit(1)

    steps = int(sys.argv[2])

    with open(sys.argv[1], 'r') as infile:
        lines = infile.readlines()
        lines = [ [int(x) for x in s.strip()] for s in lines ]
        state = np.array(lines)

        flashes = 0
        # Guess how much time I spent figuring out that my part two
        # answer was wrong because I was zero-indexing the steps?
        for i in range(1, steps+1):
            print(f'{i:4d}: ', end='')
            num_flashes, state = evolve(state)
            flashes += num_flashes
            if np.count_nonzero(state) == 0:
                print(f'Simultaneous megaflash after {i} steps')
                break

        print('Total flashes after {} step(s): {}'.format(i, flashes))
        #print('Final state:')
        #print(state)