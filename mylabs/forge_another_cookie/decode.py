from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long
from pwn import *
from Crypto.Util.Padding import pad, unpad
import os
from original import sanitize_field

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# conn = process(["python3", "original.py"])
conn = remote("130.192.5.212", 6552)

def construct_cookie(username, s='false'):
    return f"username={sanitize_field(username)}&admin={s}"


def main():


    s = 'true'
    s = pad(s.encode(), AES.block_size)

    '''
        username=aaaaaaa|__inject__|aaaaaaaaa&admin=|false
    '''
    username = "a"*7 + s.decode() + "a"*9

    conn.sendlineafter("Username: ", username.encode())
    cookie = int(conn.recvline().strip())
    cookie = long_to_bytes(cookie)

    chunks = [cookie[i:i+16] for i in range(0, len(cookie), 16)]
    print(len(chunks))

    constructed = chunks[0] + chunks[2] + chunks[1]

    conn.recvuntil(b'> ')
    conn.sendline(b'flag')
    conn.recvuntil(b': ')
    conn.sendline(str(bytes_to_long(constructed)))
    print(conn.recvline())




if __name__ == "__main__":
    main()

    conn.close()