#!/usr/bin/env python3

from enum import Enum
import sys

class Result(Enum):
    OK = 1
    HIT = 2
    MISS = 3
    TIMEOUT = 4

def update(state):
    x, y, dx, dy = state
    x_1 = x + dx
    y_1 = y + dy
    if dx != 0:
        dx_1 = (dx - 1) if dx > 0 else (dx + 1)
    else:
        dx_1 = 0
    dy_1 = dy - 1

    return (x_1, y_1, dx_1, dy_1)

def check(state, target):
    x, y, _, _ = state
    (tx_min, tx_max), (ty_min, ty_max) = target
    if (x in range(tx_min, tx_max)) and (y in range(ty_min, ty_max)):
        return Result.HIT
    elif not ((state[0] <= target[0][1]) and (state[1] >= target[1][0])):
        return Result.MISS
    else:
        return Result.OK

def simulate(state, target):

    max_height = state[1]

    # We know we missed if the current position is past the target area in 
    # either dimension - dx can't go negative, and dy can't become positive 
    # if it's negative
    tick = 0
    result = Result.OK
    while result == Result.OK:
        state = update(state)
        max_height = max(state[1], max_height)

        tick += 1
        #print('Tick: {0:03d}: {1}'.format(tick, state))
        result = check(state, target)
        if result == Result.MISS:
            #print(f"MISS: {max_height} : {state}, {target}")
            break
        elif result == Result.HIT:
            #print(f"HIT : {max_height} : {state}, {target}")
            break
        else:
            # keep going
            pass
        if tick > 10000:
            result = Result.TIMEOUT
            break
    return result, max_height

if __name__=='__main__':    
    #target_x = (20, 30)
    #target_y = (-10, -5)

    target_x = (195,238)
    target_y = (-93,-67)
    target = (target_x, target_y)

    max_max = 0
    argmax = (0,0)

    timeouts = 0
    for dx in range(0, 100):
        for dy in range(0, 100):
            state = (0, 0, dx, dy)
            #print(f"Velocity: {(dx, dy)}: ", end="")
            result, max_height = simulate(state, target)
            if result == Result.HIT and max_height >= max_max:
                max_max = max(max_height, max_max)
                argmax = (dx, dy)
            elif result == Result.TIMEOUT:
                timeouts += 1
                print('T', end='')
                sys.stdout.flush()
    print(f"Maximum height: {max_max} with initial vel. {argmax}")
    print(f"Had {timeouts} timeouts")
    