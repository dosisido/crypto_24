from pwn import *
from Crypto.Cipher import AES
import string
from Crypto.Util.Padding import pad, unpad



KNOWN_PART = ''
PADDING_TOT = 10
KEY_SIZE = len("CRYPTO23{}") + 36
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

def find_padding_size():
    global PADDING_SIZE
    base = 64
    enc = encrypt('a' * base)
    i = 0
    while enc[32:64] != enc[64:96]:
        i+=1
        enc = encrypt('a' * (base + i*2))
    
    PADDING_SIZE = 16-i

def main_printable_bottom():
    block_size = AES.block_size
    block_size_hex = block_size * 2
    flag = ''
    key_blocks = KEY_SIZE // block_size



    for i in range(len(flag)//2, block_size_hex//2 * key_blocks):
        for PRNT in string.printable:
            PRNT = PRNT.encode().hex()




if __name__ == "__main__":

    main_printable_bottom()

    conn.close()