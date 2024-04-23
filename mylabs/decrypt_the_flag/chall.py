import random
from Crypto.Cipher import ChaCha20
from Crypto.Util.number import long_to_bytes
from secret import flag, randkey

nonce = -1  # unueunused

def xor(a, b):
    return bytes([d ^ o for d,o in zip(a, b)])

def encrypt_and_update(msg, nonce):
    # cirario inizializzato tutte le volte
    cipher = ChaCha20.new(key=randkey, nonce=long_to_bytes(nonce))
    nonce = random.getrandbits(12*8)
    return cipher.encrypt(msg.encode())


def main():
    seed = int(input("Hi, our system doesn't support analogic entropy... so please give a value to initialize me!\n> "))
    random.seed(seed)
    nonce = random.getrandbits(12*8)

    print("OK! I can now give you the encrypted secret!")
    encripted_flag = encrypt_and_update(flag, nonce).hex()
    print(encripted_flag)

    encripted_flag = bytes.fromhex(encripted_flag)

    ms2 = '0' * 128
    enc2 = encrypt_and_update(ms2, nonce).hex()
    enc2 = bytes.fromhex(enc2)



    confirm = input("Do you want to encrypt something else? (y/n)")
    while confirm.lower() != 'n':
        if confirm.lower() == 'y':
            msg = input("What is the message? ")
            print(encrypt_and_update(msg, nonce).hex())
        confirm = input("Do you want to encrypt something else? (y/n)")


if __name__ == '__main__':
    main()