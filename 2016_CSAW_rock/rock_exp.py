
fstr='FLAG23456912365453475897834567'

def add_xor_str(s,added,xored):
	ret=''
	for x in s:
		x=ord(x)+added
		x=x^xored
		ret+=chr(x)
	return ret

def decrypt(fstr):
	fstr=add_xor_str(fstr,-9,0x10)
	fstr=add_xor_str(fstr,-20,0x50)
	# these two lines are useless because operations about these two lines
	# in origin program does not has effect on origin input string
	# fstr=add_xor_str(fstr,-35,0x20)
	# fstr=add_xor_str(fstr,0,0x50)
	print fstr

decrypt(fstr)