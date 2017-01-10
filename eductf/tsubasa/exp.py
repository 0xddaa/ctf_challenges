#!/usr/bin/env python

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_" 

dump_r = open('dump_rand', 'r').read().strip().split('\n')
secrets = []
for i in xrange(0, len(dump_r), 16):
    secret = ''
    for j in range(16):
        secret += chars[int(dump_r[i + j].split('= ')[1], 16) % len(chars)]
    secrets.append(secret)

chunk_sizes = [int(s) for s in open('chunk_size', 'r').read().strip().split('\n')]

chunks = dict()
for i in xrange(len(secrets)):
    chunks[chunk_sizes[i]] = secrets[i]

t = ''
for k in sorted(chunks):
    t += chunks[k]

flag = t[24] + t[37] + t[52] + t[62] + t[79] + t[94] \
    + t[95] + t[129] + t[208] + t[292] + t[364] + t[601] \
    + t[663] + t[764] + t[897] + t[955] + t[1057] + t[1179] \
    + t[1186] + t[1224] + t[1324] + t[1448] + t[1496] \
    + t[1545] + t[1548] + t[1552] + t[1674] + t[1927] \
    + t[1933] + t[2019] + t[2172] + t[2222] + t[2271] \
    + t[2287] + t[2350] + t[2360] + t[2413] + t[2430]

print flag
