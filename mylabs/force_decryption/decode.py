from pwn import *
from chall import leak
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def encrypt(string):
    string_hex = string.hex()
    if len(string) != 16:
        exit("Max length is 16 bytes")

    conn.recvuntil(b"> ")
    conn.sendline("enc".encode())
    conn.recvuntil(b"> ")
    conn.sendline(string_hex.encode())

    conn.recvuntil(b": ")
    IV = conn.recvline().strip().decode()
    conn.recvuntil(b": ")
    encrypted = conn.recvline().strip().decode()

    return bytes.fromhex(IV), bytes.fromhex(encrypted)

def decrypt(string, IV):
    string_hex = string.hex()
    IV_hex = IV.hex()

    conn.recvuntil(b"> ")
    conn.sendline("dec".encode())
    conn.recvuntil(b"> ")
    conn.sendline(string_hex.encode())
    conn.recvuntil(b"> ")
    conn.sendline(IV_hex.encode())

    rec_line = conn.recvline().decode().strip()
    line = rec_line.split(':')[0].strip()
    if "Good" not in line:
        print("Flag not found")
        conn.recvuntil(b': ')
        decrypted = conn.recvline().strip().decode()
    else:
        print("Flag found")
        decrypted = rec_line.split(':')[-1].strip()

    return decrypted


# conn = process(["python3", "chall.py"])
conn = remote('130.192.5.212', 6523)


def main():

    data = b"\x01" * 16
    IV, enc_data = encrypt(data)
    newIV = xor(xor(IV, data), leak)
    dec = decrypt(enc_data, newIV)
    print(f"{dec }")


if __name__ == "__main__":
    main()