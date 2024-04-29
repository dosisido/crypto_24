from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import json, base64
from pwn import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

conn = process(["python3", "original.py"])

def main():

    """ 
    {"username": "do|true}___ |dosi", "admin": |false} 

    " false}
    """

    username = "do" + pad(b"true}", AES.block_size).decode()  + "dosi"
    username = username.replace("\\\\", '\\')

    conn.recvuntil(b"> ")
    conn.sendline(username.encode())
    conn.recvuntil(b": ")

    token = conn.recvline().strip().decode()
    token = base64.b64decode(token)
    chunks = [token[i:i+16] for i in range(0, len(token), AES.block_size)]
    print("Len chunks: ", len(chunks))
    constructed = chunks[0] + chunks[2] + chunks[1]
    constructed = base64.b64encode(constructed)

    conn.recvuntil(b"> ")
    conn.sendline(b"flag")
    conn.recvuntil(b"> ")
    conn.sendline(constructed)
    print(conn.recvline())

    pass

if __name__ == "__main__":
    main()