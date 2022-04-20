from typing import Iterable

from ._base import NamedMixin, SignalHolder, Inputs, Outputs


class SignalProducer(Outputs, SignalHolder):
    '''
    A circuit module autonomously producing signal to its outputs.

    The signal can be changed.
    '''

    def __init__(self, sig_val: int = -1, outputs: Iterable[Inputs] = (), **kwargs):
        super(SignalProducer, self).__init__(sig_val=sig_val, outputs=outputs, **kwargs)

    def set(self, sig_val: int) -> None:
        self._signal.set(sig_val)

    def update(self):
        for output in self._outputs:
            output.update(self)


class ConstantSignalProducer(SignalProducer):
    '''
    A circuit module autonomously producing signal to its outputs.

    The signal can not be changed.
    '''

    def __init__(self, sig_val: int = -1, outputs: Iterable[Inputs] = (), **kwargs):
        self._locked = False
        super(ConstantSignalProducer, self).__init__(sig_val=sig_val, outputs=outputs, **kwargs)
        self._locked = True

    def set(self, sig_val: int):
        if self._locked:
            raise RuntimeError(f'Cannot change signal value of {self.__class__.__name__}')
        super(ConstantSignalProducer, self).set(sig_val)


class NamedSignalProducer(SignalProducer, NamedMixin):
    '''A SignalProducer with name.'''

    def __init__(self, name: str, sig_val: int = -1, outputs: Iterable[Inputs] = (), **kwargs):
        super().__init__(name=name, sig_val=sig_val, outputs=outputs, **kwargs)


class NamedConstantSignalProducer(ConstantSignalProducer, NamedMixin):
    '''A ConstantSignalProducer with name.'''

    def __init__(self, name: str, sig_val: int = -1, outputs: Iterable[Inputs] = (), **kwargs):
        super().__init__(name=name, sig_val=sig_val, outputs=outputs, **kwargs)
