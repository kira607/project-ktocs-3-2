class Signal:
    '''
    The base binary signal.

     1 means high voltage
     0 means low voltage
     -1 means no voltage
    '''

    def __init__(self, value: int = -1):
        self._value = None
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

    @property
    def value(self):
        return self._value

    def set(self, value: int):
        if value not in (-1, 0, 1):
            raise ValueError(f'{self.__class__.__name__} accepts only -1, 1 or 0')
        self._value = value
