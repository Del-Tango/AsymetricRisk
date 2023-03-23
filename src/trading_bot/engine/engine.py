import logging
import pysnooper

from src.trading_bot.engine.trade import Trade
from src.trading_bot.engine.strategy.strategy import TradingStrategy
from src.backpack.bp_general import stdout_msg, pretty_dict_print

log = logging.getLogger('AsymetricRisk')


class TradingEngine():
    context: dict

    def __init__(self, *args, **context) -> None:
        log.debug('TODO - Not all evaluators implemented')
        self.context = context
        self.strategy = None

    # ACTIONS

    def setup(self, **context):
        log.debug('')
        self.strategy = TradingStrategy(**context)
        return True

    # TODO
    def generate_trades(self, signals: list, market_data: dict, **context) -> list:
        log.debug('TODO')
        return []

    # TODO
    def evaluate(self, market_data: dict, **context) -> list:
        log.debug('TODO')
        trades, signals = [], self.strategy.evaluate(market_data, **context)

        # TODO - Remove 1 down
        stdout_msg(f'[ DEBUG ]: SIGNALS?? {signals}', red=True)

        return trades


