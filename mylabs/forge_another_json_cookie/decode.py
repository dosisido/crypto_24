from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import json, base64
from pwn import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# conn = process(["python3", "original.py"])
conn = remote("130.192.5.212", 6551)

def main():

    """ 
    {"username": "",                   "admin": false}
                    |                |                |                |                |           

    {"username": "do|dosiaaaaaaaaaa",| "admin": false}|
    {"username": "do|dosia", "admin":| false}         |
    {"username": "do|true,           |osia", "admin": |false}         |
    
    {"username": "do| ______________"|, "admin": false|}

    
    ,_______________|
    _______________\|"_______________|fooled__________|
    _______________\|"_______________|: true           }
        
    


    {"username": "do|osia", "admin": |true,           |"_______________|ciao                   | false}         
    0                1                2                3                4                5                6                7
    {"username": "do|true,___________|_______________\|"_______________|fooled__________|:_______________|osia", "admin": |false}          |
                    |                |                |                |                |                |                |                |
    """

    due_punti = ":_______________".replace("_", " ")                    # 80:96
    virgoletta = '_______________"_______________'.replace("_", " ")    # 32:64
    fooled = "fooled__________".replace("_", " ")                       # 64:80
    true = "true,           "                                           # 16:32

            # ' '*(AES.block_size - len("true}")) + \
    username = \
            "do" + \
            true + \
            virgoletta + \
            fooled + \
            due_punti + \
            "dosi"

    conn.recvuntil(b"> ")
    conn.sendline(username.encode())
    conn.recvuntil(b": ")

    token = conn.recvline().strip().decode()
    token = base64.b64decode(token)
    chunks = [token[i:i+16] for i in range(0, len(token), AES.block_size)]
    print("Len chunks: ", len(chunks))
    assert len(chunks) == 8
    constructed = b''
    for i in (0, 6, 1, 3, 4, 3, 5, 7):
        constructed+=chunks[i]
    constructed = base64.b64encode(constructed)

    conn.recvuntil(b"> ")
    conn.sendline(b"flag")
    conn.recvuntil(b"> ")
    conn.sendline(constructed)
    print(conn.recvline())
    print(conn.recvline())
    print(conn.recvline())

    pass

if __name__ == "__main__":
    main()