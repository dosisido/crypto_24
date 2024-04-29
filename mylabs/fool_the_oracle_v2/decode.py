from pwn import *
from Crypto.Cipher import AES
from chall import encrypt as enc
import string


KNOWN_PART = ''
KEY_SIZE = 46
PADDING_SIZE = 5
CHAR = '0'.encode()


conn = process(['python3', 'original.py'])
# conn = remote('130.192.5.212', '6542')

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
    padding_len_to_generate_hex = padding_len_to_generate * 2
    n_bloks = 8
    padding_bloks = PADDING_SIZE // block_size
    if PADDING_SIZE % block_size != 0: padding_bloks += 1
    
    padding_len_to_generate = block_size - padding_len

    for i in range(len(known)//2, block_size_hex//2 * n_bloks):
        for PRNT in string.printable:
            PRNT = PRNT.encode().hex()
            if len(PRNT) != 2:
                exit("PRNT len must be 2")
            payload = blank_char * (padding_len_to_generate_hex + block_size_hex * n_bloks - i*2 - 2) + known + PRNT
            padding = blank_char * (padding_len_to_generate_hex + block_size_hex * n_bloks - i*2 - 2)
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
    main_printable()

    conn.close()