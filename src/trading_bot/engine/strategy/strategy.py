import logging
import pysnooper

from src.trading_bot.engine.strategy.evaluator import *
from src.trading_bot.engine.strategy.signal import Signal

log = logging.getLogger('AsymetricRisk')


class TradingStrategy():
    context: dict

    # TODO - Not all evaluators implemented
    def __init__(self, *args, **context) -> None:
        log.debug('TODO - Not all evaluators implemented')
        self.context = context
        self.strategy_evaluators = {
            'price': PriceEvaluator(**context),
            'volume': VolumeEvaluator(**context),
#           'rsi': RSIEvaluator(**context),
#           'macd': MACDEvaluator(**context),
#           'adx': ADXEvaluator(**context),
#           'vwap': VWAPEvaluator(**context),
#           'ma': MAEvaluator(**context),
#           'ema': EMAEvaluator(**context),
#           'intuition-reversal': IREvaluator(**context),
        }

    # ACTIONS

#   @pysnooper.snoop()
    def generate_signals(self, evaluation: dict, market_data: dict, **context) -> list:
        '''
        [ NOTE ]: Model strategy evaluation data into Signal() objects.
        '''
        log.debug('')
        signals = []
        for key in evaluation:
            if not evaluation[key]['trade']:
                continue
            sig = Signal(**context)
            load = sig.load_strategy({key: evaluation[key]}, **context)
            if not load:
                continue
            signals.append(sig)
        # Sanitizing signals - leaving only those eligible for trade
        for signal in signals:
            # No trade is risk-less - if risk == 0 no trade is going to happen
            if not signal.risk:
                signals.remove(signal)
        return signals

#   @pysnooper.snoop()
    def evaluate(self, market_data: dict, **context) -> list:
        '''
        [ INPUT ]: Scraped market data.

        [ NOTE ]: Runs strategy evaluations on scraped market data and generates
            BUY|SELL signals.

        [ RETURN ]: List of Signal() instances.
        '''
        log.debug('')
        evaluation, strategy = {}, context.get('strategy', self.context.get('strategy', str())).split(',')
        for evaluator_label in strategy:
            if evaluator_label not in self.strategy_evaluators:
                log.warning(f'Invalid strategy evaluator label! ({evaluator_label})')
                continue
            evaluation[evaluator_label] = self.strategy_evaluators[evaluator_label].evaluate(
                market_data, **context
            )
        return self.generate_signals(evaluation, market_data, **context)
