from typing import Tuple, Dict, Any, Iterable

from .signal import Signal


class _Missing(object):
    pass


class ConnectionsContainer:
    '''
    A container that holds connections to other node.

    :param connections: A list of connections
    :param limit: The maximum number of connections
    '''

    def __init__(self, *connections: 'Node', limit: int = None):
        self._connections = set()
        self._limit = abs(int(limit)) if limit else None
        for conn in connections:
            self.add(conn)

    def __len__(self):
        '''Get number of connections.'''
        return len(self._connections)

    def __iter__(self):
        '''Iterate through all connections.'''
        return iter(self._connections)

    def __bool__(self):
        return bool(self._connections)

    def __repr__(self):
        return f'<{self.__class__.__name__} ({len(self)})>'

    def __str__(self):
        return repr(self)

    @property
    def connections(self):
        '''Get connections as tuple.'''
        return tuple(self._connections)

    def add(self, to_add: 'Node') -> None:
        '''
        Add connection.

        ``to_add`` **MUST** be a :class:`ic.node.node.Node` instance

        :param to_add: connection to add
        :raises TypeError: if ``to_add`` is not a :class:`ic.node.node.Node` instance
        :raises RuntimeError: if connections container exceeded its limit
        '''
        if not isinstance(to_add, Node):
            raise TypeError(f'to_add must be a Node instance. Got: {type(to_add)}')
        if self._limit:
            if len(self) == self._limit:
                raise RuntimeError(f'Connections container exceeded its limit ({self._limit})')
        self._connections.add(to_add)

    def check(self) -> None:
        '''Check of connections is connected to anything.'''
        if not self._connections:
            raise RuntimeError('Not connected!')


def connect(a: 'Node', b: 'Node'):
    a.outputs.add(b)
    b.inputs.add(a)


class Node:
    '''
    A circuit module connected to other modules
    that has a signal.
    '''

    _default_settings = dict(
        inputs=True,
        inputs_limit=None,
        outputs=True,
        outputs_limit=None,
        signal='updatable',
    )

    _settings = _default_settings

    def __init__(self, sig_val: int = -1, inputs: Iterable['Node'] = (), outputs: Iterable['Node'] = ()):
        self._load_settings(sig_val)

        self._signal = Signal(sig_val)

        if self._settings['signal'] == 'constant':
            self.signal.lock()
        elif self._settings['signal'] != 'updatable':
            raise ValueError('signal setting must be either "constant" or "updatable"')

        if self._settings['inputs']:
            self.inputs = ConnectionsContainer(*inputs, limit=self._settings['inputs_limit'])
        elif inputs:
            raise ValueError('inputs setting is turned off')
        else:
            self.inputs = None

        if self._settings['outputs']:
            self.outputs = ConnectionsContainer(*inputs, limit=self._settings['outputs_limit'])
        elif outputs:
            raise ValueError('outputs setting is turned off')
        else:
            self.outputs = None

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.inputs}:{self.outputs}>'

    def connect_to(self, other: 'Node'):
        connect(self, other)

    @property
    def signal(self):
        return self._signal

    def update_signal(self) -> None:
        self.inputs.check()
        sig_val = -1
        for node in self.inputs:
            node.update_signal()
            if node.signal.value > sig_val:
                sig_val = node.signal.value
        self._signal.set(sig_val)

    def _load_settings(self, sig_val: int):
        for setting, value in self._default_settings.items():
            sett = self._settings.get(setting, _Missing)
            if sett == _Missing:
                self._settings[setting] = value
        self._validate_settings(sig_val)

    def _validate_settings(self, sig_val: int):
        if (
            (self._settings['inputs'] is False and self._settings['outputs'] is False)
            or (self._settings['inputs_limit'] == 0 and self._settings['outputs_limit'] == 0)
        ):
            raise RuntimeError('Node must be connected to something')
        if sig_val == -1 and self._settings['signal'] == 'constant':
            raise RuntimeError('Constant signal must have a boolean value (0 or 1), not -1')


class NamedNode(Node):
    '''A node with name.'''
    def __init__(
        self,
        name: str,
        sig_val: int = -1,
        inputs: Iterable['Node'] = (),
        outputs: Iterable['Node'] = (),
    ) -> None:
        self._name = name.upper()
        super().__init__(sig_val, inputs, outputs)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self._name} {self.inputs}:{self.outputs}>'

    @property
    def name(self) -> str:
        return self._name
