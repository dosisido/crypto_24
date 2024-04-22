from KnownCipherRandomMode import *
from chall import RandomCipherRandomMode
from pwn import *


def calculate_input(otp):
    in_str = '0'*32 + '0'*32

    otp = bytes.fromhex(otp)
    in_str = bytes.fromhex(in_str)
    data = bytes([d ^ o for d,o in zip(in_str,otp)])
    in_str = data.hex()
    return in_str

def split_string(s):
    # Calculate the midpoint
    midpoint = len(s) // 2
    
    # Split the string into two halves
    first_half = s[:midpoint]
    second_half = s[midpoint:]
    
    return first_half, second_half


def proc(conn):
    conn.recvline()

    otp = conn.recvline().strip().split()[-1]
    otp = str(otp, 'utf-8')
    in_str = calculate_input(otp)

    conn.sendline(in_str)

    data = conn.recvline().strip().split()[-1]
    data = str(data, 'utf-8')
    str1, str2 = split_string(data)
    
    conn.recvline()

    if str1 == str2:
        mode = "ECB"
    else:
        mode = "CBC"
    
    conn.sendline(mode)

    if str(conn.recvline(), 'utf-8').strip() != 'OK, next':
        exit('WTF')

def main():
    conn = remote('130.192.5.212', 6531)
    conn = process(["python3", "original.py"])

    for i in range(128):
        print(f"elaboring #{i}")
        proc(conn)
    
    print(str(conn.recvline(), 'utf-8'))
    

    conn.close()
    


if __name__ == "__main__":
    main()