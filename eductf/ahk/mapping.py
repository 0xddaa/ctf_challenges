#!/usr/bin/env python
import string

key = '651ddd53164f98cdc04684bd254c0c2a8b4089ec4ebb52833ea83584883ad2425e61382cbbfbc0e020cf9520d158bddad4f678766a1d62b0e3eec842a5c441fc9f48993d626f55788b852e86f6094ea599a11cfb5e7d3640d49b6c93894c942fb497ae1e'.decode('hex')

chars = 'abcdefghijklmnopqrstuvwxyz0123456789_'
mapping = {}
for i, c in enumerate(chars):
    tmp = ord(c) ^ ord(key[i])
    assert tmp not in mapping.values(), 'gg'
    mapping[c] = chr(tmp).encode('hex')


flag = "l0c4l_stud3nts_n33d_b4sic_p0ints"
# d105bee6d1e4fa983b37092298fae422090937e47fe6faa9bee45a05a92298fa
flag_enc = ''.join([mapping[c] for c in flag])
print flag_enc
ahk_code = ''
for c in chars:
    ahk_code += ':O:@{}::{}\n'.format(c, mapping[c])
open('enc.ahk', 'w').write(ahk_code)
