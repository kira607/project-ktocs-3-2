from ic.node import NamedNode


class ConstantSignal(NamedNode):
    _settings = dict(
        inputs=False,
        signal='constant',
    )

    def __repr__(self):
        return f'<{self.name}>'

    def update_signal(self) -> None:
        pass


E = ConstantSignal('E', 1)
G = ConstantSignal('G', 0)
