#!/usr/bin/python3
from pwn import *

address = 'cryptotask2022.tailcall.net'
port = '30006'

def receive_welcome_msg(p):
    for _ in range(7):
        p.recvline()

# The warmup challenge
# The server sends a prime number `m` and receives our `base`.
# It then asks a 1000 times for some number `guess`.
# If `guess = base^exp (mod m)`, then we get a point. 
# 300 correct guesses result in us getting the flag.
# exp <- {2, ..., m-1}
# (m-1)^exp = (-1)^exp = 1 if 2|exp, -1 otherwise
# Because of this, inputting `guess = m-1` will score us a point
# around half of the time. 
# A 1000 tries is very generous and is enough to get the flag.
def solve_warmup(p):
    p.send(b'1\n')

    m = int(p.recvline()[4:-1].decode('utf-8'))
    base = str(m-1) + '\n'
    
    p.recv(5)
    p.send(base.encode('utf-8'))

    for _ in range(1000):
        p.send(b'1\n')

    return p.readall()[-39:-6].decode('utf-8')

p = remote(address, port)
receive_welcome_msg(p)
print(solve_warmup(p)) # flag{now-you-see-me-now-you-dont}
