from pwn import *
import json

conn = None


def xor(a, b):
    return bytes([d ^ o for d,o in zip(a, b)])

def nline():
    return conn.recvline().decode().strip()

def create_user_token(name):
    token = json.dumps({
        "username": name,
        # "admin": True
    })
    # print(token)
    return token.encode()


def main():
    global conn
    conn = remote('130.192.5.212', 6521)
    # conn = process(["python3", "original.py"])
    
    print()

    nline()

    dosi = 'dosi'*((64*2 - 16)//4)

    conn.sendline(dosi.encode())
    user_string = create_user_token(dosi)

    print(nline())

    token = nline().split()[-1]
    nonce, ctxt = token.split('.')
    print(nonce, ctxt)
    ctxt = base64.b64decode(ctxt)
    print('ctxt len:', len(ctxt))
    k1 = xor(user_string, ctxt)
    print('k1', k1, len(k1))


    for i in range(4):
        nline()
        # print(i, nline())

    conn.sendline('flag'.encode())

    response = nline()


    dosi = 'dosi'*((64*2 - 32)//4)
    T = f'{{"username": "s{dosi}", "admin": true}}'
    ctxt = xor(k1, T.encode())

    send = nonce + '.' + base64.b64encode(ctxt).decode()
    print('send', send)
    conn.sendline(send.encode())

    response = nline()
    if 'You are admin!' not in response:
        print(response)
        exit("Failed to be admin")

    nline()
    flag = nline()

    print(f'{flag= }')

    
    print('\n\n')
    conn.close()
    


if __name__ == "__main__":
    main()