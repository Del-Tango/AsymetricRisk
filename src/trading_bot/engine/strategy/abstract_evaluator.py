import logging
import pysnooper

from abc import ABC, abstractmethod


class AbstractEvaluator(ABC):
    context: dict

    def __init__(self, *args, **context) -> None:
        self.context = context

    @abstractmethod
    def analyze_risk(self, evaluation: dict, market_data: dict, **context) -> dict:
        pass

    @abstractmethod
    def evaluate(self, market_data: dict, **context) -> dict:
        '''
        [ INPUT ]: {
            'ticker': {
                'symbol': {},
                'info': {},
                'exchange': {},
                'historical-klines': [],
            },
            'account': {
                'account': {},
                'trading-orders': {},
                'deposit-history': {},
                'withdraw-history': {},
                'status': {},
            },
            'api': {
                'server-time': {},
                'permissions': {},
                'trading-status': {},
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
        '''
        pass

