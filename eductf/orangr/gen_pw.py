#!/usr/bin/env python
import random

def gen_co():
    co = []
    while len(co) < 56:
        r = random.randint(0, 55)
        if r in co:
            continue
        co.append(r)
    return co

co = [20, 49, 30, 25, 23, 37, 10, 17, 53, 33, 21, 52, 50, 34, 47, 36, 38, 7, 45, 22, 18, 6, 42, 44, 11, 8, 28, 3, 2, 27, 51, 31, 43, 1, 48, 41, 24, 26, 55, 35, 29, 12, 14, 19, 40, 32, 9, 39, 16, 4, 5, 13, 54, 0, 15, 46]

n = 0
for c in co:
    n = n*56 + c
print n
