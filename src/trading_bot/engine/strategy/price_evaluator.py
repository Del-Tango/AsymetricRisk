import logging
import pysnooper
import pandas as pd

from .abstract_evaluator import AbstractEvaluator
from src.backpack.bp_computers import compute_value_threshold
from src.backpack.bp_general import stdout_msg

log = logging.getLogger('AsymetricRisk')


class PriceEvaluator(AbstractEvaluator):
    '''
    [ STRATEGY ]: Price Action Strategy Evaluator

    [ NOTE ]: Generates weak buy signal when it detects a large price movement
        up, and a sell signal when it detects a large price movement down. The
        signal is strengthened when the price movement is confirmed by a large
        volume movement up.
    '''

#   @pysnooper.snoop()
    def analyze_risk(self, evaluation: dict, market_data: dict, **context) -> dict:
        log.debug('')
        if not evaluation['trade']:
            return 0
        risk = 5

        # calculate the price change percentage over the last 24 hours
        price_change_percent = evaluation['price-movement']['moved-percentage']
        trigger_percent = evaluation['price-movement']['trigger-percentage']

        # determine the risk of the trade based on the price change percentage
        log.warning(
            'Price action risk analysis based on hardcoded price movement '
            'percentages! <risk5-(>3%, >1%, >0.5%, >0%)-risk2>'
        )
        if price_change_percent > 3:
            risk = 5
        elif price_change_percent > 1:
            risk = 4
        elif price_change_percent > 0.5:
            risk = 3
        elif price_change_percent > 0:
            risk = 2
        return risk

#   @pysnooper.snoop()
    def evaluate(self, market_data: dict, **context) -> dict:
        '''
        [ RETURN ]: {
            "price-movement": {
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
            "description": "Price Action Strategy Evaluation"
        }
        '''
        log.debug('')
        evaluation = {
            'price-movement': self.evaluate_price_movement(market_data, **context),
            'interval': str(context.get('interval', self.context.get('interval'))),
            'period': int(context.get('period', self.context.get('period'))),
            'value': float(), # Buy price on side BUY, sell price on side SELL
            'risk': int(),
            'side': str(),
            'trade': False,
            'description': 'Price Action Strategy Evaluation',
        }
        if not evaluation['price-movement'] or \
                not evaluation['price-movement'].get('flag'):
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
        if evaluation['trade'] and evaluation['price-movement']['side'].upper() \
                not in ('BUY', 'SELL'):
            log.error('Invalid trade side suggestion in price movement evaluation!')
            if evaluation['price-movement']['price-direction'] not in ('UP', 'DOWN'):
                log.error('Price direction evaluation failure!')
                return ''
            if evaluation['price-movement']['price-direction'] == 'UP':
                return 'BUY'
            elif evaluation['price-movement']['price-direction'] == 'DOWN':
                return 'SELL'
        return evaluation['price-movement']['side']

#   @pysnooper.snoop()
    def evaluate_value(self, evaluation: dict, market_data: dict, **context) -> float:
        log.debug('')
        if evaluation['side'] in ('buy', 'Buy', 'BUY'):
            return market_data['ticker']['symbol']['bidPrice']
        elif evaluation['side'] in ('sell', 'Sell', 'SELL'):
            return market_data['ticker']['symbol']['askPrice']
        return 0.0

#   @pysnooper.snoop()
    def evaluate_price_movement(self, market_data: dict, **context) -> dict:
        '''
        [ NOTE ]: Price movement evaluation from scraped market data -
            * Records the first/last closing prices / other price movement data
            * Determines the overall price direction
            * Checks to see if large price movement occured
            * Generates trade signal suggestion based on price movement

        [ RETURN ]:  {
            'flag':,
            'price-direction':,
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
        price_trigger_percentage = int(
            context.get('price-movement', self.context.get('price-movement', 0))
        )
        if not price_trigger_percentage:
            return False
        closing_prices = [item[4] for item in market_data['ticker']['historical-klines']]
        evaluation = {
            'flag':               False,                                               #True if moved_percentage >= trigger_percentage else False,
            'price-direction':    str(),                                               #UP|DOWN
            'start-value':        market_data['ticker']['historical-klines'][-1][4],   #price_values[-1],
            'stop-value':         market_data['ticker']['historical-klines'][0][4],    #price_values[0],
            'min-value':          min(closing_prices),                                 #min_val,
            'max-value':          max(closing_prices),                                 #max_val,
            'moved':              float(),                                             #price movement in quote currency,
            'side':               str(),                                               #side suggestion post-evaluation,
            'moved-percentage':   float(),                                             #actual price movement percentage,
            'trigger-percentage': price_trigger_percentage,                            #price_movement,
        }
        evaluation.update({
            'price-direction': 'UP' if evaluation['start-value'] \
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
        price_threshold = compute_value_threshold(
            market_data['ticker']['symbol']['lastPrice'],
            evaluation['trigger-percentage'],
        )

        # Calculate price changes
        data['price_change'] = data['close'].diff(periods=period) \
            / data['close'].shift(periods=period)

        # Generate buy or sell signals based on recent price and volume changes
        data['signal'] = 0

        # Buy signal
        data.loc[(data['price_change'] > price_threshold), 'signal'] = 1

        # Sell signal
        data.loc[(data['price_change'] < -price_threshold), 'signal'] = -1
        last_signal = data['signal'].iloc[-1]

        # Update trade side suggestion
        if last_signal == 1:
            evaluation.update({'side': 'BUY',})
        elif last_signal == -1:
            evaluation.update({'side': 'SELL',})
        else:
            evaluation.update({'flag': False, 'side': str(), })

        # Extract the price change percentage from the response
        evaluation['moved-percentage'] = abs(float(
            market_data['ticker']['symbol']['priceChangePercent']
        ))

        # Check if the price movement exceeded the specified percentage
        if evaluation['moved-percentage'] > price_trigger_percentage:
            # Calculate the actual price movement
            evaluation.update({
                'flag': True,
                'moved': float(market_data['ticker']['symbol']['lastPrice']) \
                    * evaluation['moved-percentage'] / 100,
            })

        # Second attempt at creating a trading side suggestion
        if not evaluation['side']:
            if evaluation['price-direction'] not in ('UP', 'DOWN'):
                return evaluation
            evaluation['side'] = 'BUY' if evaluation['price-direction'] == 'UP' \
                else 'SELL'
        return evaluation

# CODE DUMP

