import logging

from ic import IC, Cascade
from ic.io import Input, Output
from ic.table import Table
from ic.transistor import Transistor

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

X = Input('X')
Y = Input('Y')
C = Input('C')

S = Output('S', Y)
P = Output('P', C)

p1 = Transistor('p', 1, 6, gate=X)
p2 = Transistor('p', 2, 6, gate=C)
p3 = Transistor('p', 3, 6, gate=Y)
p4 = Transistor('p', 4, 6, gate=X)
p5 = Transistor('p', 5, 6, gate=C)
p6 = Transistor('p', 6, 6)
p7 = Transistor('p', 7, 6, gate=X)
p8 = Transistor('p', 8, 6, gate=Y)
p9 = Transistor('p', 9, 6, gate=C)
p10 = Transistor('p', 10, 6, gate=X)
p11 = Transistor('p', 11, 6, gate=Y)
p12 = Transistor('p', 12, 6, gate=C)
p13 = Transistor('p', 13, 6)
p14 = Transistor('p', 14, 6)
n1 = Transistor('n', 1, 6, gate=X)
n2 = Transistor('n', 2, 6, gate=C)
n3 = Transistor('n', 3, 6, gate=Y)
n4 = Transistor('n', 4, 6, gate=X)
n5 = Transistor('n', 5, 6, gate=C)
n6 = Transistor('n', 6, 6)
n7 = Transistor('n', 7, 6, gate=X)
n8 = Transistor('n', 8, 6, gate=Y)
n9 = Transistor('n', 9, 6, gate=C)
n10 = Transistor('n', 10, 6, gate=X)
n11 = Transistor('n', 11, 6, gate=Y)
n12 = Transistor('n', 12, 6, gate=C)
n13 = Transistor('n', 13, 6)
n14 = Transistor('n', 14, 6)


Cascade_I = Cascade('I', scheme={
    p1: [p3],
    p2: [p3],
    p3: None,
    p4: [p5],
    p5: None,
    n1: None,
    n2: None,
    n3: [n1, n2],
    n4: None,
    n5: [n4],
})

Cascade_II = Cascade('II', inputs={'x': [6]}, scheme={
    p6: [p7, p8, p9],
    p7: None,
    p8: None,
    p9: None,
    p10: [p11],
    p11: [p12],
    p12: None,
    n6: None,
    n7: [n6],
    n8: [n6],
    n9: [n6],
    n10: None,
    n11: [n10],
    n12: [n11],
})

Cascade_III = Cascade('III', inputs={'x': [13]}, scheme={
    p13: None,
    n13: None,
})

Cascade_IV = Cascade('IV', inputs={'x': [14]}, scheme={
    p14: None,
    n14: None,
})

Cascade_I.connect_to(Cascade_II.input('x'), Cascade_IV.input('x'))
Cascade_II.connect_to(Cascade_III.input('x'))
Cascade_III.connect_to(S)
Cascade_IV.connect_to(P)

ic = IC(
    'IC',
    inputs=(X, Y, C),
    outputs=(S, P),
    cascades=(Cascade_I, Cascade_II, Cascade_III, Cascade_IV),
)


def main():
    print(ic.get_table())
    table = Table(2)
    table.set_header('Cascade', 'out capacity')
    for cas in ic.cascades():
        table.add_row(str(cas), cas.out_capacity())
    print(table.render())


if __name__ == '__main__':
    main()
