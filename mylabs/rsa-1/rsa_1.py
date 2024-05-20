from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse
from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
import sys
sys.path.append('../../rsa_textbook_attacks')
from basic_rsa import decrypt


# p, q = getPrime(64), getPrime(64)

p = 12499036198482036913
q = 14417935640429069899
phi = (p-1)*(q-1)
n = p*q
e = 65537
d = inverse(e, phi)
key = RSA.construct((n, e, d))
print(n)
assert n == 180210299477107234107018310851575181787
# m = bytes_to_long(flag)
# print(pow(m,e,n))

c = 27280721977455203409121284566485400046

m = decrypt(c, key)
print(long_to_bytes(m))

#180210299477107234107018310851575181787
#27280721977455203409121284566485400046
