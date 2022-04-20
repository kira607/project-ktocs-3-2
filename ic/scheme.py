from typing import Iterable

from ic.transistor import is_transistor


class SchemeNode:
    def __init__(self, *connections):
        self.connections = list(connections)

    def add(self, connection):
        self.connections.append(connection)


class Scheme:
    def __init__(self, scheme: dict, inputs: Iterable[int], outputs: Iterable[int]) -> None:
        self._scheme = scheme
        self._input = SchemeNode()
        self._output = SchemeNode()
        self._connect()

    def _connect(self) -> None:
        for type, scheme in self._scheme.items():
            for source, transistors in scheme.items():
                if not transistors:
                    if not is_transistor(source):
                        raise RuntimeError(f'Constant source signal {source} must be connected to transistor(s).')
                    self._output.add(source)
                    continue
                for t in transistors:
                    if type == 'p':
                        t.source = source
                    if type == 'n':
                        t.drain = source

    def __iter__(self):
        return iter(self._scheme.items())


'''
scheme={
    E: [p14],
    p14: None,
    G: [n14],
    n14: None,
}

scheme={
    Tp: {
        E: [p6, p10],
        p6: [p7, p8, p9],
        p7: None,
        p8: None,
        p9: None,
        p10: [p11],
        p11: [p12],
        p12: None,
    }
    Tn: {
        G: [n7, n8, n9, n12],
        n6: None,
        n7: [n6],
        n8: [n6],
        n9: [n6],
        n10: None,
        n11: [n10],
        n12: [n11],
    }
}
'''
