from pwn import *
from Crypto.Cipher import AES
import string


KNOWN_PART = 'CRYPTO24'
TOT_PADDING = 10
KEY_SIZE = len("CRYPTO23{}") + 36
PADDING_SIZE = None
CHAR = '0'


# conn = process(['python3', 'chall.py'])
conn = remote('130.192.5.212', 6544)


#CRYPTO24{f18ce0c5-1f07-4f5e-aba0-500b5185

def encrypt(data: str) -> bytes:
    conn.recvuntil(b'> ')
    conn.sendline(b'enc')
    conn.recvuntil(b'> ')
    conn.sendline(data.encode())
    data = conn.readline().strip().decode()
    return data

def find_padding_size():
    global PADDING_SIZE

    tot_padding = 10

    base = 64
    enc = encrypt('a' * base)
    i = 0

    while enc[32:64] != enc[64:96]:
        i+=1
        enc = encrypt('a' * (base + i*2))
    
    PADDING_SIZE = 16-i

    pass

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

    first_padding = ''
    for i in range(TOT_PADDING - PADDING_SIZE):
        for PRNT in [f'{i:02x}' for i in range(256)]:
            print("Pad: " + first_padding + PRNT, end='\r')
            if len(PRNT) != 2: exit("PRNT len must be 2")

            payload = CHAR * padding_len_to_generate_hex                            # toglie il padding dalla finestra
            payload+= CHAR * (block_size_hex * key_blocks - i*2 - 2) + first_padding + PRNT
            payload+= CHAR * (block_size_hex * key_blocks - i*2 - 2)
            
            encrypted = encrypt(payload)
            encrypted = encrypted[padding_blocks * block_size_hex:]

            if encrypted[:block_size_hex * key_blocks] == encrypted[block_size_hex * key_blocks:block_size_hex * 2 * key_blocks]:
                first_padding+= PRNT
                if(len(bytes.fromhex(first_padding)) == KEY_SIZE - 5):
                    return
                break
        else:
            print("WTF")
            return -567
    print("Pad: " + first_padding)


    for i in range(len(flag)//2, block_size_hex//2 * key_blocks):
        for PRNT in string.printable:
            PRNT = PRNT.encode().hex()
            print(bytes.fromhex(flag + PRNT).decode(), end='\r')

            if len(PRNT) != 2: exit("PRNT len must be 2")

            payload = CHAR * padding_len_to_generate_hex                            # toglie il padding dalla finestra
            payload+= CHAR * (block_size_hex * key_blocks - (i+TOT_PADDING - PADDING_SIZE)*2 - 2) + first_padding + flag + PRNT
            payload+= CHAR * (block_size_hex * key_blocks - (i+TOT_PADDING - PADDING_SIZE)*2 - 2)
            
            encrypted = encrypt(payload)
            encrypted = encrypted[padding_blocks * block_size_hex:]

            if encrypted[:block_size_hex * key_blocks] == encrypted[block_size_hex * key_blocks:block_size_hex * 2 * key_blocks]:
                flag+= PRNT
                if(len(bytes.fromhex(flag)) == KEY_SIZE - 5):
                    return
                break
        else:
            exit("WTF")
    print(bytes.fromhex(flag + PRNT).decode())
    

if __name__ == "__main__":
    if PADDING_SIZE is None: find_padding_size()

    main_printable() 

    conn.close()