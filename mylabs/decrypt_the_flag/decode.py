from pwn import *

conn = None


def xor(a, b):
    return bytes([d ^ o for d,o in zip(a, b)])

def readline(prnt: bool = False) -> str:
    l = conn.recvline().decode().strip()
    if prnt: print(l)
    return l

def sendline(line: str):
    conn.sendline(line.encode())

def main():
    global conn
    conn = remote('130.192.5.212', 6561)
    # conn = process(["python3", "original.py"])
    print()
    
    seed = 0
    readline()
    sendline(str(seed))
    readline()
    secret = bytes.fromhex(readline())
    print(f"{secret= }")

    l = conn.recvline().decode().strip()
    print(l)
    sendline('y')
    readline()
    msg = '0' * 128
    sendline(msg)
    enc = readline()
    enc = bytes.fromhex(enc)

    k = xor(enc, msg.encode())

    plain = xor(secret, k).encode()
    print(f"secret: {plain}")


    
    print('\n\n')
    conn.close()
    
def forzebrutte():
    secret = 'ed7bf2c8ecb739c2e578d93541d33944a28614f9e9950dcb796748bfbc80767bade41c97aac200d1c4cc04399d4d'
    secret = bytes.fromhex(secret)

    msg = '0'*128
    enc = '9e199ba888c83bc6ae2e8d6341d36a42a49b15a8e8c410cf2b6f48a2eed32529b0ed4fc5acca0980cccc0339c8007f3d15c7c64af020df8eca188b191cb27217af971616ede838e2ea0ba8a046f46fa1ab8f6291049e82046bd876c82f76e75993b83cd4274b4bd454aa6b1ba9b754258bd32de495d8f982ec3c4ff82fb3a858'
    k = xor(msg.encode(), bytes.fromhex(enc))

    res = xor(k, secret)
    print('flag: ', res.decode())


if __name__ == "__main__":
    forzebrutte()
    main()