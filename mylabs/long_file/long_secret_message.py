#usa mtp testa di ca
import numpy as np
from string import *
f = open("./file.enc", "rb")

freq ={
    "a": 0.0651738, "b": 0.0124248, "c": 0.0217339, "d": 0.0349835, "e": 0.1041442,
    "f": 0.0197881, "g": 0.0158610, "h": 0.0492888, "i": 0.0558094, "j": 0.0009033,
    "k": 0.0050529, "l": 0.0331490, "m": 0.0202124, "n": 0.0564513, "o": 0.0596302,
    "p": 0.0137645, "q": 0.0008606, "r": 0.0497563, "s": 0.0515760, "t": 0.0729357,
    "u": 0.0225134, "v": 0.0082903, "w": 0.0171272, "x": 0.0013692, "y": 0.0145984,
    "z": 0.0007836, " ": 0.1918182
}
lines = []
data = True
while data:
    data = f.read(1000)
    if data:
        lines.append(data.hex())

# print(lines)

chipers = [bytes.fromhex(lines[i]) for i in range(len(lines))]
candidates_list = []
min_len = len(min(chipers, key=len))
# print(min_len)
for byte_to_guess in range(min_len):
    counters = np.zeros(256, dtype=float)
    # print(byte_to_guess)
    for guess in range(256):
        for c in chipers:
            if chr(c[byte_to_guess] ^ guess) in printable:
                # print((c[byte_to_guess] ^ guess))
                counters[guess]+=freq.get(chr(c[byte_to_guess] ^ guess).lower(), 0)

    # print(counters)
    match_list = [(counters[i],i) for i in range(256)]
    # print(match_list)
    ordered_match_list = sorted(match_list, reverse=True)

    candidates = []

    for pair in ordered_match_list:
        if pair[0] < max(counters)*0.95:
            break
        candidates.append(pair)

    candidates_list.append(candidates)
# print(candidates_list)
keystream = b""
for c in candidates_list:
    keystream+=c[0][1].to_bytes(1, byteorder="big")

from Crypto.Util.strxor import strxor

for c in chipers:
    print(strxor(c[:min_len], keystream))