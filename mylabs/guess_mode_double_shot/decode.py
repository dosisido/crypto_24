from pwn import *

data = '00' * 32
data = data.encode()


def process_line(conn):
    conn.recvuntil(b": ")
    conn.sendline(data)
    conn.recvuntil(b": ")
    line = conn.recvline().strip().decode()
    conn.recvuntil(b": ")
    conn.sendline(data)
    conn.recvuntil(b": ")
    line2 = conn.recvline().strip().decode()
    if line == line2:
        return "ECB"
    else:
        return "CBC"


def main():
    # conn = process(["python3", "original.py"])
    conn = remote('130.192.5.212', 6532)

    for i in range(128):
        print(f"Processing #{i+1}")
        mode = process_line(conn)
        conn.recvuntil(b')\n')
        conn.sendline(mode)
        line = conn.recvline().strip().decode()
        if 'OK' not in line:
            exit("Error")
    else:
        print(conn.recvline().strip().decode())
        conn.close()

if __name__ == "__main__":
    main()