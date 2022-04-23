from typing import Iterable, Optional, List, Union, Dict, Tuple

from .node import Node, NamedNode
from .io import E, G
from .transistor import Transistor, TransistorTypeT
from .transistor.utils import TransistorChecker, is_transistor


class CascadeOutput(Node):
    def __init__(self, cascade: 'Cascade', transistors_nums: Iterable[int] = (), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cascade = cascade
        transistors = [self._cascade.transistor(t, i) for i in transistors_nums for t in 'pn']
        for t in transistors:
            t.drain.connect_to(self)

    def __repr__(self):
        return f'<{self._cascade} output={self.signal.value}>'

    def update_signal(self):
        super().update_signal()


class CascadeInput(NamedNode):
    def __init__(self, cascade: 'Cascade', name: str, transistors_nums: Iterable[int] = (), *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._cascade = cascade
        transistors = [self._cascade.transistor(t, i) for i in transistors_nums for t in 'pn']
        for t in transistors:
            self.connect_to(t.gate)

    def __repr__(self):
        return f'<{self._cascade} input {self.name}>'


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

        self.inputs = CascadeInputs(self, inputs or {})
        self.output = CascadeOutput(self)

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
        return self.inputs.get(name)

    def inputs(self) -> Tuple[CascadeInput]:
        ins = tuple(inp for __name, inp in self.inputs)
        return ins

    def connect_to(self, *out: Node):
        for o in out:
            self.output.connect_to(o)

    def is_autonomous(self):
        return len(self.inputs) == 0

    def out_capacity(self):
        '''сумма ширин каналов тразисторов, подключенных к выходу каскада.'''
        pass

    def _connect_transistors(self):
        self._validate_scheme()

        for daddy, transistors in self._scheme.items():
            if not transistors:
                daddy.drain.connect_to(self.output)
                continue
            for boy in transistors:
                daddy.drain.connect_to(boy.source)

        for daddy in self._scheme.keys():
            if daddy.source.inputs:
                continue
            src = G if daddy.type == 'n' else E
            src.connect_to(daddy.source)

    def _validate_scheme(self):
        for k, v in self._scheme.items():
            if not is_transistor(k):
                raise ValueError(f'{k} is not transistor!')
            if not v:
                continue
            for i in v:
                if not is_transistor(k):
                    raise ValueError(f'{i} is not transistor!')

