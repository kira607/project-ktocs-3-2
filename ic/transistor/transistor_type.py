from enum import Enum
from typing import Union


class TransistorType(Enum):
    P = 'p'
    N = 'n'

    @classmethod
    def resolve(cls, t: Union[str, 'TransistorType']) -> 'TransistorType':
        if isinstance(t, TransistorType):
            return t
        elif isinstance(t, str):
            return TransistorType(t.lower())
        else:
            raise TypeError(type(t))

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: 'TransistorTypeT'):
        other = self.resolve(other)
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


TransistorTypeT = Union[str, TransistorType]
Tp = TransistorType.P
Tn = TransistorType.N
