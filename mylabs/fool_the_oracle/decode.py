from pwn import *
from tmp import gen_byte
from Crypto.Cipher import AES
from chall import encrypt as enc
import string

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# conn = process(['python3', 'original.py'])
conn = remote('130.192.5.212', '6541')

def encrypt(data: str) -> bytes:
    conn.recvuntil(b'> ')
    conn.sendline(b'enc')
    conn.recvuntil(b'> ')
    conn.sendline(data)
    data = conn.readline().strip().decode()

    # data = enc(data)
    return data

def main_hex():
    flag = 'CRYPTO24{59'.encode().hex()
    blank_char = '0'
    block_size = AES.block_size
    block_size_hex = block_size * 2
    n_bloks = 6

    """
    __blank__flag|__blank__flag
    """

    known = flag
    for i in range(len(known), block_size_hex//2 * n_bloks):
        for HEX in gen_byte():
            payload = blank_char * (block_size_hex * n_bloks - i - 2) + known + HEX
            padding = blank_char * (block_size_hex * n_bloks - i - 2)
            encrypted = encrypt(payload + padding)
            # print(payload, padding, sep='\n')
            if encrypted[:block_size_hex * n_bloks] == encrypted[block_size_hex * n_bloks:block_size_hex * 2 * n_bloks]:
                known+= HEX
                print(bytes.fromhex(known).decode('utf-8'))
                if(known[-1] == '}'):
                    return
                break
        else:
            exit('WTF')
    
def main_printable():
    flag = 'CRYPTO24{5'.encode().hex()
    blank_char = '0'
    block_size = AES.block_size
    block_size_hex = block_size * 2
    n_bloks = 6

    """
    __blank__flag|__blank__flag
    """

    known = flag
    for i in range(len(known)//2, block_size_hex//2 * n_bloks):
        for PRNT in string.printable:
            PRNT = PRNT.encode().hex()
            if len(PRNT) != 2:
                exit("PRNT len must be 2")
            payload = blank_char * (block_size_hex * n_bloks - i*2 - 2) + known + PRNT
            padding = blank_char * (block_size_hex * n_bloks - i*2 - 2)
            encrypted = encrypt(payload + padding)
            # print(payload, padding, sep='\n')
            if encrypted[:block_size_hex * n_bloks] == encrypted[block_size_hex * n_bloks:block_size_hex * 2 * n_bloks]:
                known+= PRNT
                print(bytes.fromhex(known).decode('utf-8'))
                if(known[-1] == '}'):
                    return
                break
        else:
            exit('WTF')

if __name__ == "__main__":
    # main_hex()
    main_printable()

    conn.close()