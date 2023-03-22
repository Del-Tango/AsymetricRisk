import logging
import pysnooper

from .abstract_evaluator import AbstractEvaluator

log = logging.getLogger('AsymetricRisk')

# TODO
class VWAPEvaluator(AbstractEvaluator):
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
            'value': float(), # Buy price on side BUY, sell price on side SELL
            'interval': str(),
            'period': int(),
            'risk': int(),
            'side': str(),
            'trade': False,
            'description': str(),
        }
        return evaluation

# CODE DUMP

