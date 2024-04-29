from pwn import *
from Crypto.Cipher import AES
from chall import encrypt as enc
import string


KNOWN_PART = 'CRYPTO24{'
KEY_SIZE = 46
PADDING_SIZE = 5
CHAR = '0'


# conn = process(['python3', 'original.py'])
conn = remote('130.192.5.212', '6542')

def encrypt(data: str) -> bytes:
    conn.recvuntil(b'> ')
    conn.sendline(b'enc')
    conn.recvuntil(b'> ')
    conn.sendline(data.encode())
    data = conn.readline().strip().decode()

    # data = enc(data)
    return data

  
def main_printable():
    flag = KNOWN_PART.encode().hex()
    block_size = AES.block_size
    block_size_hex = block_size * 2

    padding_blocks = PADDING_SIZE // block_size
    if PADDING_SIZE % block_size != 0: padding_blocks += 1
    padding_len_to_generate = padding_blocks * block_size - PADDING_SIZE
    padding_len_to_generate_hex = padding_len_to_generate * 2
    
    key_blocks = KEY_SIZE // block_size
    if KEY_SIZE % block_size != 0: key_blocks += 1

    tot_bloks = padding_blocks + key_blocks * 2


    for i in range(len(flag)//2, block_size_hex//2 * key_blocks):
        for PRNT in string.printable:
            PRNT = PRNT.encode().hex()
            if len(PRNT) != 2: exit("PRNT len must be 2")

            payload = CHAR * padding_len_to_generate_hex                            # toglie il padding dalla finestra
            payload+= CHAR * (block_size_hex * key_blocks - i*2 - 2) + flag + PRNT
            payload+= CHAR * (block_size_hex * key_blocks - i*2 - 2)
            
            encrypted = encrypt(payload)
            encrypted = encrypted[padding_blocks * block_size_hex:]

            if encrypted[:block_size_hex * key_blocks] == encrypted[block_size_hex * key_blocks:block_size_hex * 2 * key_blocks]:
                flag+= PRNT
                printable_flag = bytes.fromhex(flag).decode('utf-8')
                print(printable_flag)
                if(len(printable_flag) == KEY_SIZE):
                    return
                break
        else:
            exit('WTF')

if __name__ == "__main__":
    main_printable()

    conn.close()