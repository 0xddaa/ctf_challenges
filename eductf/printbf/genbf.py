#!/usr/bin/env python

key = "kDW~cHfd@`!|P58\\'g]|I?$e7x# 489^"

def enc(flag):
    return ''.join([chr(ord(flag[i]) ^ ord(key[i % len(key)])) for i in range(len(flag))])

flag = 'CTF{fm7_vuln_1s_7ur1ng_c0mpl373}'[::-1]
assert len(flag) <= 32, 'too long'
flag_enc = enc(flag)
assert '\x00' not in flag_enc

exp = ''

"""
0x0000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00     ; reg
0x0010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00     ; reg 
0x0020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x0030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00     ; key 
0x0040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00     ; key 
0x0050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x0060: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00     ; flag
0x0070: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00     ; flag
0x0080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x0090: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00     ; data
0x00a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00     ; data
"""

# count = data[0] = 0x20
count = 0x20
exp += '>'*0x91 + '+'*count + '<'*0x91

# make enc flag
exp += '>'*0x60
for c in flag_enc:
    exp += '+' * ord(c) + '>'
exp += '<'*0x80

# make random key 
exp += '>'*0x30 
exp += ''.join(['{}>'.format('+'*ord(c)) for c in key])
exp += '<'*0x50

# read input at cell[1]
loop = '<'*0x91 + '>,<'

# read last random key to cell[2]
loop += '>'*0x30 + '[>]<' + '[{}+{}-]'.format('[<]'+'<'*0x2d, '<<'+'>'*0x30+'[>]<') + '<[<]>' + '<'*0x30
# xor
loop += '[-]>>>' + '[-]>'*0x1d + '<'*0x20
loop += '-[[>>>>>>[>>>]++[-<<<]<<<-]>]>>>[<]>[[>[>-<-]>[<<<<<<+>>>>>>[-]]>]+[<[<<<++>>>-]<<]>>]<<<<<'
# read flag to cell[1]
loop += '>'*0x60 + '[>]<' + '[{}+{}-]'.format('[<]'+'<'*0x5e, '<'+'>'*0x60+'[>]<') + '<[<]>' + '<'*0x60
# xor
loop += '[-]>>>' + '[-]>'*0x1d + '<'*0x20
loop += '-[[>>>>>>[>>>]++[-<<<]<<<-]>]>>>[<]>[[>[>-<-]>[<<<<<<+>>>>>>[-]]>]+[<[<<<++>>>-]<<]>>]<<<<<'

# add result to data[1]
loop += '>>[<<{}+{}>>-]<<'.format('>'*0x93, '<'*0x93) # xor[data[1]+xor-]

# count--, count = data[0]
loop += '>'*0x91 + '-'

exp += '{}[{}]'.format('>'*0x91, loop)

# puts("gg") if failed
gg = '<{}..{}.<'.format('+'*ord('g'), '-'*(ord('g') - 0xa))
exp += '{}[{}]<<'.format('<'*0x91 + '>'*0x93, gg)

open('bf', 'w').write(exp)
