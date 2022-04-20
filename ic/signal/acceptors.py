from typing import Iterable

from ._base import SignalHolder, Inputs, NamedMixin


class SignalAcceptor:
    '''A circuit module accepting signal from its inputs.'''

    _signal = SignalHolder()
    _inputs = Inputs()

    def __init__(self, inputs: Iterable[SignalHolder] = (), **kwargs):
        self._inputs.add_inputs(inputs)

    def update(self, parent: SignalHolder):
        sig_val = parent.signal.value
        if sig_val > self._signal.value:
            self._signal.set(sig_val)


class NamedSignalAcceptor(SignalAcceptor, NamedMixin):
    def __init__(self, name: str, inputs: Iterable[SignalHolder] = (), **kwargs):
        super().__init__(name=name, inputs=inputs, **kwargs)
