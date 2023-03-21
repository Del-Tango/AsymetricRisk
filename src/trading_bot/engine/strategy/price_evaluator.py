import logging
import pysnooper

from .abstract_evaluator import AbstractEvaluator

log = logging.getLogger('AsymetricRisk')


class PriceEvaluator(AbstractEvaluator):
    '''
    [ STRATEGY ]: Price Action Strategy Evaluator

    [ NOTE ]: Generates weak buy signal when it detects a large price movement
        up, and a sell signal when it detects a large price movement down. The
        signal is strengthened when the price movement is confirmed by a large
        volume movement up.
    '''
    # TODO
    def evaluate(self, market_data: dict, **context) -> dict:
        '''
        [ INPUT ]: {
            'ticker': {},
            'account': {
                'account': ,
                'trading-orders': ,
                'deposit-history': ,
                'withdraw-history': ,
                'status': ,
            },
            'api': {
                'server-time': ,
                'permissions': ,
                'trading-status': ,
            },
            'indicator': {
                'data'{
                    'rsi': {},
                    'ma': {},
                    'ema': {},
                    'adx': {},
                    'vwap': {},
                    'macd': {},
                },
                'history': {
                    'rsi': {},
                    'ma': {},
                    'ema': {},
                    'adx': {},
                    'vwap': {},
                    'macd': {},
                },
            },
        }

        [ RETURN ]: {
            'price-movement': {flag: True, ...},
            'confirmed-by-volume': {flag: True, volume: {flag: ...}},
            'interval': '1h',
            'period': 14,
            'buy_price': 20903.77,
            'sell_sell': 20910.23,
            'risk': 3,
            'side': 'buy',
            'trade': True,
            'description': 'Price Action Strategy',
        }
        '''
        log.debug('TODO - Under construction, building...')
        evaluation = {
            'price-movement': {},
            'confirmed-by-volume': {},
            'value': float(), # Buy price on side BUY, sell price on side SELL
            'interval': str(),
            'period': int(),
            'risk': int(),
            'side': str(),
            'trade': False,
            'description': 'Price Action Strategy',
        }
        return evaluation



# CODE DUMP


