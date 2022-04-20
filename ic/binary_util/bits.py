from .binary_to_int import binary_to_int
from .int_to_binary import int_to_binary


def bits(n):
    m = binary_to_int(tuple(1 for _ in range(n))) + 1
    result = []
    for x in range(m):
        result.append(int_to_binary(x, fill=n))
    return result
