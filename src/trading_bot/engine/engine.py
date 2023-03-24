import logging
import pysnooper

from src.trading_bot.engine.trade import Trade
from src.trading_bot.engine.strategy.strategy import TradingStrategy
from src.backpack.bp_general import stdout_msg

log = logging.getLogger('AsymetricRisk')


class TradingEngine():
    context: dict

    def __init__(self, *args, **context) -> None:
        log.debug('')
        self.context = context
        self.strategy = None

    # ACTIONS

    def setup(self, **context) -> bool:
        log.debug('')
        self.strategy = TradingStrategy(**context)
        return True

#   @pysnooper.snoop()
    def generate_trade(self, signals: list, market_data: dict, **context) -> Trade:
        log.debug('')
        trade = Trade(**context)
        trade.load_signals(market_data, *signals, **context)
        return trade

#   @pysnooper.snoop()
    def evaluate(self, market_data: dict, **context) -> list:
        log.debug('')
        trades, signals = [], self.strategy.evaluate(market_data, **context)
        buy_signals = [signal for signal in signals if signal.side == 'BUY']
        sell_signals = [signal for signal in signals if signal.side == 'SELL']
        if not signals:
            log.warning('Market data evaluation did not generate any trading signals.')
        elif len(buy_signals) == len(sell_signals):
            log.warning(f'Getting mixed signals :? Discarding {signals}.')
            return []
        elif buy_signals and len(buy_signals) > len(sell_signals):
            trades.append(self.generate_trade(buy_signals, market_data, **context))
        elif sell_signals and len(sell_signals) > len(buy_signals):
            trades.append(self.generate_trade(sell_signals, market_data, **context))
        return trades


