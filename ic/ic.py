from typing import Iterable, Tuple, Optional

from .binary_util import bits
from .cascade import Cascade
from .io import Input, Output
from .table import Table
from .transistor import Transistor, TransistorTypeT
from .transistor import TransistorChecker


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

    def all_states(self):
        states = []
        for state in bits(len(self._inputs)):
            s = {}
            for i, name in enumerate(self._inputs.keys(), start=0):
                s[name] = state[i]
            states.append(s)
        return states

    def get_table(self):
        table = Table(len(self._inputs) + len(self._outputs) + 2)
        table.set_header(*self._inputs.keys(), *self._outputs.keys(), 'Open transistors', 'Active transistors')
        for state in self.all_states():
            self.change_state(**state)
            row = [input.signal.value for input in self._inputs.values()]
            row.extend([output.signal.value for output in self._outputs.values()])
            row.append(self.transistors(TransistorChecker(is_open="open")))
            row.append(self.transistors(TransistorChecker(is_open="open", is_active="active")))
            table.add_row(*row)
        return table.render()

    def _update(self):
        for o in self._outputs.values():
            o.update_signal()
