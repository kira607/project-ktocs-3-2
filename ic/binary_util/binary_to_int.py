def binary_to_int(b: tuple):
    result = 0
    for n, bit in enumerate(b, start=0):
        multiplier = 2 ** n
        result += bit * multiplier
    return result
