

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