from pwn import *
from Crypto.PublicKey import RSA
from math import gcd
from Crypto.Util.number import long_to_bytes

e = 65537

conn = remote('130.192.5.212', 6646)
cipher = int(conn.recvline().decode())

# blinding -n
print("Encrypting 2 messages")
# c1 = encrypt(2, key)
# c2 = encrypt(3, key)
conn.sendline(b"e2")
c1 = int(conn.recvline().decode())
conn.sendline(b"e3")
c2 = int(conn.recvline().decode())

n = gcd(2**e - c1, 3**e - c2)

key = RSA.construct((n, e))

c = 2**key.e * cipher % key.n

conn.sendline(f"d{c}".encode())
# two_m = decrypt(c, key)
two_m = int(conn.recvline().decode())


inv_2 = pow(2, -1, key.n)
m = two_m * inv_2 % key.n

print(long_to_bytes(m).decode())