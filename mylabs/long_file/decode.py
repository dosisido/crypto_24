from Crypto.Util.strxor import strxor
from string import printable

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

FILE = 'file.enc'
KEYSTREAM_SIZE = 1000

def xor(a, b):
    return bytes([x ^ y for x,y in zip(a,b)])

CHARACTER_FREQ = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
} # ','

ciphertexts = []
with open(FILE, 'rb') as f: 
    for chunk in iter(lambda: f.read(KEYSTREAM_SIZE), b''): 
        ciphertexts.append(chunk)



key = b''  

for column in range(KEYSTREAM_SIZE):
    print(f"Trying column: {column}", end='\r')
    occurrences = set()
    for char in range(256):
        char = bytes([char])
        # print(f"Trying char: {char.hex()}")
        valids = 0
        for row in ciphertexts:
            c = xor(bytes([row[column]]), char)
            if c in printable.encode(): valids+= CHARACTER_FREQ.get(c.decode().lower(), 0)

        occurrences.add((char, valids))

    occurrences = sorted(occurrences, key=lambda x: x[1], reverse=True)
    # print(occurrences)

    key+=occurrences[0][0]

print("key:", key.hex())

plaintexts = ""
for row in ciphertexts:
    plaintexts+= strxor(row, key[:len(row)]).decode()
with open('plaintext.txt', 'w') as f:
    f.write(plaintexts)
