import logging
import time
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Optional


class Timer:
    '''Timer for logging time certain process takes.'''

    def __init__(self, log_message: str, logging_level: int = logging.INFO, start_message: bool = True) -> None:
        '''
        init.

        :param log_message: message to log before logging the time.
        :param logging_level: level of logging.
        '''
        self._log_message = log_message
        self._logging_level = logging_level
        self._start_message = start_message
        self._logging_mark = '[Timer-G20xGd]'
        self._start = None
        self._stop = None
        self._logger = logging.getLogger(__name__)

    def start(self):
        '''
        Start timer.

        Logs start point.
        '''
        self._start = time.time()
        if self._start_message:
            self.log(f'{self._logging_mark} Started: {self._log_message}')
        return self

    def stop(self, additional_log: Optional[str] = None) -> float:
        '''
        Stop timer.

        Logs end point and process time.

        :param str additional_log: the additional info to log after stopping the timer.
        :return: time process took in seconds
        :rtype: float
        '''
        self._stop = time.time()
        process_time = round(self._stop - self._start, 4)
        message = f'{self._logging_mark} Ended: {self._log_message}. '
        if additional_log:
            message += f'({additional_log}) '
        message += f'(process took: {process_time} sec)'
        self.log(message)
        return process_time

    def log(self, message: str):
        '''Log a message.'''
        self._logger.log(self._logging_level, message)

    def __call__(self, f: Callable) -> Callable:
        '''
        Use timer as a decorator.

        It is required to define a log message::

            @Timer('log message')
            def f():
                pass  # some code
        '''

        @wraps(f)
        def wrapper(*args, **kwargs):
            self.start()
            return_value = f(*args, **kwargs)
            self.stop()
            return return_value

        return wrapper

    @classmethod
    @contextmanager
    def context(cls, message):
        t = cls(message)
        try:
            pass
        finally:
            t.stop()
