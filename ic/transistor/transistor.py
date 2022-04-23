from ic.node import Node
from .transistor_type import TransistorType, TransistorTypeT


class Source(Node):

    _settings = dict(
        outputs=False,
    )

    def __init__(self, transistor: 'Transistor', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transistor = transistor

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.transistor}={self.signal}>'


class Drain(Node):

    _settings = dict(
        inputs=False,
    )

    def __init__(self, transistor: 'Transistor', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transistor = transistor

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.transistor}={self.signal}>'

    def update_signal(self) -> None:
        self.transistor.source.update_signal()
        self.transistor.gate.update_signal()
        if self.transistor.is_open:
            self._signal.set(self.transistor.source.signal.value)
        else:
            self._signal.set(-1)


class Gate(Node):

    _settings = dict(
        inputs_limit=1,
        outputs=False,
    )

    def __init__(self, transistor: 'Transistor', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transistor = transistor

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.transistor}={self.signal}>'


class Transistor:
    def __init__(
        self,
        typ: TransistorTypeT,
        number: int,
        canal_width: int = 6,
        canal_length: int = 9999,
        gate: Node = None,
    ) -> None:
        # scheme designation
        self.type = TransistorType.resolve(typ)
        self.number = number

        # physical parameters
        self.canal_length = canal_length
        self.canal_width = canal_width

        # connections
        self.gate = Gate(self)  # затвор
        self.drain = Drain(self)  # сток
        self.source = Source(self)  # исток
        if gate:
            gate.connect_to(self.gate)

    def __str__(self):
        return f'T{self.type}{self.number}'

    def __repr__(self):
        return f'<{str(self)}>'

    def print_info(self):
        inputs = []
        for conn in self.source.inputs.connections:
            inputs.append(f'{conn}')
        print(self, ':')
        print('Source: ', ' '.join(inputs), '->', self.source.signal.value)
        print('Gate: ', f'{self.gate} -> {self.gate.signal.value} -- {"closed" if not self.is_open else "open"}')
        print('Drain: ', self.drain, '->', self.drain.signal.value)

    @property
    def is_open(self):
        '''
        Get is transistor open.

        Транзистор открыт каогда
        есть разность потенциалов между
        затвором и истоком.
        '''
        return self.gate.signal - self.source.signal
