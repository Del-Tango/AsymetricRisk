#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# TRADE

import random
import datetime
import logging
import pysnooper

from src.backpack.bp_general import stdout_msg, pretty_dict_print
from src.backpack.bp_generators import generate_msg_id

log = logging.getLogger('AsymetricRisk')


class Trade():

    def __init__(self, *args, **kwargs):
        self.create_date = datetime.datetime.now()
        self.write_date = self.create_date
        self.expired_at = None
        self.executed_at = None
        self.expired = False
        self.executed = False
        self.result = {}
        self.risk = 0
        self.ticker_symbol = kwargs.get('ticker-symbol', str())
        self.base_currency = kwargs.get('base-currency', str())
        self.quote_currency = kwargs.get('quote-currency', str())
        self.price = kwargs.get('price', float())
        self.amount = kwargs.get('order-amount', float())
        self.base_amount = kwargs.get('base-amount', float())
        self.quote_amount = kwargs.get('quote-amount', float())
        self.stop_loss = kwargs.get('stop-loss', float())
        self.take_profit = kwargs.get('take-profit', float())
        self.trailing_stop = kwargs.get('trailing-stop', float())
        self.strategy = kwargs.get('strategy', str())
        self.side = kwargs.get('side', str())
        self.time_in_force = kwargs.get('order-time-in-force', int())
        self.response_type = kwargs.get('order-response-type', str())
        self.recv_window = kwargs.get('order-recv-window', int())
        self.trade_timeout = kwargs.get('trade-timeout', int())
        self.order_id = kwargs.get(
            'order-id', generate_msg_id(random.randint(20))
        )

    def __str__(self):
        return 'Trade {}'.format(self.order_id)

    def update(self, trade_response, **kwargs):
        log.debug('TODO - Under construction, building...')
        self.result.update(trade_response)
        return self.result

    def details(self, *args):
        '''
        [ INPUT ]: *args = ('all' | 'ticker_symbol', 'base_currency', ...)

        [ RETURN ]: {
            'ticker_symbol': 'BTC/USDT',
            'base_currency': 'BTC',
            ...
        }
        '''
        log.debug('')
        if not args or 'all' in args:
            details = self.__dict__.copy()
        else:
            details = {
                field_name: self.__dict__.get(field_name) for field_name in args
            }
        log.debug(
            'Trade {}: {}'.format(self.order_id, pretty_dict_print(details))
        )
        return details

    def expire(self):
        log.debug('')
        if self.expired:
            log.debug(
                'Trade ({}) already expired at ({})'.format(
                    self.order_id, self.expired_at
                )
            )
            return False
        self.expired_at = datetime.datetime.now()
        self.write_date = self.expired_at
        self.expired = True
        return self.expired

    def execute(self):
        log.debug('')
        self.executed_at = datetime.datetime.now()
        self.write_date = self.executed_at
        self.executed = True
        return self.executed

    def is_expired(self):
        log.debug('')
        return self.expired

    def is_executed(self):
        log.debug('')
        return self.executed


