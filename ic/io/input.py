from ic.node import NamedNode


class Input(NamedNode):
    _settings = dict(
        inputs=False,
    )

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}={self.signal.value}>'

    def update_signal(self) -> None:
        pass
