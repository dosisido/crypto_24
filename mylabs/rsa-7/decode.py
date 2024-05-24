from pwn import *
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
import decimal

e = 65537


conn = remote('130.192.5.212', 6647)
n = int(conn.recvline().decode())
cipher = int(conn.recvline().decode())
key = RSA.construct((n, e))

decimal.getcontext().prec = n.bit_length()
bounds = (decimal.Decimal(0), decimal.Decimal(key.n))
c = cipher
length = key.n.bit_length()
for i in range(length):
    print(f"Status: {(i+1)/length*100:.2f}%", end="\r")
    c = (pow(2, key.e, key.n) * c) % key.n

    conn.sendline(str(c).encode())
    bit = int(conn.recvline().decode().strip())
    # print(f"Received bit: {bit}", bit==0)

    if  bit == 0:
        bounds = (bounds[0], (bounds[1] + bounds[0])//2)
    else:
        bounds = ((bounds[1] + bounds[0])//2, bounds[1])
print()

print("Bounds:")
for b in bounds:
    print(b)

bounds = (int(bounds[0]), int(bounds[1]))
print("Original message:")
for bound in range(bounds[0], bounds[1]+1):
    print(long_to_bytes(bound).decode())

print("Guess:")
myguess = (long_to_bytes(bounds[0]).decode())[:-1] + '}'
print(myguess)
print(bytes_to_long(myguess.encode()))


