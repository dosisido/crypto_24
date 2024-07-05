from typing import Tuple, Union

EC_POINT = Union[Tuple[int, int], None]
EC_CURVE = Tuple[int, int, int]

def add(P: EC_POINT, Q: EC_POINT, ec: EC_CURVE) -> EC_POINT:
    if P is None:
        return Q
    if Q is None:
        return P
    if P[0] == Q[0] and P[1] == -Q[1]:
        return None
    if P == Q:
        s = (3 * P[0] ** 2 + ec[0]) * pow(2 * P[1], -1, ec[2]) % ec[2]
    else:
        s = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, ec[2]) % ec[2]
    print(s)
    x = (s ** 2 - P[0] - Q[0]) % ec[2]
    y = (s * (P[0] - x) - P[1]) % ec[2]
    return (x, y)

def double(P: EC_POINT, ec: EC_CURVE) -> EC_POINT:
    return add(P, P, ec)
