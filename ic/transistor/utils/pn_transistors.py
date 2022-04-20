from ..transistor import Transistor


def pn_transistors(num: int):
    return Transistor('p', num), Transistor('n', num)
