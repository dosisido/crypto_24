from typing import Tuple
from Crypto.Util.number import getPrime
from random import randint
from math import gcd


def ord(a: int, p: int) -> int:
    """
    Compute the order of a modulo p.
    """
    if a == 0:
        return 1
    if a == 1:
        return 1
    n = 1
    while pow(a, n, p) != 1:
        n += 1
    return n

def generate_possible_inverse() -> Tuple[int, int]:
    """
    Generate a possible inverse of a number modulo p.
    """
    p = getPrime(7)
    a = randint(1, p)
    while gcd(a, p) != 1:
        a = randint(1, p)
    return a, p

def interactive_inverse():
    while True:
        a, p = generate_possible_inverse()
        print(f"Compute the inverse of {a} modulo {p}")
        inv = int(input("Your answer: "))
        actual_inv = pow(a, -1, p)
        if actual_inv != inv:
            print(f"Wrong answer, the actual inverse is {actual_inv}")
            break