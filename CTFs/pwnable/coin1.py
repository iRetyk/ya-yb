


from pwn import *
import re
p = remote('pwnable.kr', 9007)
for i in range(100):
	N, C = re.findall(b"N=(\d+) C=(\d+)", p.recv())[0]
	N = int(N)
	C = int(C)
	start, end = 0, N-1
	while start <= end and C > 0:
		mid = (start + end) // 2
		x = " ".join([str(j) for j in range(start, mid+1)])	# build range list
		p.sendline(x)
		res = int(p.recvline()[:-1])
		if res % 10 == 0:
			start = mid+1	# through first half
		else:
			end = mid-1		# through second half
		C -= 1
	while C > 0:	# use all the tries
		p.sendline("0")
		p.recv(1024)	
		C -= 1
	p.sendline(str(start))	# final answer
	print(p.recv())
