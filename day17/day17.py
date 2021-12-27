#!/usr/bin/env python3

from enum import Enum
import sys

class Result(Enum):
    OK = 1
    HIT = 2
    MISS = 3

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

if __name__=='__main__':    
    target_x = (20, 30)
    target_y = (-10, -5)
    target = (target_x, target_y)

    state = (0, 0, 17, -4)

    # We know we missed if the current position is past the target area in 
    # either dimension - dx can't go negative, and dy can't become positive 
    # if it's negative
    tick = 0
    result = Result.OK
    while result == Result.OK:
        state = update(state)
        tick += 1
        print('Tick: {0:03d}: {1}'.format(tick, state))
        result = check(state, target)
        if result == Result.MISS:
            print(f"MISS: {state}, {target}")
            break
        elif result == Result.HIT:
            print(f"HIT : {state}, {target}")
            break
        else:
            # keep going
            pass
        if tick > 10:
            print('???')
            break

    