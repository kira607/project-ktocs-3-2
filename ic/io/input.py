from ic.signal import NamedSignalProducer


class Input(NamedSignalProducer):
    def __init__(self, name: str, value: int = 0):
        super().__init__(name=name, sig_val=value)
