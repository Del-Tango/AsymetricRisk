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
        buy_signals = [signal for signal in signals if signal.side == 'BUY']
        sell_signals = [signal for signal in signals if signal.side == 'SELL']
        if buy_signals:
            trade = Trade(**context)
            trade.load_signals(*buy_signals, **context)
            trades.append(trade)
        if sell_signals:
            trade = Trade(**context)
            trade.load_signals(*sell_signals, **context)
            trades.append(trade)

        # TODO - Remove 1 down
        stdout_msg(f'[ DEBUG ]: SIGNALS: {signals}', red=True)
        stdout_msg(f'[ DEBUG ]: TRADES: {trades}', red=True)

        return trades


