from pwn import *
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long

conn = remote('130.192.5.212', 6645)

e = 65537
n = int(conn.recvline().decode())
cipher = int(conn.recvline().decode())
# print(f"{n= }")
# print(f"{cipher= }")

key = RSA.construct((n, e))

c = 2**key.e * cipher % key.n

conn.sendline(f"d{c}")
# two_m = decrypt(c, key)
two_m = int(conn.recvline().decode())


inv_2 = pow(2, -1, key.n)
m = two_m * inv_2 % key.n

print(long_to_bytes(m).decode())