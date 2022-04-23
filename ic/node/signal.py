from copy import copy


class Signal:
    '''
    The base binary signal.

     1 means high voltage
     0 means low voltage
     -1 means no voltage
    '''

    def __init__(self, value: int = -1):
        self._value = None
        self._locked = False
        self._immutable = self.immutable_copy()
        self.set(value)

    def __repr__(self):
        return f'<{self.__class__.__name__}={self.value}>'

    def __str__(self):
        return repr(self)

    def __sub__(self, other: 'Signal') -> bool:
        '''Разность потенциалов.'''
        if self.value == -1 or other.value == -1:
            return False
        return self.value != other.value

    def __get__(self):
        return self

    @property
    def value(self):
        return self._value

    def is_locked(self) -> bool:
        return self._locked

    def lock(self):
        self._locked = True

    def immutable_copy(self):
        s = copy(self)
        s.lock()
        return s

    def set(self, value: int):
        if self._locked:
            raise RuntimeError('Trying to change locked signal!')
        if value not in (-1, 0, 1):
            raise ValueError(f'{self.__class__.__name__} accepts only -1, 1 or 0. Got: {value}')
        self._value = value
