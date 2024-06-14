from pwn import *
from Crypto.Cipher import AES
import string


KNOWN_PART = ''
PADDING_TOT = 10
KEY_SIZE = len("CRYPTO23{}") + 36 + 10
CHAR = '0'


# conn = process(['python3', 'chall.py'])
conn = remote('130.192.5.212', 6544)

def encrypt(data: str) -> bytes:
    conn.recvuntil(b'> ')
    conn.sendline(b'enc')
    conn.recvuntil(b'> ')
    conn.sendline(data.encode())
    data = conn.readline().strip().decode()

    # data = enc(data)
    return data

def main_printable_bottom():
    block_size = AES.block_size
    block_size_hex = block_size * 2
    flag = ''


    for i in range(len(flag)//2, block_size_hex//2 * key_blocks):
        for PRNT in string.printable:
            PRNT = PRNT.encode().hex()




if __name__ == "__main__":

    main_printable_bottom()

    conn.close()