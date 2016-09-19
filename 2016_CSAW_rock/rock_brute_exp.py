from pwn import *

def testn(ps,n):
	for x in range(33,127):
		nows=ps[:n]+chr(x)+ps[n+1:]
		p=process('rock')
		p.sendline(nows)
		recv=p.recvall()
		# get number
		final=recv[-2] if n<10 else recv[-3:-1]
		p.close()
		print 'recv: '+recv[-10:]
		try:
			if int(final)==n:
				continue
			else:
				return nows
		except Exception as e:
			return nows
		

s='ABCDEFGHIJKLMNOPQRSTUVWXYZABCD'
for i in range(0,30):
	print '------------------------------------'+str(i)+'-------------------------------------'
	s=testn(s,i)
print s
	

