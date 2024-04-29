from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from secret import flag
import json, base64

key = get_random_bytes(32)

def get_user_token(name: str) -> str:
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    print('username: ', name)
    token = json.dumps({
        "username": name,
        "admin": False
    })
    print(f"Token json: {token}, len: {len(token)}")
    print(f"Token json encoded: {token.encode()}")
    padded = pad(token.encode(),AES.block_size)
    print(f"Token padded: {padded}, len: {len(padded)}")

    enc_token = cipher.encrypt(padded)
    print("Encrypted token: ", enc_token, len(enc_token))
    
    return f"{base64.b64encode(enc_token).decode()}"


def check_user_token(token):
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    dec_token = unpad(
        cipher.decrypt(
            base64.b64decode(token)
        ),
        AES.block_size
    )

    # dec_token = cipher.decrypt(
    #         base64.b64decode(token)
    #     )

    user = json.loads(dec_token)
    
    if user.get("admin", False) == True:
        return True
    else:
        return False
    

def get_flag():
    token = input("What is your token?\n> ").strip()
    if check_user_token(token):
        print("You are admin!")
        print(f"This is your flag!\n{flag}")
    else:
        print("HEY! WHAT ARE YOU DOING!?")
        exit(1)


if __name__ == "__main__":
    name = input("Hi, please tell me your name!\n> ").strip()
    token = get_user_token(name)
    print("This is your token: " + token)

    menu = \
        "What do you want to do?\n" + \
        "quit - quit the program\n" + \
        "help - show this menu again\n" + \
        "flag - get the flag\n" + \
        "> "
    while True:
        cmd = input(menu).strip()

        if cmd == "quit":
            break
        elif cmd == "help":
            continue
        elif cmd == "flag":
            get_flag()
