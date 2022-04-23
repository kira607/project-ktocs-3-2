from typing import Iterable, Tuple, Optional

from .binary_util import bits
from .cascade import Cascade
from .io import Input, Output
from .transistor import Transistor, TransistorTypeT
from .transistor.utils import TransistorChecker


class IC:
    '''Integrated Circuit.'''
    def __init__(
        self, 
        name: str, 
        inputs: Iterable[Input],
        outputs: Iterable[Output],
        cascades: Iterable[Cascade],
    ) -> None:
        self.name = name
        self._inputs = dict(((i.name, i) for i in inputs))
        self._outputs = dict(((o.name, o) for o in outputs))
        self._cascades = dict(((c.name, c) for c in cascades))
        self.change_state()
        self._update()

    def inputs(self) -> Tuple[Input]:
        return tuple(self._inputs.values())

    def input(self, name: str) -> Optional[Input]:
        return self._inputs.get(name)

    def outputs(self) -> Tuple[Output]:
        return tuple(self._outputs.values())

    def output(self, name: str) -> Optional[Output]:
        return self._outputs.get(name)

    def cascades(self) -> Tuple[Cascade]:
        return tuple(self._cascades.values())

    def cascade(self, name: str) -> Optional[Cascade]:
        return self._cascades.get(name)

    def transistors(self, checker: TransistorChecker = None) -> Tuple[Transistor]:
        transistors = []
        for cascade in self.cascades():
            transistors.extend(cascade.transistors(checker))
        return tuple(transistors)

    def transistor(self, t: TransistorTypeT, num: int) -> Optional[Transistor]:
        for cascade in self._cascades.values():
            transistor = cascade.transistor(t, num)
            if transistor:
                return transistor
        return None

    def change_state(self, **kwargs) -> None:
        if not kwargs:
            kwargs = dict((input_name, 0) for input_name in self._inputs)
        inputs_names = tuple(self._inputs.keys())
        for input_name, input_signal in kwargs.items():
            input_ = self.input(input_name)
            if not input_:
                raise ValueError(f'Wrong input name: "{input_name}". Expected on of: {inputs_names}')
            input_.signal.set(input_signal)
        self._update()

    def get_table(self):
        table = '  '.join(self._inputs.keys()) + '  '
        table += '  '.join(self._outputs.keys())
        table += '\n'
        states = bits(len(self._inputs))
        for state in states:
            s = {}
            for i, name in enumerate(self._inputs.keys(), start=0):
                s[name] = state[i]
            self.change_state(**s)
            table += '  '.join(str(input.signal.value) for input in self._inputs.values()) + '  '
            table += '  '.join(str(output.signal.value) for output in self._outputs.values())
            table += '\n'
        return table

    def _update(self):
        for o in self._outputs.values():
            o.update_signal()
