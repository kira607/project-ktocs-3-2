from typing import Iterable

from ic.io import Input
from ic.signal import SignalAcceptor, SignalProducer, Signal

from .transistor_type import TransistorType, TransistorTypeT
from ..signal._base import SignalHolder


class Source(SignalAcceptor):
    def __init__(self, transistor: 'Transistor', *inputs: SignalHolder):
        super().__init__(inputs=inputs)
        self._transistor = transistor

    def update(self, parent: SignalHolder):
        super().update(parent)
        self._transistor.update()


class Drain(SignalProducer):
    def __init__(self, transistor: 'Transistor'):
        self._transistor = transistor
        super().__init__()


class Transistor:
    def __init__(
        self,
        typ: TransistorTypeT,
        number: int,
        canal_width: int = 6,
        canal_length: int = 9999,
        gate: SignalProducer = None,
        sources: Iterable[SignalHolder] = (),
    ) -> None:
        # scheme designation
        self.type = TransistorType.resolve(typ)
        self.number = number

        # physical parameters
        self.canal_length = canal_length
        self.canal_width = canal_width

        # connections
        self.gate = gate  # затвор
        self.drain = Drain(self)  # сток
        self.source = Source(self, *sources)  # исток

    def __repr__(self):
        return (
            f'<{self.__class__.__name__} {self.type}{self.number} '
            f'({self.canal_width}) {{{self.gate if self.gate else ""}}}>'
        )

    def __str__(self):
        inn = f' <- {self.gate}' if isinstance(self.gate, Input) else ''
        return f'T{self.type}{self.number} ({self.canal_width}){inn}'

    def update(self):
        if self.is_open:
            self.drain.set(self.source.signal.value)
        else:
            self.drain.set(-1)

    def add_input(self, to_add: SignalHolder):
        self.source.add_input(to_add)

    @property
    def signal(self) -> Signal:
        return self.drain.signal

    @property
    def is_open(self):
        '''
        Get is transistor open.

        Транзистор открыт каогда
        есть разность потенциалов между
        затвором и истоком.
        '''
        return self.gate.signal - self.source.signal
