#!/usr/bin/env python3

import sys

# Each input is ten unique signal patterns, a | delimiter, and the 4 digit output value.

# Part 1: in the output values, how many times do digits 1, 4, 7, or 8 appear?
# 1 is two segments, 7 is three segments, 7 is four segments, and 8 is 7 segments
# so the count is the number of tokens with that many characters in each line after
# the pipe

#    aaaa
#   b    c
#   b    c
#    dddd
#   e    f
#   e    f
#    gggg

def translate_output(signal_strs, output):

    signal = [ set( [ x for x in blob ] ) for blob in signal_strs ]
    
    one = [ x for x in signal if len(x) == 2 ][0]
    four = [ x for x in signal if len(x) == 4][0]
    seven = [ x for x in signal if len(x) == 3][0]
    eight = [ x for x in signal if len(x) == 7][0]
    six_nine_zero = [ x for x in signal if len(x) == 6]
    two_three_five = [x for x in signal if len(x) == 5]

    a, b, c, d, e, f, g = ["?"]*7
    
    # segment a is four - one
    a = seven - one
    
    # If you remove the six segments from eight, you should end up 
    # with only segment C lit up. If there's an intersection with
    # one, that means that the value we used was a six. If not, 
    # then it was a nine
    for test in six_nine_zero:
        if len(one.intersection(eight - test)) == 1:
            six = test
        elif len(four.intersection(eight - test - one)) == 1:
            zero = test
        else:
            nine = test
    
    e = eight - nine
    c = eight - six
    d = eight - zero

    aeg = eight - four
    g = aeg - a - e

    bd = four - one
    b = bd - d
    
    # f is the only one left
    f = eight - a - b - c - d - e - g

    for cand in two_three_five:
        if e == six - cand:
            five = cand
            break
    two_three_five.remove(five)
    
    # print(f"a: {a}, b: {b}, c: {c}, d: {d}, e: {e}, f: {f}, g: {g}")
    
    two = eight - b - f
    three = eight - b - e
    
    translated = []
    for symbol in output:
        segments = set( [ x for x in symbol ])
        if segments == one:
            translated.append("1")
        elif segments == two:
            translated.append("2")
        elif segments == three:
            translated.append("3")
        elif segments == four:
            translated.append("4")
        elif segments == five:
            translated.append("5")
        elif segments == six:
            translated.append("6")
        elif segments == seven:
            translated.append("7")
        elif segments == eight:
            translated.append("8")
        elif segments == nine:
            translated.append("9")
        elif segments == zero:
            translated.append("0")
        else:
            print("???", segments)

    return int("".join(translated))


signals = []
outputs = []
with open(sys.argv[1], "r") as infile:
    for line in infile.readlines():
        signals.append(line.strip().split("|")[0].strip().split(" "))
        outputs.append(line.strip().split("|")[1].strip().split(" "))

def filt(x):
    if len(x) == 2 or len(x) == 3 or len(x) == 4 or len(x) == 7:
        return True
    return False

total = 0
for o in outputs:
    total += len(list(filter(filt, o)))

print(f"Number of easy ones: {total}")

acc = 0
for idx, signal in enumerate(signals):
    acc += translate_output(signal, outputs[idx])

print(acc)