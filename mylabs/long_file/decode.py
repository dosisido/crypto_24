from base64 import b64decode
import numpy
from Crypto.Util.strxor import strxor
from string import *

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))



FILE = 'file.enc'

CHARACTER_FREQ = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
} # ','

ciphertexts = []
with open(FILE, 'rb') as f: ciphertexts = f.readlines()

print("stats: ")
print(f"\tlen ciphertexts: {len(ciphertexts)}")

longest_c = max(ciphertexts, key=len)
max_len = len(longest_c)
print(f"\tlongest: {len(longest_c)}")

shortest_c = min(ciphertexts, key=len)
min_len = len(shortest_c)
print(f"\tshortest: {len(shortest_c)}")


candidates_list = []

for byte_to_guess in range(max_len):
    freqs = numpy.zeros(256, dtype=float)

    for guessed_byte in range(256):
        for c in ciphertexts:
            if byte_to_guess >= len(c):
                continue
            if chr(c[byte_to_guess] ^ guessed_byte) in printable:
                freqs[guessed_byte] += CHARACTER_FREQ.get(chr(c[byte_to_guess] ^ guessed_byte).lower(),0)

    max_matches = max(freqs)
    # print(max_matches)

    match_list = [(freqs[i], i) for i in range(256)]
    # print(match_list)
    ordered_match_list = sorted(match_list, reverse=True)
    # print(ordered_match_list)

    # candidates = []
    # for pair in ordered_match_list:
    #     if pair[0] < max_matches * .95:
    #         break
    #     candidates.append(pair)

    # print(candidates)
    candidates_list.append(ordered_match_list)

# for c in candidates_list:
#     print(c)


keystream = bytearray()
for x in candidates_list:
    keystream += x[0][1].to_bytes(1,byteorder='big')


# keystream[0] = 148

# dec = keystream[1] ^ ciphertexts[0][1]
# dec2 = keystream[2] ^ ciphertexts[0][2]

# mask = dec ^ ord('h')
# keystream[1] = keystream[1] ^ mask
# mask2 = dec2 ^ ord('i')
# keystream[2] = keystream[2] ^ mask2



for c in ciphertexts:
    l = min(len(keystream),len(c))
    print(strxor(c[:l],keystream[:l]).decode())

