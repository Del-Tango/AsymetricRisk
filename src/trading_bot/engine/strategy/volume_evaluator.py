import logging
import pysnooper

from .abstract_evaluator import AbstractEvaluator

log = logging.getLogger('AsymetricRisk')

# TODO
class VolumeEvaluator(AbstractEvaluator):
    '''
    [ STRATEGY ]:  Strategy Evaluator
    '''
    # TODO
    def analyze_risk(self, evaluation: dict, market_data: dict, **context) -> dict:
        log.debug('TODO - Under construction, building...')
        return {}
    def evaluate(self, market_data: dict, **context) -> dict:
        '''
        '''
        log.debug('TODO - Under construction, building...')
        evaluation = {
            'volume-movement': dict(),
            'value': float(), # Buy price on side BUY, sell price on side SELL
            'interval': str(),
            'period': int(),
            'risk': int(),
            'side': str(),
            'trade': False,
            'description': str(),
        }
        return evaluation


    # TODO - Move to Volume evaluator
    def evaluate_volume_movement(self, evaluation: dict, market_data: dict,
                                             **context) -> dict:
        log.debug('TODO - Under construction, building...')
        # TODO - Check trade flag
        # TODO - Check if volume moved up at the same time as price
        vol_trigger_percentage = int(
            context.get('volume-movement', self.context.get('volume-movement', 0))
        )
        if not evaluation['trade'] or not vol_trigger_percentage:
            return False
        # TODO
#       volume_threshold = compute_value_threshold(current_price, vol_trigger_percentage)
#       data['vol_change'] = data['volume'].diff(periods=period) \
#           / data['volume'].shift(periods=period)
#       data.loc[(data['vol_change'] > vol_threshold), 'signal'] = 1  # Buy signal
#       data.loc[(data['vol_change'] < -vol_threshold), 'signal'] = -1  # Sell signal
    def evaluate_trade_risk(self):
        pass
    def evaluate_value(self):
        pass
    def evaluate_trade_side(self):
        pass


# CODE DUMP

