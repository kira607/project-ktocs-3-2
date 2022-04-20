from typing import Iterable, Optional, List, Union, Dict, Tuple

from .signal import SignalAcceptor, AcceptorProducer, NamedAcceptorProducer
from .transistor import Transistor, TransistorTypeT
from .transistor.utils import TransistorChecker, is_transistor


class CascadeOutput(AcceptorProducer):
    def __init__(self, cascade: 'Cascade', transistors: Iterable[int] = (), **kwargs):
        self._cascade = cascade
        transistors = [self._cascade.transistor(t, i) for i in transistors for t in 'pn']
        super().__init__(inputs=(t.drain for t in transistors), **kwargs)


class CascadeInput(NamedAcceptorProducer):
    def __init__(self, cascade: 'Cascade', name: str, transistors_nums: Iterable[int] = (), **kwargs):
        super().__init__(name=name, **kwargs)
        self._cascade = cascade
        self._transistors = [self._cascade.transistor(t, i) for i in transistors_nums for t in 'pn']
        for t in self._transistors:
            t.gate = self

    def update(self):
        self._cascade.update()


class CascadeInputs:
    def __init__(self, cascade: 'Cascade', inputs: Dict[str, Iterable[int]] = None):
        self._cascade = cascade
        inputs = inputs or {}
        self._inputs: Dict[str, CascadeInput] = dict(
            (name, CascadeInput(cascade, name, inputs_nums))
            for name, inputs_nums in inputs.items()
        )

    def __iter__(self):
        return iter(self._inputs.items())

    def __len__(self):
        return len(self._inputs)

    def get(self, name: str) -> CascadeInput:
        return self._inputs[name]


class Cascade:
    def __init__(
        self,
        name: str, 
        inputs: Dict[str, Union[Iterable[int], int]] = None,
        scheme: dict = None,
    ) -> None:
        '''
        :param name: the name of the cascade (I, II, III, IV, etc.).
        :param inputs: map of cascade inputs and transistors
         connected to these inputs (e.g. {'x': [13], 'y': [14, 15]})
        :param scheme: the scheme of the cascade
        '''
        self.name = name
        self._scheme = scheme

        self._inputs = CascadeInputs(self, inputs or {})
        self._output = CascadeOutput(self)

        self._connect_transistors()

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def transistor(self, t: TransistorTypeT, num: int) -> Optional[Transistor]:
        for node in self._scheme:
            if is_transistor(node) and node.type == t and node.number == num:
                return node
        return None

    def transistors(self, checker: TransistorChecker = None) -> List[Transistor]:
        '''
        Get transistors in the cascade.

        :param checker: transistor checker
        '''
        transistors = []
        checker = checker or TransistorChecker()
        for transistor in self._scheme:
            if checker.check(transistor):
                transistors.append(transistor)
        return transistors

    def input(self, name: str) -> CascadeInput:
        return self._inputs.get(name)

    def inputs(self) -> Tuple[CascadeInput]:
        ins = tuple(inp for __name, inp in self._inputs)
        return ins

    def connect_to(self, *out: SignalAcceptor):
        for o in out:
            o.add_input(self._output)

    def is_autonomous(self):
        return len(self._inputs) == 0

    def update(self):
        for transistor, outputs in self._scheme.items():
            return
            if not is_transistor(transistor):
                continue
            transistor.update()

    def out_capacity(self):
        '''сумма ширин каналов тразисторов, подключенных к выходу каскада.'''

    def _connect_transistors(self):
        for ts, transistors in self._scheme.items():
            if not transistors:
                if not is_transistor(ts):
                    raise RuntimeError(f'Constant source signal {ts} must be connected to transistor(s).')
                self._output.add_input(ts.drain)
                continue
            for t in transistors:
                producer = ts if not is_transistor(ts) else ts.drain
                t.source.add_input(producer)
