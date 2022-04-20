def int_to_binary(n: int, fill: int = 0):
    bi = []
    while n:
        n, b = divmod(n, 2)
        bi.insert(0, b)
    unfilled = fill - len(bi)
    if unfilled > 0:
        for _ in range(unfilled):
            bi.insert(0, 0)
    return tuple(bi)
