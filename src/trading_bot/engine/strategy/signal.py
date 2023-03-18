#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADE MODEL

import logging
import datetime
import pysnooper

from dataclasses import dataclass

from src.backpack.bp_fetchers import fetch_timestamp
from src.backpack.bp_general import (
    stdout_msg, pretty_dict_print
)
from src.ar_exceptions import (
    ARInvalidStateException,
    ARPreconditionsException,
)

log = logging.getLogger('AsymetricRisk')


@dataclass
class Signal():
    '''
    [ NOTE ]: Trading signal generated by the strategy evaluator.
    '''

#   @pysnooper.snoop()
    def __init__(self, **context) -> None:
        log.debug('')
        self._context = context
        self.create_date = datetime.datetime.now()
        self.write_date = self.create_date
        self.ticker_symbol = str(context.get('ticker-symbol')).replace('/', '')
        self.side = str()
        self.risk = int()
        self.source_strategy = dict()

    # MAGIK

    def __str__(self):
        return f'Trade Signal: {self}'

    # TODO
    def __add__(self, other):
        pass
    def __sub__(self, other):
        pass
    def __mul__(self, other):
        pass
    def __truediv__(self, other):
        pass
    def __floordiv__(self, other):
        pass
    def __mod__(self, other):
        pass
    def __pow__(self, other):
        pass
    def __lt__(self, other):
        pass
    def __gt__(self, other):
        pass
    def __le__(self, other):
        pass
    def __ge__(self, other):
        pass
    def __eq__(self, other):
        pass

