from pwn import *

conn = None

def xor(a, b):
    return bytes([d ^ o for d,o in zip(a, b)])

def nline():
    return conn.recvline().decode().strip()

def main():
    global conn
    conn = remote('130.192.5.212', 6521)
    conn = process(["python3", "chall.py"])
    print()

    print(nline())

    dosi = 'dosi'*((64*2 - 16)//4)
    # S = '{"username": "{dosi}"}' # 16

    conn.sendline(dosi.encode())

    # print(nline())
    token = nline().split()[-1]
    # print(token)
    nonce, ctxt = token.split('.')
    print(nonce, ctxt)
    ctxt = base64.b64decode(ctxt)
    k1 = xor(dosi.encode(), ctxt)
    print('k1', k1, len(k1))


    for i in range(4):
        nline()
        # print(i, nline())

    conn.sendline('flag'.encode())

    print(nline())


    dosi = 'dosi'*((64*2 - 32)//4)
    T = f'{{"username": "s{dosi}", "admin": true}}'
    ctxt = xor(k1, T.encode())

    send = nonce + '.' + base64.b64encode(ctxt).decode()
    print('send', send)
    conn.sendline(send.encode())
    print(nline())
    print(nline())

    
    print('\n\n')
    conn.close()
    


if __name__ == "__main__":
    main()