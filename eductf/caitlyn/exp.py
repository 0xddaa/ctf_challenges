#!/usr/bin/env python
import sys
from pwn import *
from z3 import *

HOST, PORT = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ('localhost', 5566)
r = remote(HOST, PORT)

def print_board(board, fname=None):
    raw_board = ''
    for row in board:
        for c in row:
            if type(c) == 'str':
                raw_board += c
            else:
                raw_board += '%2d ' % c
        raw_board += '\n'
    if not fname:
        log.info(raw_board)
    else:
        open(fname, 'w').write(raw_board)

def get_board(line):
    board = []
    r.recvline(); r.recvline()
    for i in range(line):
        r.recvuntil('    ')
        board.append(r.recvline().strip().split('  '))

    int_board = []
    for row in board:
        row2 = []
        for c in row:
            row2.append(int(c)) if '-' not in c and '*' not in c else row2.append(0)
        int_board.append(row2)

    return int_board

def find_mine(int_board, line):
    def get_neighbor(x, y):
        n = []
        max_n = 0

        # corner
        if y > 0 and x > 0:
            max_n += 1
            if int_board[y-1][x-1] == 0:
                n.append(smt_board[y-1][x-1])
        if y > 0 and x < line-1:
            max_n += 1
            if int_board[y-1][x+1] == 0:
                n.append(smt_board[y-1][x+1])
        if y < line-1 and x > 0:
            max_n += 1
            if int_board[y+1][x-1] == 0:
                n.append(smt_board[y+1][x-1])
        if y < line-1 and x < line-1:
            max_n += 1
            if int_board[y+1][x+1] == 0:
                n.append(smt_board[y+1][x+1])
        # direction
        if y > 0:
            max_n += 1
            if int_board[y-1][x] == 0:
                n.append(smt_board[y-1][x])
        if y < line-1:
            max_n += 1
            if int_board[y+1][x] == 0:
                n.append(smt_board[y+1][x])
        if x > 0:
            max_n += 1
            if int_board[y][x-1] == 0:
                n.append(smt_board[y][x-1])
        if x < line-1:
            max_n += 1
            if int_board[y][x+1] == 0:
                n.append(smt_board[y][x+1])
        return max_n, n

    smt_board = [[Int("board_{}_{}".format(i, j)) for i in range(line)] for j in range(line)]
    s = Solver()

    for j in range(line):
        for i in range(line):
            if int_board[j][i] == 0:
                s.add(Or(smt_board[j][i] == 0, smt_board[j][i] == -1))  # mine or blank 
                max_n, n = get_neighbor(i, j)
                if len(n) == max_n:
                    s.add(smt_board[j][i] == 0)
            else:
                s.add(smt_board[j][i] == IntVal(int_board[j][i]))       # info constraint
                s.add(sum(get_neighbor(i, j)[1]) == IntVal(-int_board[j][i]))

    assert s.check() == sat, "unsat"

    ans = s.model()
    ans_board = []
    for row in smt_board:
        row2 = []
        for index in row:
            row2.append(ans[index].as_long())
        ans_board.append(row2)

    return ans_board

def send_ans(board):
    for row in board:
        for c in row:
            r.send(str(c) + ' ')
        r.sendline('')

def check_ans(ans_board, line):
    for y in range(line):
        for x in range(line):
            if ans_board[y][x] == -1:
                continue

            count = 0
            # corner
            if y > 0 and x > 0:
                if ans_board[y-1][x-1] == -1:
                    count += 1
            if y > 0 and x < line-1:
                if ans_board[y-1][x+1] == -1:
                    count += 1
            if y < line-1 and x > 0:
                if ans_board[y+1][x-1] == -1:
                    count += 1
            if y < line-1 and x < line-1:
                if ans_board[y+1][x+1] == -1:
                    count += 1
            # direction
            if y > 0:
                if ans_board[y-1][x] == -1:
                    count += 1
            if y < line-1:
                if ans_board[y+1][x] == -1:
                    count += 1
            if x > 0:
                if ans_board[y][x-1] == -1:
                    count += 1
            if x < line-1:
                if ans_board[y][x+1] == -1:
                    count += 1

            assert count == ans_board[y][x], 'not correct answer'

progress = log.progress('level')
for i in range(1, 10):
    progress.status(str(i))
    board = get_board(10*i)
    ans_board = find_mine(board, 10*i)
    check_ans(ans_board, 10*i)
    send_ans(ans_board)
progress.success(r.recvline())
