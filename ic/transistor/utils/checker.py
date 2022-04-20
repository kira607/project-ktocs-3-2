from ..transistor import Transistor
from .is_transistor import is_transistor


class TransistorChecker:
    def __init__(
        self,
        t: str = 'any',
        is_open: str = 'any',
        is_active: str = 'any',
    ) -> None:
        if is_open.lower() not in ('any', 'open', 'closed'):
            raise ValueError(is_open)
        if t.lower() not in ('any', 'p', 'n'):
            raise ValueError(t)
        if is_active.lower() not in ('any', 'active', 'not active'):
            raise ValueError(is_active)
        self._t = t
        self._is_open = is_open
        self._is_active = is_active

    def check(self, transistor: Transistor) -> bool:
        if not is_transistor(transistor):
            return False
        return (
            self._check_is_open(transistor)
            and self._check_type(transistor)
            # and self._check_active(transistor)
        )

    def _check_is_open(self, transistor):
        if self._is_open == 'any':
            return True
        elif self._is_open == 'open':
            return transistor.is_open
        elif self._is_open == 'closed':
            return not transistor.is_open

    def _check_type(self, transistor):
        if self._t == 'any':
            return True
        return transistor.type == self._t

    def _check_active(self, transistor):
        if self._is_active == 'any':
            return True
        elif self._is_active == 'active':
            pass
        elif self._is_active == 'not active':
            pass
