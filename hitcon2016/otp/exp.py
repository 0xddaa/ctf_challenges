#!/usr/bin/env python
import sys
import struct
from hashlib import sha1
from pwn import *

def _left_rotate(n, b):
    """Left rotate a 32-bit integer n by b bits."""
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def _gcry_sha1_mixblock(chunk, h0, h1, h2, h3, h4):
    """Process a chunk of data and return the new digest variables."""
    assert len(chunk) == 64

    w = [0] * 80

    # Break chunk into sixteen 4-byte big-endian words w[i]
    for i in range(16):
        w[i] = struct.unpack(b'>I', chunk[i*4:i*4 + 4])[0]

    # Extend the sixteen 4-byte words into eighty 4-byte words
    for i in range(16, 80):
        w[i] = _left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)
    
    # Initialize hash value for this chunk
    a = h0
    b = h1
    c = h2
    d = h3
    e = h4
    
    for i in range(80):
        if 0 <= i <= 19:
            # Use alternative 1 for f from FIPS PB 180-1 to avoid bitwise not
            f = d ^ (b & (c ^ d))
            k = 0x5A827999
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i <= 59:
            f = (b & c) | (b & d) | (c & d) 
            k = 0x8F1BBCDC
        elif 60 <= i <= 79:
            f = b ^ c ^ d
            k = 0xCA62C1D6
   
        a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff, 
                        a, _left_rotate(b, 30), c, d)
    
    # Add this chunk's hash to result so far
    h0 = (h0 + a) & 0xffffffff
    h1 = (h1 + b) & 0xffffffff 
    h2 = (h2 + c) & 0xffffffff
    h3 = (h3 + d) & 0xffffffff
    h4 = (h4 + e) & 0xffffffff
    
    return flat(h0, h1, h2, h3, h4).encode('hex')

def predict(hashbuf): 
    h0 = u32(hashbuf[0:4])
    h1 = u32(hashbuf[4:8])
    h2 = u32(hashbuf[8:12])
    h3 = u32(hashbuf[12:16])
    h4 = u32(hashbuf[16:20])
    return _gcry_sha1_mixblock(hashbuf, h0, h1, h2, h3, h4)

r = remote('localhost', 5566)

r.recvuntil('> ')
r.sendline('2')
r.recvuntil('> ')
r.sendline('3')
r.recvuntil('> ')
r.sendline('1')
r.recvuntil('len?\n')
r.sendline(str(580))
r.recvuntil('data?\n')
r.send('\x00'*(580))
r.recvuntil('encrypt content:\n')

cipher = r.recv().strip().decode('hex')
flag = cipher[580:]
key = cipher[:580].ljust(600, '\x00')

g = predict(key[-40:-20]+key[0:44]).decode('hex')

c = ''
for i in range(len(g)):
    c += chr(ord(g[i]) ^ ord(flag[i]))
    
print c
