import logging
import pysnooper

from src.trading_bot.engine.strategy.evaluator import *
from src.trading_bot.engine.strategy.signal import Signal

log = logging.getLogger('AsymetricRisk')


# TODO
class TradingStrategy():
    context: dict

    def __init__(self, *args, **context) -> None:
        log.debug('TODO - Under construction, building...')
        self.context = context

    # ACTIONS

    # TODO
    def analyze_risk(self, evaluation: dict, market_data: dict, **context) -> dict:
        log.debug('TODO - Under construction, building...')
        return {}
    def evaluate(self, market_data: dict, **context) -> list:
        log.debug('TODO - Under construction, building...')
        return []
