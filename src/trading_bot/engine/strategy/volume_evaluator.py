import logging
import pysnooper
import pandas as pd

from .abstract_evaluator import AbstractEvaluator
from src.backpack.bp_computers import compute_value_threshold
from src.backpack.bp_general import stdout_msg

log = logging.getLogger('AsymetricRisk')


class VolumeEvaluator(AbstractEvaluator):
    '''
    [ STRATEGY ]: Trading Volume Strategy Evaluator

    [ NOTE ]: Strengthens an already confirmed prive movement.
    '''

    def analyze_risk(self, evaluation: dict, market_data: dict, **context) -> dict:
        log.debug('')
        if not evaluation['trade']:
            return 0
        risk = 5

        # calculate the price change percentage over the last 24 hours
        volume_change_percent = evaluation['volume-movement']['moved-percentage']
        trigger_percent = evaluation['volume-movement']['trigger-percentage']

        # determine the risk of the trade based on the price change percentage
        log.warning(
            'Volume risk analysis based on hardcoded volume movement '
            'percentages! <risk5-(>3%, >1%, >0.5%, >0%)-risk2>'
        )
        if volume_change_percent > 3:
            risk = 5
        elif volume_change_percent > 1:
            risk = 4
        elif volume_change_percent > 0.5:
            risk = 3
        elif volume_change_percent > 0:
            risk = 2
        return risk

    def evaluate(self, market_data: dict, **context) -> dict:
        '''
        [ RETURN ]: {
            "volume-movement": {
                "flag": true,
                "price-direction": "DOWN",
                "start-value": "0.42400000",
                "stop-value": "0.41680000",
                "min-value": "0.41680000",
                "max-value": "0.42520000",
                "moved": 0.03588312,
                "side": "SELL",
                "moved-percentage": 8.463,
                "trigger-percentage": 5
            },
            "interval": "5m",
            "period": 14,
            "value": "0.42350000",
            "risk": 3,
            "side": "SELL",
            "trade": true,
            "description": "Trading Volume Strategy Evaluation"
        }
        '''
        log.debug('')
        evaluation = {
            'volume-movement': self.evaluate_volume_movement(market_data, **context),
            'interval': str(context.get('interval', self.context.get('interval'))),
            'period': int(context.get('period', self.context.get('period'))),
            'value': float(), # Buy price on side BUY, sell price on side SELL
            'risk': int(),
            'side': str(),
            'trade': False,
            'description': 'Trading Volume Strategy Evaluation',
        }
        if not evaluation['volume-movement'] or \
                not evaluation['volume-movement'].get('flag'):
            return evaluation
        evaluation['trade'] = True
        evaluation.update({
            'side': self.evaluate_trade_side(evaluation, market_data, **context),
        })
        evaluation.update({
            'risk': self.analyze_risk(evaluation, market_data, **context),
            'value': self.evaluate_value(evaluation, market_data, **context),
        })
        return evaluation

#   @pysnooper.snoop()
    def evaluate_trade_side(self, evaluation: dict, market_data: dict, **context) -> str:
        log.debug('')
        if not evaluation['trade']:
            return ''
        if evaluation['trade'] and evaluation['volume-movement']['side'].upper() \
                not in ('BUY', 'SELL'):
            log.error('Invalid trade side suggestion in volume movement evaluation!')
            if evaluation['volume-movement']['volume-direction'] not in ('UP', 'DOWN'):
                log.error('Volume direction evaluation failure!')
                return ''
            if evaluation['volume-movement']['volume-direction'] == 'UP':
                return 'BUY'
            elif evaluation['volume-movement']['volume-direction'] == 'DOWN':
                return 'SELL'
        return evaluation['volume-movement']['side']

    def evaluate_value(self, evaluation: dict, market_data: dict, **context) -> float:
        log.debug('')
        return float(market_data['ticker']['symbol']['volume'])

#   @pysnooper.snoop()
    def evaluate_volume_movement(self, market_data: dict, **context) -> dict:
        '''
        [ NOTE ]: Volume movement evaluation from scraped market data -
            * Records the volume of the first/last candles/other volume movement data
            * Determines the overall volume direction
            * Checks to see if large volume movement occured
            * Generates trade signal suggestion based on volume movement

        [ RETURN ]:  {
            'flag':,
            'volume-direction':,
            'start-value':,
            'stop-value':,
            'min-value':,
            'max-value':,
            'moved':,
            'side':,
            'moved-percentage':,
            'trigger-percentage':,
        }
        '''
        log.debug('')
        vol_trigger_percentage = float(
            context.get('volume-movement', self.context.get('volume-movement', 0))
        )
        if not vol_trigger_percentage:
            return False
        volume_values = [
            float(item[5]) for item in market_data['ticker']['historical-klines']
        ]
        evaluation = {
            'flag':               False,                                               #True if moved_percentage >= trigger_percentage else False,
            'volume-direction':   str(),                                               #UP|DOWN
            'start-value':        float(market_data['ticker']['historical-klines'][-1][5]),   #price_values[-1],
            'stop-value':         float(market_data['ticker']['historical-klines'][0][5]),    #price_values[0],
            'min-value':          min(volume_values),                                  #min_val,
            'max-value':          max(volume_values),                                  #max_val,
            'moved':              float(),                                             #price movement in quote currency,
            'side':               str(),                                               #side suggestion post-evaluation,
            'moved-percentage':   float(),                                             #actual price movement percentage,
            'trigger-percentage': vol_trigger_percentage,                              #price_movement,
        }
        evaluation.update({
            'volume-direction': 'UP' if evaluation['start-value'] \
                < evaluation['stop-value'] else 'DOWN',
        })

        # Create Pandas data frame from ticker historical klines - this is used
        # in order to create trade side suggestion
        data = pd.DataFrame(
            market_data['ticker']['historical-klines'],
            columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume',
                'taker_buy_quote_asset_volume', 'ignore'
            ]
        )
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data = data.set_index('timestamp')
        period = context.get('period', self.context.get('period'))

        # Turn specified trigger price movement percentage into actual price
        volume_threshold = compute_value_threshold(
            float(market_data['ticker']['symbol']['volume']),
            evaluation['trigger-percentage'],
        )
        # Calculate volume changes
        data['volume_change'] = data['volume'].diff(periods=period) \
            / data['volume'].shift(periods=period)

        # Generate buy or sell signals based on recent volume changes
        data['signal'] = 0

        # Buy signal
        data.loc[(data['volume_change'] > volume_threshold), 'signal'] = 1

        # Sell signal
        data.loc[(data['volume_change'] < -volume_threshold), 'signal'] = -1
        last_signal = data['signal'].iloc[-1]

        # Update trade side suggestion
        if last_signal == 1:
            evaluation.update({'side': 'BUY',})
        elif last_signal == -1:
            evaluation.update({'side': 'SELL',})
        else:
            evaluation.update({'flag': False, 'side': str(), })

        # Compute the volume change percentage from first and last candles
        evaluation['moved-percentage'] = abs(float(
            ((evaluation['start-value'] - evaluation['stop-value'])
             / evaluation['stop-value']) * 100
        ))

        # Check if the volume movement exceeded the specified percentage
        if evaluation['moved-percentage'] > evaluation['trigger-percentage']:
            # Calculate the actual volume movement
            evaluation.update({
                'flag': True,
                'moved': float(market_data['ticker']['symbol']['volume']) \
                    * evaluation['moved-percentage'] / 100,
            })

        # Second attempt at creating a trading side suggestion
        if not evaluation['side']:
            if evaluation['volume-direction'] not in ('UP', 'DOWN'):
                return evaluation
            evaluation['side'] = 'BUY' if evaluation['volume-direction'] == 'UP' \
                else 'SELL'
        return evaluation

# CODE DUMP

