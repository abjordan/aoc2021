#!/usr/bin/env python3

import numpy as np
import sys

from itertools import groupby

def check_board(board, cover):
    score = None
    # Check to see if there's a row where the sum(cover) == 5
    row_check = (cover.sum(-1) == 5)
    col_check = (cover.sum(0) == 5)
    if (True in row_check) or (True in col_check):
        to_count = board[ cover == 0 ]
        score = sum(to_count)
        #print(f"WINNER! Board score is {score}")
    return score
    
boards = {}
covers = {}
calls = []

first_winner = True
if len(sys.argv) == 1:
    print("USAGE: day04.py DATA_FILE <do_b>")
    print("  If given a second argument (value irrelevant), do part B")
    sys.exit(1)

if len(sys.argv) > 2:
    first_winner = False

with open(sys.argv[1], "r") as inf:
    # First line is the numbers called, in order
    calls = [ int(x) for x in inf.readline().strip().split(",") ]
    blank = inf.readline()

    raw_boards = [ x.strip() for x in inf.readlines() ]

    # groupby is pretty neat: https://docs.python.org/3/library/itertools.html#itertools.groupby
    # Using bool as the key function takes advantage of the fact that '' is the only non-truthy string
    str_boards = [ list(b) for k, b in groupby(raw_boards, key=bool) if  k ]
    
    board_id = 0
    for str_board in str_boards:
        # Well, if nothing else, I'm getting better at list comprehensions...
        board = [ np.stack([int(c) for c in r.split()]) for r in str_board ]
        boards[board_id] = np.array(board)
        covers[board_id] = np.zeros_like(boards[board_id])
        board_id += 1

found = False
winners = []
round = 0
for call in calls:
    if found and first_winner: break
    
    round += 1
    
    for id, board in boards.items():
        if id in winners: continue
        cover = covers[id]
        # Use the board matrix to flip the values in the covers matrix: see Boolean Indexing in the numpy docs
        cover[(board == call).nonzero()] = 1
        score = check_board(board, cover)
        if score is not None:
            print(f"Winning board found in round {round}! Board {id}'s total score is {call} * {score} = { call * score }")
            found = True
            winners.append(id)
            if first_winner: break

    if len(winners) == len(boards.keys()):
        break