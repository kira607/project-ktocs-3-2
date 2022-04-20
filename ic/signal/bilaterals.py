from typing import Iterable

from ._base import SignalHolder, Inputs, Outputs, NamedMixin
from .producers import SignalProducer
from .acceptors import SignalAcceptor


class AcceptorProducer(SignalHolder, Outputs, Inputs):
    '''A circuit module accepting signal from its inputs and producing this signal to its outputs.'''
    def __init__(
        self,
        inputs: Iterable[SignalProducer] = (),
        outputs: Iterable[SignalAcceptor] = (),
        **kwargs,
    ) -> None:
        super().__init__(inputs=inputs, outputs=outputs, **kwargs)
        self.add_inputs(inputs)
        self.add_outputs(outputs)

    def update(self):
        for o in self.outputs:
            o.update(self)

    def _update_signal(self):
        return max(t.signal.value for t in self._inputs).signal.value


class NamedAcceptorProducer(AcceptorProducer, NamedMixin):
    def __init__(
        self,
        name: str,
        inputs: Iterable[SignalProducer] = (),
        outputs: Iterable[SignalAcceptor] = (),
        **kwargs,
    ) -> None:
        super(NamedAcceptorProducer, self).__init__(name=name, inputs=inputs, outputs=outputs, **kwargs)
