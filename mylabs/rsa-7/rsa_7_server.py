from Crypto.Util.number import bytes_to_long, getPrime, inverse
from secret import flag

p,q = getPrime(512), getPrime(512)
n = p*q
e = 65537
m = bytes_to_long(flag)
phi = (p-1)*(q-1)
d = inverse(e,phi)

print(n)                    # message
print(pow(m,e,n))           # ciphertext

while True:
    req = input()
    dec = pow(int(req),d,n)
    print(dec%2)