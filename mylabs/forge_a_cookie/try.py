from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from secret import flag
import json, base64

key = get_random_bytes(32)
nonce = get_random_bytes(12)
BASE_STR = '0'*64*2

# {"username": ""}


def f(string):
    string = string.encode()
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ctxt = cipher.encrypt(string)

    print(base64.b64encode(string).decode())
    print(base64.b64encode(ctxt).decode())
    print('-'*50)

    return ctxt

def xor(a, b):
    return bytes([d ^ o for d,o in zip(a, b)])


print(base64.b64encode(key).decode())
print(base64.b64encode(nonce).decode())
print('-'*50)



string = BASE_STR * 4
ctxt = f(string)

k1 = xor(string.encode(), ctxt)


string = '1' * len(BASE_STR)
ctxt = f(string)
try_ctxt = xor(k1, string.encode())

print(base64.b64encode(try_ctxt).decode())
print('-'*50)
print(base64.b64encode(ctxt).decode())

if(try_ctxt == ctxt):
    print('OK')

encoded = base64.b64encode(ctxt).decode()
decoded = base64.b64decode(encoded)


pass