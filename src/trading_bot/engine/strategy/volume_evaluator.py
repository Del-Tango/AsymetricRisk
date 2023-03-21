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

