from ic.io import Input
from ic.node import NamedNode


class Output(NamedNode):
    _settings = dict(
        outputs=False,
    )

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}={self.signal.value}>'

    def __init__(self, name: str, connected: Input, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._connected = connected
