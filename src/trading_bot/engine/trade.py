#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADE MODEL

import logging
import time
import datetime
import random
import string
import pysnooper

from src.backpack.bp_fetchers import fetch_timestamp
from src.backpack.bp_generators import generate_msg_id
from src.backpack.bp_general import (
    stdout_msg, pretty_dict_print
)
from src.ar_exceptions import (
    ARInvalidStateException,
    ARPreconditionsException,
)

log = logging.getLogger('AsymetricRisk')


class Trade():
    '''
    [ NOTE ]: Responsibilities:

        * Defines Trade data model.
        * Records state, context and metadata of trade.
        * Keeps action history records.
        * Keeps record of signals that generated trade,
        * Enforces state transition rules.
        * Locally generates default Trade ID.

    [ NOTE ]: State order:
        DRAFT -> EVALUATED -> COMMITED -> DONE
                                       -> DISCARDED
                                       -> EXPIRED

    [ NOTE ]: Each time the Trade status changes, a history record with all the
        the action data is cached, with a default history limit of 20 records.

    [ NOTE ]: Multiple buy/sell signals can be grouped in order to generate the
        Trade() instance. If the Trade already exists and is not yet commited,
        new signals of the same side will also be associated with this instance.
    '''

    STATUS_DRAFT = 'DRAFT'
    STATUS_EVALUATED = 'EVALUATED'
    STATUS_COMMITED = 'COMMITED'
    STATUS_DONE = 'DONE'
    STATUS_DISCARDED = 'DISCARDED'
    STATUS_EXPIRED = 'EXPIRED'
    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'
    STOP_ORDER_TIME_IN_FORCE = 'GTC'

#   @pysnooper.snoop()
    def __init__(self, **context) -> None:
        log.debug('')
        self._signals = list()
        self._context = context
        self._history = {} # <timestamp>: {action: '', context: {}, result: {}, failed=False}
        self.create_date = datetime.datetime.now()
        self.write_date = self.create_date
        self.trade_id = context.get('trade-id', generate_msg_id(
            random.randint(4, 12), id_characters=list(string.digits)
        ))
        self.ticker_symbol = context.get('ticker-symbol', str())
        self.status = self.STATUS_DRAFT
        self.previous_status = None
        self.risk = int()
        self.base_quantity = float()
        self.quote_quantity = float()
        self.side = str()
        self.current_price = float()
        self.stop_loss_price = float()
        self.take_profit_price = float()
        self.min_price_step = float()
        self.trade_fee = float()
        self.expires_on = None
        self.result = dict()

    # MAGIK

    def __str__(self):
        return f'Symbol: {self.ticker_symbol}, Side: {self.sided}, '\
            f'Quantity: {self.base_quantity}, Status: {self.status}, '\
            f'Risk: {self.risk}'

    # SETTERS

    def set_evaluated(self) -> bool:
        '''
        [ NOTE ]:
        '''
        log.debug('')
        return False if not self.check_preconditions() \
            else self.set_state(self.STATUS_EVALUATED)

    def set_commited(self) -> bool:
        '''
        [ NOTE ]:
        '''
        log.debug('')
        return False if not self.check_preconditions() \
            else self.set_state(self.STATUS_COMMITED)

    def set_done(self) -> bool:
        '''
        [ NOTE ]:
        '''
        log.debug('')
        if not self.check_preconditions():
            return False
        self.expires_on = None
        return self.set_state(self.STATUS_DONE)

    def set_state(self, state: str) -> bool:
        log.debug('')
        valid_states = (
            self.STATUS_DRAFT, self.STATUS_EVALUATED, self.STATUS_COMMITED,
            self.STATUS_DONE, self.STATUS_DISCARDED, self.STATUS_EXPIRED,
        )
        if state not in valid_states:
            raise ARInvalidStateException(11, f'Invalid Trade state for {self}')
            return False
        elif self.check_expired():
            state = self.STATUS_EXPIRED
        self.previous_status, self.status = self.status, state
        self.write_date = datetime.datetime.now()
        return True

    # CHECKERS

    def check_preconditions(self):
        '''
        [ NOTE ]: Checks all Trade data to be aligned to the constraints imposed
            by the Trade state. Results may differ when executed in different
            states with the same data set.
        '''
        log.debug('')
        # Enforce ticker symbol trade rules
        checkers = {
            self.STATUS_DRAFT: self.check_preconditions_draft,
            self.STATUS_EVALUATED: self.check_preconditions_evaluated,
            self.STATUS_COMMITED: self.check_preconditions_commited,
            self.STATUS_DONE: self.check_preconditions_done,
        }
        if self.status not in checkers.keys() \
                or not self.check_preconditions_general():
            return False
        return checkers[self.status]()

    def check_time_until_expires(self) -> int:
        '''
        [ RETURN ]: Number of seconds until trade opportunity expires. If the
            trade will not be commited in this time it will no longer be viable
            and the TradingMarket will refuse to execute it.
        '''
        log.debug('')
        if self.check_expired():
            return 0
        now = datetime.datetime.now()
        tdelta = self.expires_on - now
        return int(tdelta.total_seconds())

    def check_expired(self):
        '''
        [ NOTE ]: First it checks if a datetime.datetime object is set to
            expires_on, and if is, verifies if its in the future or the past
            relative to the current datetime.
        '''
        log.debug('')
        now = datetime.datetime.now()
        return now > self.expires_on

    def check_preconditions_general(self):
        log.debug('')
        return False if not self.ticker_symbol or not self.side \
            or not self.base_quantity or not self.current_price else True

    def check_preconditions_draft(self):
        log.debug('')
        return False if not self.risk or not self.trade_fee else True

    def check_preconditions_evaluated(self):
        log.debug('')
        return False if not self._signals or not self.stop_loss_price \
            or not self.take_profit_price or not self.min_price_step else True

    def check_preconditions_commited(self):
        log.debug('')
        return False if not self.result else True

    def check_preconditions_done(self):
        log.debug('')
        return False if self.expires_on else True

    # UPDATES

    def update(self, **new_data) -> bool:
        '''
        [ NOTE ]: Updates the following Trade parameters in a single GO:

            * trade_id
            * ticker_symbol
            * status
            * risk'
            * base_quantity
            * quote_quantity
            * side
            * current_price
            * stop_loss_price
            * take_profit_price
            * trade_fee
        '''
        log.debug('')
        if not new_data:
            return False
        state = self.status
        self.__dict__.update({
            'trade_id': new_data.get('trade-id', self.trade_id),
            'ticker_symbol': new_data.get('ticker-symbol', self.ticker_symbol),
            'status': new_data.get('status', self.status),
            'risk': new_data.get('risk', self.risk),
            'base_quantity': new_data.get('base_quantity', self.base_quantity),
            'quote_quantity': new_data.get('quote_quantity', self.quote_quantity),
            'side': new_data.get('side', self.side),
            'current_price': new_data.get('current_price', self.current_price),
            'stop_loss_price': new_data.get('stop_loss_price', self.stop_loss_price),
            'take_profit_price': new_data.get('take_profit_price', self.take_profit_price),
            'trade_fee': new_data.get('trade_fee', self.trade_fee),
        })
        if self.status != state:
            self.previous_status = state
        self.write_date = datetime.datetime.now()
        return True

    def update_context(self, **new_updates) -> dict:
        '''
        [ NOTE ]: Merges new context values with the olds ones. If there are
            any duplicate value keys, they are overwritten with the new value.
        '''
        log.debug('')
        self._context.update(new_updates)
        return self._context

    def update_signals(self, *new_signals) -> list:
        '''
        [ NOTE ]: Adds more Signal() instances that validate this Trade to the
            list.
        '''
        log.debug('')
        self._signals.extend(new_signals)
        return self._signals

    def update_action_history(self, action: str, ok_flag: bool, **new_updates) -> dict:
        log.debug('')
        timestamp = fetch_timestamp()
        self._history.update({timestamp: {
            'action': action,
            'succeeded': ok_flag,
            'details': new_update,
        }})
        return self._history

    # ACTIONS

    def expire(self) -> bool:
        log.debug('')
        return self.set_state(self.STATUS_EXPIRED)

    def discard(self) -> bool:
        log.debug('')
        return self.set_state(self.STATUS_DISCARDED)

    def next_state(self) -> bool:
        '''
        [ NOTE ]: Acts as a jump-table for unspecified state transitions
        '''
        log.debug('')
        current_state = self.status
        if current_state in (
                self.STATUS_DONE, self.STATUS_DISCARDED, self.STATUS_EXPIRED):
            return False
        state_changers =  {
            self.STATUS_DRAFT: self.set_evaluated,
            self.STATUS_EVALUATED: self.set_commited,
            self.STATUS_COMMITED : self.set_done,
        }
        return state_changers[current_state]()

    def previous_state(self) -> bool:
        log.debug('')
        if not self.previous_status:
            return False
        return self.set_state(self.previous_status)

    def unpack(self, **context) -> dict:
        '''
        [ NOTE ]: Unpacks Trade instance data into kwargs for binance.create_oco_order():

        [ RETURN ]: {
            'symbol':               self.ticker_symbol,
            'side':                 self.side,
            'quantity':             self.base_quantity,
            'stopLimitTimeInForce': self.STOP_ORDER_TIME_IN_FORCE,
            'price':                self.current_price,
            'stopPrice':            self.stop_loss_price,
            'stopLimitPrice':       self.stop_limit_price,
            'listClientOrderID':    self.trade_id,
            'recvWindow':           context.get(
                'recv-window', self._context.get('recv-window', 60000)
            )
        }
        '''
        log.debug('')
        if not self.ticker_symbol or not self.side or not self.base_quantity \
                or not self.current_price:
            return False
        return {
            'symbol': self.ticker_symbol,
            'side': self.side,
            'quantity': self.base_quantity,
            'stopLimitTimeInForce': self.STOP_ORDER_TIME_IN_FORCE,
            'price': self.current_price,
            'stopPrice': self.stop_loss_price,
            'stopLimitPrice': self.stop_limit_price,
            'listClientOrderID': self.trade_id,
            'recvWindow': context.get(
                'recv-window', self._context.get('recv-window', 60000)
            ),
        }


