from typing import Tuple
from Crypto.Util.number import getPrime
from random import randint
from math import gcd
from gmpy2 import next_prime, isqrt



def fermat(n):
    a = isqrt(n)
    b = a
    b2 = pow(a,2) - n

    while True:
        if b2 == pow(b,2): break
        else:
            a+= 1
            b2= pow(a, 2) - n
            b = isqrt(b2)

    p = a+b
    q = a-b

    factor_list = [int(p), int(q)]
    factor_list.sort()
    return tuple(factor_list)

def ord(a: int, p: int) -> int:
    """
    Compute the order of a modulo p.
    """
    if a == 0: return 1
    if a == 1: return 1
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

def isomorphism(iso, coeff):
    l = []
    for i in range(iso[0]):
        for j in range(iso[1]):
            l.append((coeff[0] * i + coeff[1] * j) % (iso[0]*iso[1]))
    l.sort()
    return l

def quad_residue(a, P):
    p_el = fermat(P)
    none = 0
    for p in p_el:
        if pow(a, (p-1)//2, p) != 1:
            none+=1
    if none != 0:
        print(f"Found {none} non-quadratic residues from the primes")

    l = []
    for i in range(P):
        if pow(i, 2, P) == a:
            l.append(i)
    return l