from pwn import *
from Crypto.Cipher import AES
import string


KNOWN_PART = ''
KEY_SIZE = len("CRYPTO23{}") + 36
PADDING_SIZE = None
CHAR = '0'


# conn = process(['python3', 'chall.py'])
conn = remote('130.192.5.212', 6543)

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

    max_padding = 15
    block_size = AES.block_size

    encrypted = encrypt('')
    originallen = len(bytes.fromhex(encrypted))
    print(f"{originallen= }")
    
    for added_chars in range(0, max_padding):
        encrypted = encrypt(CHAR*2*added_chars)
        newlen = len(bytes.fromhex(encrypted))
        # print(added_chars, newlen)
        if newlen != originallen:
            break
    else: exit('WTF')

    print(newlen, originallen, added_chars, 16-added_chars)
    PADDING_SIZE = 16-added_chars + 2

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
    print(conn.recvline().decode().strip())
    if PADDING_SIZE is None: find_padding_size()
    print(f'PADDING_SIZE: {PADDING_SIZE}')

    main_printable()

    conn.close()