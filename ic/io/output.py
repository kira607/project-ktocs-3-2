from ic.signal import NamedSignalAcceptor
from .input import Input


class Output(NamedSignalAcceptor):
    def __init__(self, name: str, connected: Input = None):
        self._connected = connected
        super().__init__(name)
