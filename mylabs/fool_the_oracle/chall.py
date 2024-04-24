from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from secret import flag

assert(len(flag) == len("CRYPTO23{}") + 36) # len = 46

key = get_random_bytes(24)
flag = flag.encode()

def encrypt(data = None) -> bytes:
    # init
    cipher = AES.new(key=key, mode=AES.MODE_ECB)

    # string
    if data is None:
        data  = bytes.fromhex(input("> "))
    else:
        data = bytes.fromhex(data)
    payload = data + flag

    if True:
        print('recieved:',)
        for i in range(len(payload) // AES.block_size * 2):
            print(payload.hex()[i * 32:(i + 1) * 32])

    # encrypt
    hex_string = cipher.encrypt(pad(payload, AES.block_size)).hex()
    
    # print(hex_string)
    return hex_string


def main():
    menu = \
    "What do you want to do?\n" + \
    "quit - quit the program\n" + \
    "enc - encrypt something\n" + \
    "help - show this menu again\n" + \
    "> "
    
    while True:
        cmd = input(menu).strip()

        if cmd == "quit":
            break
        elif cmd == "help":
            continue
        elif cmd == "enc":
            encrypt()


if __name__ == '__main__':
    main()

