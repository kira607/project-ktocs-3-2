from ..transistor import Transistor


def pn_transistors(num: int, gate=None):
    return Transistor('p', num, gate=gate), Transistor('n', num, gate=gate)
