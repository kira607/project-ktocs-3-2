from typing import Iterable

from .signal import Signal


class NamedMixin:
    '''Named module.'''

    def __init__(self, name: str, **kwargs):
        self._set_name(name)

    @property
    def name(self):
        return self._name

    def _set_name(self, name: str):
        if not name:
            raise ValueError(name)
        self._name = name.upper()


class SignalHolder:
    '''A circuit module that has a signal.'''

    def __init__(self):
        self._signal = Signal(-1)

    def __repr__(self):
        return f'<{str(self)}>'

    def __str__(self):
        return f'{self.__class__.__name__} signal={self._signal}'

    @property
    def signal(self):
        self._signal.set(self._update_signal())
        return self._signal

    def _update_signal(self) -> int:
        return self._signal.value


class Inputs:
    '''A circuit module with inputs.'''

    def __init__(self, inputs: Iterable[SignalHolder] = ()):
        self._inputs = set()
        self.add_inputs(inputs)

    def __len__(self):
        return len(self._inputs)

    @property
    def inputs(self):
        return tuple(self.inputs)

    def add_inputs(self, inputs: Iterable[SignalHolder]) -> None:
        for i in inputs:
            self.add_input(i)

    def add_input(self, to_add: SignalHolder) -> None:
        if not isinstance(to_add, SignalHolder):
            raise RuntimeError(f'to_add must be a HasSignal instance. Got: {type(to_add)}')
        self._inputs.add(to_add)

    def _check_inputs(self):
        if not self._inputs:
            raise RuntimeError(f'{self.__class__.__name__}: Not connected!')


class Outputs:
    '''A circuit module with outputs.'''

    def __init__(self, outputs: Iterable[Inputs] = (), **kwargs):
        self._outputs = set()
        self.add_outputs(outputs)

    def __len__(self) -> int:
        return len(self._outputs)

    @property
    def outputs(self):
        return tuple(self._outputs)

    def add_outputs(self, outputs: Iterable[Inputs]):
        for o in outputs:
            self.add_output(o)

    def add_output(self, to_add: Inputs) -> None:
        if not isinstance(to_add, Inputs):
            raise RuntimeError(f'to_add must be a SignalAcceptor instance. Got: {type(to_add)}')
        self._outputs.add(to_add)

    def _check_outputs(self):
        if not self._outputs:
            raise RuntimeError(f'{self.__class__.__name__}: Not connected!')
