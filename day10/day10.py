#!/usr/bin/env python3

from queue import LifoQueue
from statistics import median
import sys

OPENERS = '([{<'
CLOSERS = ')]}>'

matcher = {
    '<': '>',
    '[': ']',
    '{': '}',
    '(': ')'
}

error_scorer = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

autocomplete_scorer = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

# Return autocomplete_score, error_score
def score_line(line):
    stack = LifoQueue()
    for ch in line:
        if ch in OPENERS:
            print(ch, end='')
            stack.put(ch)
        elif ch in CLOSERS:
            print(ch, end='')
            q = stack.get()
            if ch != matcher[q]:
                print(' ! error')
                return 0, error_scorer[ch]
    
    print('  INC: ', end='')
    if stack.empty():
        return 0, 0
    score = 0
    while not stack.empty():
        q = stack.get()
        score = 5 * score + autocomplete_scorer[q]
        print(q, end='')
    print(f' = {score}')
    return score, 0

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as infile:

        total_error = 0
        ac_scores = []
        for line in infile.readlines():
             ac, error = score_line(line.strip())
             if ac:
                ac_scores.append(ac)
             total_error += error

        median_ac = median(ac_scores)
        print(f'Median autocomplete score: {median_ac}')
        print(f'Total error score        : {total_error}')