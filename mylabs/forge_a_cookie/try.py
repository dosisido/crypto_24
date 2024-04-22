from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from secret import flag
import json, base64

key = get_random_bytes(32)
nonce = get_random_bytes(12)
cipher = ChaCha20.new(key=key, nonce=nonce)

print(base64.b64encode(key).decode())
print('-'*50)

string = '0'*64*2

ctxt = cipher.encrypt(string.encode())

print(string)
print(base64.b64encode(ctxt).decode())
print('-'*50)

string+= string

cipher = ChaCha20.new(key=key, nonce=nonce)
ctxt = cipher.encrypt(string.encode())

print(string)
print(base64.b64encode(ctxt).decode())
print('-'*50)

string+= string

cipher = ChaCha20.new(key=key, nonce=nonce)
ctxt = cipher.encrypt(string.encode())

print(string)
print(base64.b64encode(ctxt).decode())
print('-'*50)

