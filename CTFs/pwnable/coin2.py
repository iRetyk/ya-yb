from pwn import *

# Connect to the remote server using pwntools
sh = ssh('coin2', 'pwnable.kr', password='b1naRy_S34rch1Ng_1s_3asy_p3asy', port=2222)

s = sh.process(['nc', '0', '9008'])
s.recv()

def algorithm(N: int, C: int):
    start, end = 0, N
    st = b"-".join([b" ".join([str(n).encode() for n in range(start, end) if n & (1 << bit_pos)]) for bit_pos in range(C)]) + b'\n'

    print("Sets = ", len(st.split(b'-')))
    s.send(st)
    #print(f"send>>>{st}")
    from_server = s.recv(2048).decode()[:-1]
    print(f"{from_server = }")
    answer = 0
    for i, result in enumerate(from_server.split('-')):
        result = int(result)
        if result % 10 == 9:
            answer += (2 ** i)

    send_this = str(answer).encode()
    s.sendline(str(answer).encode())
    print("Send>>>", send_this)
    print("from server-" + s.recvline().decode())




def main():
    while True:
        from_server = s.recvline().decode()
        print("from server in main loop" ,from_server)
        try:
            _, n, c = from_server.split("=")
        except:
            print(s.recvline())
        n, _ = n.split()
        algorithm(int(n), int(c))

main()

