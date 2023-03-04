#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ENGINE

import datetime
import logging
import pysnooper

from .ar_trade import Trade

log = logging.getLogger('AsymetricRisk')


class TradingEngine():

    def __init__(self, *args, **kwargs):
        self.create_date = datetime.datetime.now()
        self.write_date = self.create_date
        self.context = kwargs.copy()
        self.cache_limit = kwargs.get('cache-limit', 10)
        self.trade_cache = []

    def validate(self, *args, **kwargs):
        '''
        [ INPUT ]:
            *args = (Trade(), Trade(), ...)
            **kwargs = {context...}

        [ NOTE ]: TradingEngine.validate(Trade)

        [ RETURN ]: {
            'failures': 1,
            'ok': [Trade(), ],
            'nok': [Trade(), ],
        }
        '''
        failures, ok, nok = 0, [], []
        for trade in args:
            if not isinstance(trade, Trade):
                failures += 1
                nok.append(trade)
                continue
            ok.append(trade)
        return {
            'failures': failures,
            'ok': ok,
            'nok': nok,
        }

    def update_trade_cache(self, trade_object, **kwargs):
        self.trade_cache.append(trade_object)
        self.write_date = datetime.datetime.now()
        if len(self.trade_cache) >= self.cache_limit:
            elements_to_remove = len(self.trade_cache) - int(self.cache_limit)
            trimmed_cache = self.trade_cache[elements_to_remove:]
            self.trade_cache = trimmed_cache
        return True

    def generate(self, *args, **kwargs):
        '''
        [ INPUT ]: **kwargs = {context...}

        [ NOTE ]: trade = TradingEngine.generate(**data)

        [ RETURN ]: Trade() or False
        '''
        trade = Trade(*args, **kwargs)
        if trade:
            self.update_trade_cache(trade)
        return trade or False



