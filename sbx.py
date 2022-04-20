from ic.io import Input, Output
from ic.signal import E, G
from ic.transistor import Transistor


def main():
    x = Input('X')
    y = Output('Y')
    n1 = Transistor('n', 1, gate=x)
    p1 = Transistor('p', 1, gate=x)
    p1.source.add_input(E)
    n1.source.add_input(G)
    p1.drain.add_output(y)
    n1.drain.add_output(y)
    return


if __name__ == '__main__':
    main()
