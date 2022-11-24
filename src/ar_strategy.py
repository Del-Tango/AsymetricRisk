#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADING BOT

import logging
import pysnooper
import pprint

from src.backpack.bp_general import stdout_msg, pretty_dict_print, scan_value_sets
from src.backpack.bp_computers import compute_percentage, compute_percentage_of
from src.backpack.bp_checkers import check_majority_in_set

log = logging.getLogger('AsymetricRisk')


class TradingStrategy():

    def __init__(self, *args, **kwargs):
        log.debug('')
        self.risk_tolerance = kwargs.get('risk-tolerance', 1) # less-risk 1, 2, 3, 4, 5 more-risk
        self.adx_bottom = kwargs.get('adx-bottom', 25)
        self.adx_top = kwargs.get('adx-top', 70)
        self.rsi_bottom = kwargs.get('rsi-bottom', 30)
        self.rsi_top = kwargs.get('rsi-top', 70)
        self.strategies = {
            'vwap': self.strategy_vwap,
            'rsi': self.strategy_rsi,
            'macd': self.strategy_macd,
            'ma': self.strategy_ma,
            'ema': self.strategy_ema,
            'adx': self.strategy_adx,
            'volume': self.strategy_volume,
            'price': self.strategy_price,
        }
        self.risk_evaluators = {
            1: self.evaluate_low_risk_tolerance,
            2: self.evaluate_low_mid_risk_tolerance,
            3: self.evaluate_mid_risk_tolerance,
            4: self.evaluate_mid_high_risk_tolerance,
            5: self.evaluate_high_risk_tolerance,
        }
        self.base_evaluators = {
            'buy': self.evaluate_buy,
            'sell': self.evaluate_sell,
            'trade': self.evaluate_trade,
        }

    # FETCHERS

    # SETTERS

    def set_risk_tolerance(self, risk_index):
        log.debug('')
        if risk_index > 5 or risk_index < 0:
            return False
        self.risk_tolerance = risk_index
        return self.risk_tolerance

    # CHECKERS

    def check_vwap_bullish_trend_confirmation(self, *args, **kwargs):
        '''
        [ NOTE ]: Buy when price is trading below VWAP and then breaks to begin
                  to trade above it - Bullish Trend Confirmation
        '''
        log.debug('')
        crossover = self.check_vwap_crossover(*args, direction='bullish', **kwargs)
        if crossover['flag'] and crossover['price-direction'] == 'up' \
                and crossover['scan']['start2'] < crossover['scan']['start1']:
            crossover['side'] = 'buy'
        else:
            crossover['flag'] = False
        return crossover

    def check_vwap_bearish_trend_confirmation(self, *args, **kwargs):
        '''
        [ NOTE ]: Sell when price is trading above VWAP and the breaks to begin
                  to trade below it - Bearish Trend Confirmation
        '''
        log.debug('')
        crossover = self.check_vwap_crossover(*args, direction='bearish', **kwargs)
        if crossover['flag'] and crossover['price-direction'] == 'down' \
                and crossover['scan']['start2'] > crossover['scan']['start1']:
            crossover['side'] = 'sell'
        else:
            crossover['flag'] = False
        return crossover

    def check_vwap_crossover(self, *args, direction='bullish', **kwargs):
        log.debug('')
        details = kwargs['details']['history']
        vwap_values = {
            'vwap': [ float(details['vwap'][index]['value'])
                    for index in range(len(details['vwap'])) ],
            'price': [ float(details['price'][index]['value'])
                     for index in range(len(details['price'])) ],
        }
        scan = scan_value_sets(
            vwap_values['vwap'], vwap_values['price'], look_for='crossover'
        )
        return_dict = {
            'flag': scan['flag'],
            'start-candle': details['vwap'][len(details['vwap'])-1]['backtrack'],
            'stop-candle': details['vwap'][0]['backtrack'],
            'vwap-direction': scan['direction1'] if direction == 'bullish' \
                else scan['direction2'],
            'price-direction': scan['direction2'] if direction == 'bullish' \
                else scan['direction1'],
            'side': '',
            'values': vwap_values,
            'scan': scan,
        }
        return return_dict

    def check_rsi_bullish_divergence(self, *args, **kwargs):
        log.debug('')
        divergence = self.check_rsi_divergence(
            *args, direction='bullish', **kwargs
        )
        if divergence['flag'] and divergence['rsi-direction'] == 'up' \
                and divergence['price-direction'] == 'down':
            divergence['side'] = 'buy'
        else:
            divergence['flag'] = False
        return divergence

    def check_rsi_bearish_divergence(self, *args, **kwargs):
        log.debug('')
        divergence = self.check_rsi_divergence(
            *args, direction='bearish', **kwargs
        )
        if divergence['flag'] and divergence['rsi-direction'] == 'down' \
                and divergence['price-direction'] == 'up':
            divergence['side'] = 'sell'
        else:
            divergence['flag'] = False
        return divergence

    def check_rsi_divergence(self, *args, direction='bullish', **kwargs):
        log.debug('')
        details = kwargs['details']['history']
        rsi_values = {
            'rsi': [ float(details['rsi'][index]['value'])
                    for index in range(len(details['macd'])) ],
            'price': [ float(details['price'][index]['value'])
                    for index in range(len(details['macd'])) ],
        }
        scanner_args, scanner_kwargs = [], {
            'look_for': 'divergence', 'peak_distance': 1, 'error_margin': 1
        }
        if direction == 'bullish':
            scanner_args = [rsi_values['rsi'], rsi_values['price']]
        elif direction == 'bearish':
            scanner_args = [rsi_values['price'], rsi_values['rsi']]
        scan = scan_value_sets(*scanner_args, **scanner_kwargs)
        return_dict = {
            'flag': False,
            'start-candle': details['rsi'][len(details['rsi'])-1]['backtrack'],
            'stop-candle': details['rsi'][0]['backtrack'],
            'rsi-direction': scan['direction1'] if direction == 'bullish' \
                else scan['direction2'],
            'price-direction': scan['direction2'] if direction == 'bullish' \
                else scan['direction1'],
            'values': rsi_values,
            'scan': scan,
        }
        if not scan['flag'] or not scan['confirmed']:
            return return_dict
        return_dict['flag'] = scan['flag']
        return return_dict

#   @pysnooper.snoop()
    def check_macd_bullish_divergence(self, *args, **kwargs):
        log.debug('')
        divergence = self.check_macd_divergence(*args, direction='bullish', **kwargs)
        if divergence['flag'] and divergence['macd-direction'] == 'up' \
                and divergence['price-direction'] == 'down':
            divergence['side'] = 'buy'
        else:
            divergence['flag'] = False
        return divergence

#   @pysnooper.snoop()
    def check_macd_bearish_divergence(self, *args, **kwargs):
        log.debug('')
        divergence = self.check_macd_divergence(*args, direction='bearish', **kwargs)
        if divergence['flag'] and divergence['macd-direction'] == 'down' \
                and divergence['price-direction'] == 'up':
            divergence['side'] = 'sell'
        else:
            divergence['flag'] = False
        return divergence

#   @pysnooper.snoop()
    def check_macd_divergence(self, *args, direction='bullish', **kwargs):
        log.debug('')
        details = kwargs['details']['history']
        macd_values = {
            'macd': [ float(details['macd'][index]['valueMACD'])
                    for index in range(len(details['macd'])) ],
            'signal': [ float(details['macd'][index]['valueMACDSignal'])
                    for index in range(len(details['macd'])) ],
            'history': [ float(details['macd'][index]['valueMACDHist'])
                    for index in range(len(details['macd'])) ],
            'price': [ float(details['price'][index]['value'])
                    for index in range(len(details['macd'])) ]
        }
        scanner_args, scanner_kwargs = [], {
            'look_for': 'divergence-peaks', 'peak_distance': 1, 'error_margin': 1
        }
        if direction == 'bullish':
            scanner_args = [macd_values['macd'], macd_values['price']]
        elif direction == 'bearish':
            scanner_args = [macd_values['price'], macd_values['macd']]
        scan = scan_value_sets(*scanner_args, **scanner_kwargs)
        return_dict = {
            'flag': False,
            'start-candle': details['macd'][len(details['macd'])-1]['backtrack'],
            'stop-candle': details['macd'][0]['backtrack'],
            'macd-direction': scan['direction1'] if direction == 'bullish' \
                else scan['direction2'],
            'price-direction': scan['direction2'] if direction == 'bullish' \
                else scan['direction1'],
            'values': macd_values,
            'scan': scan,
        }
        if not scan['flag'] or not scan['confirmed'] \
                or len(scan['peaks']) not in (2, 3):
            return return_dict
        return_dict['flag'] = scan['flag']
        return return_dict

#   @pysnooper.snoop()
    def check_macd_bullish_crossover(self, *args, **kwargs):
        log.debug('')
        crossover = self.check_macd_crossover(*args, **kwargs)
        if crossover['flag'] and crossover['macd-direction'] == 'up':
            crossover['side'] = 'sell'
        else:
            crossover['flag'] = False
        return crossover

#   @pysnooper.snoop()
    def check_macd_bearish_crossover(self, *args, **kwargs):
        log.debug('')
        crossover = self.check_macd_crossover(*args, **kwargs)
        if crossover['flag'] and crossover['macd-direction'] == 'down':
            crossover['side'] = 'sell'
        else:
            crossover['flag'] = False
        return crossover

#   @pysnooper.snoop()
    def check_macd_crossover(self, *args, **kwargs):
        log.debug('')
        details = kwargs['details']['history']
        macd_values = {
            'macd': [ float(details['macd'][index]['valueMACD'])
                    for index in range(len(details['macd'])) ],
            'signal': [ float(details['macd'][index]['valueMACDSignal'])
                    for index in range(len(details['macd'])) ],
            'history': [ float(details['macd'][index]['valueMACDHist'])
                    for index in range(len(details['macd'])) ],
        }
        scan = scan_value_sets(
            macd_values['macd'], macd_values['signal'], look_for='crossover'
        )
        return_dict = {
            'flag': False,
            'start-candle': details['macd'][len(details['macd'])-1]['backtrack'],
            'stop-candle': details['macd'][0]['backtrack'],
            'macd-direction': scan['direction1'],
            'signal-direction': scan['direction2'],
            'values': macd_values,
            'scan': scan,
        }
        if not scan['flag'] or not scan['confirmed'] \
                or len(scan['crossovers']) not in (2, 3, 4):
            return return_dict
        return_dict['flag'] = scan['flag']
        return return_dict

    def check_adx_crossover(self, *args, **kwargs):
        log.debug('')
        details = kwargs['details']['history']
        adx_top = float(kwargs.get('adx-top', self.adx_top))
        adx_bottom = float(kwargs.get('adx-bottom', self.adx_bottom))
        adx_values = {
            'adx': [ float(details['adx'][index]['adx'])
                    for index in range(len(details['adx'])) ],
            '+di': [ float(details['adx'][index]['plusdi'])
                    for index in range(len(details['adx'])) ],
            '-di': [ float(details['adx'][index]['minusdi'])
                    for index in range(len(details['adx'])) ],
        }
        scan = scan_value_sets(
            adx_values['+di'], adx_values['-di'], look_for='crossover'
        )
        return_dict = {
            'flag': False, #scan.get('flag', False),
            'start-candle': details['adx'][len(details['adx'])-1]['backtrack'],
            'stop-candle': details['adx'][0]['backtrack'],
            'side': '',
            'values': adx_values,
            'scan': scan,
        }
        if not scan['flag']:
            return return_dict
        for index in return_dict['scan']['crossovers']:
            if not adx_values['adx'][index] > adx_bottom:
                continue
            return_dict['flag'] = True
        return return_dict

#   @pysnooper.snoop()
    def check_adx_bullish_crossover(self, *args, **kwargs):
        '''
        [ NOTE ]: When a Bullish Crossover occurs (when the ADX line is above
                  25 and the +DI line moves upward, which is from below to above
                  the -DI line), we must buy at the next candle after the
                  Crossover and place the stop-loss lower than the previous candle.
        '''
        log.debug('')
        return_dict = self.check_adx_crossover(*args, **kwargs)
        if not return_dict['scan']['flag']:
            return return_dict
        return_dict['flag'] = True \
            if return_dict['scan']['direction1'] == 'up' else False
        return_dict.update({
            'flag': True if return_dict['scan']['direction1'] == 'down' else False,
            'side': 'buy' if return_dict['scan']['flag'] else '',
        })
        return return_dict

#   @pysnooper.snoop()
    def check_adx_bearish_crossover(self, *args, **kwargs):
        '''
        [ NOTE ]: When a Bearish Crossover occurs (when the ADX line is above 25
                  and the +DI line moves downward, which is from above to below
                  the -DI line), we must sell at the next candle after the
                  Crossover and place the stop-loss higher than the previous candle.
        '''
        log.debug('')
        return_dict = self.check_adx_crossover(*args, **kwargs)
        if not return_dict['scan']['flag']:
            return return_dict
        return_dict.update({
            'flag': True if return_dict['scan']['direction1'] == 'down' else False,
            'side': 'sell' if return_dict['scan']['flag'] else '',
        })
        return return_dict

#   @pysnooper.snoop()
    def check_price_movement_confirmed_by_volume(self, price_dict, **kwargs):
        log.debug('')
        check_volume = self.check_large_volume_movement(**kwargs)
        return_dict = {
            'flag': False if not price_dict['flag'] else check_volume['flag'],
            'volume': check_volume,
        }
        if price_dict['flag'] and return_dict['volume']['flag'] \
                and return_dict['volume']['side'] == 'up':
            log.debug(
                'Large price movement confirmed by large volume movement!',
            )
        elif price_dict['flag'] and not return_dict['volume']['flag']:
            log.debug(
                'Large price movement was not confirmed by volume movement.'
            )
        return return_dict

#   @pysnooper.snoop()
    def check_large_volume_movement(*args, **kwargs):
        log.debug('')
        volume_movement = int(kwargs.get('volume-movement', 0)) # %
        if volume_movement == 0:
            stdout_msg(
                'Cannot compute if I duonno what a large volume movement is! '
                'Please specify', err=True
            )
            return False
        details = kwargs['details']['history']
        volume_values = [
            float(details['volume'][index]['value'])
            for index in range(len(details['volume']))
        ]
        period_volume_avg = sum(volume_values) / len(volume_values)
        min_val, max_val = min(volume_values), max(volume_values)
        min_candle = [
            item for item in details['volume']
            if float(item['value']) == float(min_val)
        ]
        if min_candle:
            min_candle = min_candle[0]['backtrack']
        max_candle = [
            item for item in details['volume']
            if float(item['value']) == float(max_val)
        ]
        if max_candle:
            max_candle = max_candle[0]['backtrack']
        movement = max_val - min_val
        move_percent = compute_percentage_of(movement, period_volume_avg)
        return_dict = {
            'flag': True if move_percent >= volume_movement else False,
            'start-value': volume_values[-1],
            'stop-value': volume_values[0],
            'min-value': min_val,
            'max-value': max_val,
            'period-average': period_volume_avg,
            'start-candle': details['volume'][len(volume_values)-1]['backtrack'],
            'stop-candle': details['volume'][0]['backtrack'],
            'min-candle': min_candle or None,
            'max-candle': max_candle or None,
            'side': '',
            'moved': movement,
            'moved-percentage': move_percent,
            'trigger-percentage': volume_movement,
        }
        return_dict.update({
            'side': 'up' if min_candle > max_candle else 'down',
        })
        if move_percent >= volume_movement:
            log.debug('Large volume movement detected!')
        else:
            log.debug(
                'No large volume movement occured over period. '
                'Moved by {}%'.format(move_percent)
            )
        return return_dict

#   @pysnooper.snoop()
    def check_large_price_movement(self, *args, **kwargs):
        log.debug('')
        price_movement = int(kwargs.get('price-movement', 0)) # %
        if price_movement == 0:
            stdout_msg(
                'Cannot compute if I duonno what a large price movement is! '
                'Please specify', err=True
            )
            return False
        details = kwargs['details']['history']
        if isinstance(details['price'], dict) and details['price'].get('error'):
            stdout_msg(
                'Price history error - {}'.format(details['price']['error']), err=True
            )
        price_values = [
            float(details['price'][index]['value'])
            for index in range(len(details['price']))
        ]
        period_price_avg = sum(price_values) / len(price_values)
        min_val = float(details.get('price-support', min(price_values)))
        max_val = float(details.get('price-resistance', max(price_values)))
        min_candle = [
            item for item in details['price']
            if float(item['value']) == float(min_val)
        ]
        if min_candle:
            min_candle = min_candle[0]['backtrack']
        max_candle = [
            item for item in details['price']
            if float(item['value']) == float(max_val)
        ]
        if max_candle:
            max_candle = max_candle[0]['backtrack']
        movement = max_val - min_val
        move_percent = compute_percentage_of(movement, period_price_avg)
        return_dict = {
            'flag': True if move_percent >= price_movement else False,
            'start-value': price_values[-1],
            'stop-value': price_values[0],
            'min-value': min_val,
            'max-value': max_val,
            'period-average': period_price_avg,
            'start-candle': details['price'][len(price_values)-1]['backtrack'],
            'stop-candle': details['price'][0]['backtrack'],
            'min-candle': min_candle or None,
            'max-candle': max_candle or None,
            'moved': movement,
            'side': '',
            'moved-percentage': move_percent,
            'trigger-percentage': price_movement,
        }
        return_dict.update({
            'side': 'up' if min_candle > max_candle else 'down',
        })
        if move_percent >= price_movement:
            log.debug('Large price movement detected!')
        else:
            log.debug(
                'No large price movement occured over period. '
                'Moved by {}%'.format(move_percent)
            )
        return return_dict

    # GENERAL

    def load_strategy(self, **kwargs):
        '''
        [ INPUT ]: **{label: self.function_reference, ...}
        '''
        log.debug('')
        if not kwargs:
            return False
        self.strategies.update(kwargs)
        return self.strategies

    # ACTIONS

    @pysnooper.snoop()
    def analyze_risk(self, strategy='vwap', side='auto', **kwargs):
        log.debug('')
        log.debug('Risk Analyzer received kwargs - {}'.format(kwargs))
        failures = 0
        trade_flag, risk_index, trade_side, evaluations = False, 0, side, {}
        stdout_msg('Computing strategy...', info=True)
        for strategy_label in strategy.split(','):
            if strategy_label not in self.strategies:
                failures += 1
                stdout_msg('Strategy {}'.format(strategy_label), nok=True)
                continue
            # Compute trading strategy
            evaluations[strategy_label] = self.strategies[strategy_label](**kwargs)
            stdout_msg(
                'Strategy {} - \n{}'.format(
                    strategy_label,
                    pretty_dict_print(evaluations[strategy_label])
                ),
                ok=False if not evaluations[strategy_label] else True,
                nok=False if evaluations[strategy_label] else True,
            )
        # Evaluate risk of give strategy results
        stdout_msg('Evaluating trading risk', info=True)
        trade_flag, risk_index, trade_side = self.risk_evaluators[self.risk_tolerance](
            evaluations, side=side, details=kwargs.get('details', {})
        )
        stdout_msg(
            'Risk evaluation: Trade - {}, Risk - {}, Side - {}'.format(
                trade_flag, risk_index, trade_side
            ),
            ok=False if not trade_flag else True,
            nok=False if trade_flag else True,
        )
        return trade_flag, risk_index, trade_side, failures

    # COMPUTERS

    # TODO
    def compute_vwap_trade_risk(self, return_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_rsi_trade_risk(self, return_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_macd_trade_risk(self, return_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_trade_flag(self, evaluations_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_adx_trade_risk(self, return_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_volume_trade_risk(self, return_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_risk_index(self, evaluations_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_price_trade_risk(self, return_dict, **kwargs):
        '''
        [ INPUT ]: return_dict - {
            'price-movement': ,
            'confirmed-by-volume': ,
            'interval': ,
            'value': ,
            'risk': ,
            'trade': ,
            'description': ,
        }

        kwargs - {}

        [ RETURN ]: risk_index - type int - values low.1-5.high
        '''
        log.debug('TODO - Under construction, building...')
        return 0

    # EVALUATORS


    # TODO
    def evaluate_buy(self, evaluations_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        instruction_set = kwargs.copy()
        instruction_set.update({'side': 'buy'})
        return self.evaluate_risk(evaluations_dict, **instruction_set)
#       if not evaluations_dict:
#           return False
#       trade_flag, risk_index = False, 0
#       return trade_flag, risk_index
    def evaluate_sell(self, evaluations_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        instruction_set = kwargs.copy()
        instruction_set.update({'side': 'sell'})
        return self.evaluate_risk(evaluations_dict, **instruction_set)
#       if not evaluations_dict:
#           return False
#       trade_flag, risk_index = False, 0
#       risk_values = [
#           int(evaluations_dict[indicator_label]['risk'])
#           for indicator_label in evaluations_dict
#       ]
#       risk_index = sum(risk_values) / len(risk_values)
#       trade_flag = True if risk_index <= self.risk_tolerance \
#           and risk_index != 0 else False
#       return trade_flag, risk_index



    def evaluate_risk(self, evaluations_dict, **kwargs):
        '''
        [ NOTE ]: Risk index is evaluated from the given indicator/strategy count
                  divided by no: vwap, rsi, ma, ema, adx, macd, price, volume

        [ INPUT ]: evaluations_dict - {
            'vwap': {value: 2435.897674764, interval: 5m, risk: 3, trade: False, description: VWAP},
            'rsi': {value: , interval: , risk: , trade: , description: },
            'ma': {value: , interval: , risk: , trade: , description: },
            'ema': {value: , interval: , risk: , trade: , description: },
            'macd': {value: , interval: , risk: , trade: , description: },
            'macd-signal': {value: , interval: , risk: , trade: , description: },
            'macd-hist': {value: , interval: , risk: , trade: , description: },
            'adx': {value: , interval: , risk: , trade: , description: },
            'price': {value: , interval: , risk: , trade: , description: },
            'volume': {value: , interval: , risk: , trade: , description: },
            ...
        }
        '''
        log.debug('TODO - Under construction, building...')
        log.info('evaluations_dict - {}'.format(evaluations_dict))
        log.info('kwargs - {}'.format(kwargs))
        if not evaluations_dict:
            stdout_msg(
                'Necessary data set for risk evaluation not found!', err=True
            )
            return False
        trade_flag, risk_index = False, 0
        risk_values = [
            int(evaluations_dict[indicator_label]['risk'])
            for indicator_label in evaluations_dict
            if evaluations_dict[indicator_label]
        ]
        risk_index = sum(risk_values) / len(risk_values)
        trade_flag = True if risk_index <= self.risk_tolerance \
            and risk_index != 0 else False
        return trade_flag, risk_index

    def evaluate_trade(self, evaluations_dict, **kwargs):
        log.debug('')
        if not evaluations_dict or not self.base_evaluators:
            return False
        trade_flag, risk_index, trade_side = False, 0, kwargs.get('side', 'auto')
        if trade_side == 'auto':
            buy_flag, buy_risk = self.base_evaluators['buy'](
                evaluations_dict, **kwargs
            )
            sell_flag, sell_risk = self.base_evaluators['sell'](
                evaluations_dict, **kwargs
            )
            if buy_flag:
                trade_flag, trade_side, risk_index = buy_flag, 'buy', buy_risk
            elif sell_flag:
                trade_flag, trade_side, risk_index = sell_flag, 'sell', sell_risk
        else:
            trade_flag, risk_index = self.base_evaluators[trade_side](
                evaluations_dict, **kwargs
            )
        return trade_flag, risk_index, trade_side

    def evaluate_low_risk_tolerance(self, evaluations_dict, **kwargs):
        log.debug('')
        trade_flag, risk_index, trade_side = self.base_evaluators['trade'](
            evaluations_dict, **kwargs
        )
        return trade_flag if risk_index <= 1 else False, risk_index, trade_side

    def evaluate_low_mid_risk_tolerance(self, evaluations_dict, **kwargs):
        log.debug('')
        trade_flag, risk_index, trade_side = self.base_evaluators['trade'](
            evaluations_dict, **kwargs
        )
        return trade_flag if risk_index <= 2 else False, risk_index, trade_side

    def evaluate_mid_risk_tolerance(self, evaluations_dict, **kwargs):
        log.debug('')
        trade_flag, risk_index, trade_side = self.base_evaluators['trade'](
            evaluations_dict, **kwargs
        )
        return trade_flag if risk_index <= 3 else False, risk_index, trade_side

    def evaluate_mid_high_risk_tolerance(self, evaluations_dict, **kwargs):
        log.debug('')
        trade_flag, risk_index, trade_side = self.base_evaluators['trade'](
            evaluations_dict, **kwargs
        )
        return trade_flag if risk_index <= 4 else False, risk_index, trade_side

    def evaluate_high_risk_tolerance(self, evaluations_dict, **kwargs):
        log.debug('')
        return self.base_evaluators['trade'](evaluations_dict, **kwargs)

    # STRATEGIES

    # TODO
    def strategy_ma(self, *args, **kwargs):
        '''
        [ STRATEGY ]: Moving Average

        [ NOTE ]: Technical indicator that sums up the data points of a financial
                  security over a specific time period and divides the total by
                  the number of data points to arrive at an average.

                  It's called a "Moving" Average because it is continually
                  recalculated based on the latest price data.

        [ NOTE ]: Used to examine support and resistance by evaluating the
                  movements of an assets price.

        [ INPUT ]:
        [ RETURN ]:
        '''
        log.debug('TODO - Under construction, building...')
        # TODO - Research
    def strategy_ema(self, *args, **kwargs):
        '''
        [ STRATEGY ]: Exponential Moving Average

        [ NOTE ]: A Moving Average which gives more weight to the most recent
                  price points to make it more responsive to recent data points.

        [ INPUT ]:
        [ RETURN ]:
        '''
        log.debug('TODO - Under construction, building...')
        # TODO - Research

    @pysnooper.snoop()
    def strategy_vwap(self, *args, **kwargs):
        '''
        [ STRATEGY ]: Volume Weighted Average Price

        [ NOTE ]: Buy when price is trading below VWAP and then breaks to begin
                  to trade above it - Bullish Trend Confirmation

        [ NOTE ]: Sell when price is trading above VWAP and the breaks to begin
                  to trade below it - Bearish Trend Confirmation

        [ INPUT ]:
        [ RETURN ]:
        '''
        log.debug('')
        return_dict = {
            'bullish-crossover': self.check_vwap_bullish_trend_confirmation(*args, **kwargs),
            'bearish-crossover': self.check_vwap_bearish_trend_confirmation(*args, **kwargs),
            'interval': kwargs.get('vwap-interval', kwargs.get('interval')),
            'period': kwargs.get('vwap-period', kwargs.get('period')),
            'risk': 0,
            'trade': False,
            'description': 'Volume Weighted Average Price Strategy',
        }
        if return_dict['bullish-crossover']['flag']:
            stdout_msg(
                'VWAP Bullish Trend Confirmation detected! Triggered when when '
                'price is trading below VWAP and then breaks to begin to trade '
                'above it.',  ok=True
            )
        elif return_dict['bearish-crossover']['flag']:
            stdout_msg(
                'VWAP Bearish Trend Confirmation detected! Triggered when price '
                'is trading above VWAP and the breaks to begin to trade below it ',
                ok=True
            )
        return_dict['risk'] = self.compute_vwap_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = True if check_majority_in_set(True, [
            return_dict[label]['flag'] for label in (
                'bullish-crossover', 'bearish-crossover'
            )
        ]) else False
        if return_dict['trade']:
            return_dict['side'] = [
                return_dict[item]['side'] for item in (
                    'bullish-crossover', 'bearish-crossover'
                ) if return_dict[item]['flag']
            ][0]
        return return_dict

    @pysnooper.snoop()
    def strategy_rsi(self, *args, **kwargs):
        '''
        [ STRATEGY ]: Relative Strength Index

        [ NOTE ]: When to buy? When a Bullish Divergence occurs (when price
                  makes lower lows but RSI makes higher lows).

                  This could be a sign that downward momentum is waining and a
                  bullish reversal may follow.

                  After spotting a Bullish Divergence an investor might use a
                  crossback above 30 as an entry signal.

        [ NOTE ]: When to sell? When a Bearish Divergence occurs (when price
                  makes higher highs, but RSI makes lower highs).

                  This could be a sign that upward momentum is slowing, and a
                  Bearish Reversal may occur.

                  After spotting a Bearish Divergence an investor might use a
                  crossback below 70 as an exit signal.

        [ INPUT ]:
        [ RETURN ]:
        '''
        log.debug('')
        return_dict = {
            'bullish-divergence': self.check_rsi_bullish_divergence(*args, **kwargs),
            'bearish-divergence': self.check_rsi_bearish_divergence(*args, **kwargs),
            'interval': kwargs.get('rsi-interval', kwargs.get('interval')),
            'period': kwargs.get('rsi-period', kwargs.get('period')),
            'risk': 0,
            'trade': False,
            'side': '',
            'description': 'Relative Strength Index Strategy',
        }

        if return_dict['bullish-divergence']['flag']:
            stdout_msg('RSI Bullish Divergence detected!')
        elif return_dict['bearish-divergence']['flag']:
            stdout_msg('RSI Bearish Divergence detected!')

        return_dict['risk'] = self.compute_rsi_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = True if True in [
            return_dict[label]['flag'] for label in (
                'bullish-divergence', 'bearish-divergence',
            )
        ] else False

        if return_dict['trade']:
            return_dict['side'] = [
                return_dict[item]['side'] for item in (
                    'bullish-divergence', 'bearish-divergence'
                ) if return_dict[item]['flag']
            ][0]
        return return_dict

    @pysnooper.snoop()
    def strategy_macd(self, *args, **kwargs):
        '''
        [ STRATEGY ]: Moving Average Convergence Divergence

        [ NOTE ]: When to buy? Glad you asked!
                  When a Bullish Crossover occurs (when MACD crosses above its
                  signal line following a brief downside correction within a
                  long-term uptrend)

                  or when a Bullish Divergence occurs (when MACD makes two rising
                  lows corresponding with two falling lows in the price).

        [ NOTE ]: When to sell?... well ok, guess we're doing this now -
                  When a Bearish Crossover occurs (when MACD crosses below it's
                  signal line following a brief move higher withing a long-term
                  downtrend)

                  or when a Bearish Divergence occurs (when MACD forms a series
                  of two falling highs that correspond with two rising highs in
                  the price).

        [ NOTE ]: A Bearish Divergence that appears during a long-term bearish
                  trend is considered confirmation that the trend is likely to
                  continue.

        [ INPUT ]:
        [ RETURN ]:
        '''
        log.debug('')
        return_dict = {
            'bullish-crossover': self.check_macd_bullish_crossover(*args, **kwargs),
            'bearish-crossover': self.check_macd_bearish_crossover(*args, **kwargs),
            'bullish-divergence': self.check_macd_bullish_divergence(*args, **kwargs),
            'bearish-divergence': self.check_macd_bearish_divergence(*args, **kwargs),
            'interval': kwargs.get('macd-interval', kwargs.get('interval')),
            'period': kwargs.get('macd-period', kwargs.get('period')),
            'risk': 0,
            'trade': False,
            'side': '',
            'description': 'Moving Average Convergence Divergence Strategy',
        }

        if return_dict['bullish-crossover']['flag']:
            stdout_msg('MACD Bullish Crossover detected!')
        elif return_dict['bearish-crossover']['flag']:
            stdout_msg('MACD Bearish Crossover detected!')

        if return_dict['bullish-divergence']['flag']:
            stdout_msg('MACD Bullish Divergence detected!')
        elif return_dict['bearish-divergence']['flag']:
            stdout_msg('MACD Bearish Divergence detected!')

        return_dict['risk'] = self.compute_macd_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = True if True in [
            return_dict[label]['flag'] for label in (
                'bullish-crossover', 'bearish-crossover',
                'bullish-divergence', 'bearish-divergence',
            )
        ] else False

        if return_dict['trade']:
            return_dict['side'] = [
                return_dict[item]['side'] for item in (
                    'bullish-crossover', 'bearish-crossover',
                    'bullish-divergence', 'bearish-divergence'
                ) if return_dict[item]['flag']
            ][0]
        return return_dict

    def strategy_adx(self, *args, **kwargs):
        '''
        [ STRATEGY ]: Average Directional Index

        [ NOTE ]: When a Bullish Crossover occurs (when the ADX line is above
                  25 and the +DI line moves upward, which is from below to above
                  the -DI line), we must buy at the next candle after the
                  Crossover and place the stop-loss lower than the previous candle.

        [ NOTE ]: When a Bearish Crossover occurs (when the ADX line is above 25
                  and the +DI line moves downward, which is from above to below
                  the -DI line), we must sell at the next candle after the
                  Crossover and place the stop-loss higher than the previous candle.

        [ INPUT ]:
        [ RETURN ]:
        '''
        log.debug('')
        return_dict = {
            'bullish-crossover': self.check_adx_bullish_crossover(*args, **kwargs),
            'bearish-crossover': self.check_adx_bearish_crossover(*args, **kwargs),
            'interval': kwargs.get('adx-interval', kwargs.get('interval')),
            'period': kwargs.get('adx-period', kwargs.get('period')),
            'risk': 0,
            'trade': False,
            'description': 'Average Directional Index Strategy',
        }
        if return_dict['bullish-crossover']['flag']:
            stdout_msg(
                'ADX Bullish Crossover detected! Triggered when ADX is above '
                '{} and +DI goes from bellow to above -DI.'
                .format(self.adx_bottom),  ok=True
            )
        elif return_dict['bearish-crossover']['flag']:
            stdout_msg(
                'ADX Bearish Crossover detected! Triggered when ADX is above '
                '{} and +DI goes from above to below -DI. '
                .format(self.adx_bottom),
                ok=True
            )
        return_dict['risk'] = self.compute_adx_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = True if check_majority_in_set(True, [
            return_dict['bullish-crossover']['flag'],
            return_dict['bearish-crossover']['flag'],
        ]) else False
        if return_dict['trade']:
            return_dict['side'] = [
                return_dict[item]['side'] for item in (
                    'bullish-crossover', 'bearish-crossover'
                ) if return_dict[item]['flag']
            ][0]
        return return_dict

    def strategy_volume(self, *args, **kwargs):
        '''
        [ STRATEGY ]: Trading Volume
        [ NOTE ]: A large volume movement upwards can validate a large price
                  movement either side.
        [ INPUT ]:
        [ RETURN ]: {
            'volume-movement': {flag: True, ...},
            'interval': '1h',
            'period': 14,
            'value': 20903.77,
            'risk': 3,
            'side': 'buy',
            'trade': True,
            'description': 'Volume Strategy',
        }
        '''
        log.debug('')
        return_dict = {
            'volume-movement': self.check_large_volume_movement(*args, **kwargs),
            'interval': kwargs.get('volume-interval', kwargs.get('interval')),
            'period': kwargs.get('volume-period', kwargs.get('period')),
            'value': kwargs.get('volume'),
            'risk': 0,
            'side': '',
            'trade': False,
            'description': 'Volume Strategy',
        }
        return_dict['risk'] = self.compute_volume_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = False if return_dict['risk'] \
            > self.risk_tolerance or return_dict['risk'] == 0 else True
        return_dict['side'] = '' if not return_dict['trade'] \
            else return_dict['volume-movement']['side']
        return return_dict

    @pysnooper.snoop()
    def strategy_price(self, *args, **kwargs):
        '''
        [ STRATEGY ]: Price Action

        [ NOTE ]: Generates weak buy signal when it detects a large price
                  movement up, and a sell signal when it detects a large price
                  movement down. The signal is strengthened when the price
                  movement is confirmed by a large volume movement up.

        [ INPUT ]: kwargs[details] {
            'ticker-symbol': 'BTC/USDT',
            'buy-price': 20903.77,
            'sell-price': 20904.5,
            'volume': 7270.56273,
            'indicators': {
                'adx': 25.79249660682844,
                'macd': -55.08962670456458,
                'macd-signal': -18.088430567653305,
                'macd-hist': -37.001196136911275,
                'ma': 21216.220666666643,
                'ema': 21216.220700066643,
                'rsi': 25.931456303405913,
                'vwap': 20592.650164735693
            },
            'history': {
                'price-support': 1234,
                'price-resistance': 1235,
                'price': [{'value': 1234, backtrack: 1}, ...],
                'volume': [{'value': 1234, backtrack: 1}, ...],
                "adx": [{'value': 1234, backtrack: 1}, ...],
                "+di": [{'value': 1234, backtrack: 1}, ...],
                "-di": [{'value': 1234, backtrack: 1}, ...],
                'macd': [{'value': 1234, backtrack: 1}, ...],
                'macd-signal': [{'value': 1234, backtrack: 1}, ...],
                'macd-hist': [{'value': 1234, backtrack: 1}, ...],
                'ma': [{'value': 1234, backtrack: 1}, ...],
                'ema': [{'value': 1234, backtrack: 1}, ...],
                'rsi': [{'value': 1234, backtrack: 1}, ...],
                'vwap': [{'value': 1234, backtrack: 1}, ...],
            }
        }

        [ RETURN ]: {
            'price-movement': {flag: True, ...},
            'confirmed-by-volume': {flag: True, volume: {flag: ...}},
            'interval': '1h',
            'period': 14,
            'value': 20903.77,
            'risk': 3,
            'side': 'buy',
            'trade': True,
            'description': 'Price Action Strategy',
        }
        '''
        log.debug('')
        return_dict = {
            'price-movement': self.check_large_price_movement(*args, **kwargs),
            'confirmed-by-volume': {},
            'interval': kwargs.get('price-interval', kwargs.get('interval')),
            'period': kwargs.get('price-period', kwargs.get('period')),
            'value': kwargs.get('details', {}).get('sell-price') \
                if kwargs.get('side') == 'sell' \
                else kwargs.get('details', {}).get('buy-price'),
            'risk': 0,
            'side': '',
            'trade': False,
            'description': 'Price Action Strategy',
        }
        if return_dict['price-movement']['flag']:
            stdout_msg(
                'Large {}% price movement detected! Triggered over {}%'.format(
                    move_percent, price_movement
                ), ok=True
            )
            details = kwargs.copy()
            details.update({
                'volume-period': kwargs.get('price-period', kwargs.get('period')),
                'volume-interval': kwargs.get('price-interval', kwargs.get('interval')),
            })
            return_dict['confirmed-by-volume'] = \
                self.check_price_movement_confirmed_by_volume(
                    return_dict['price-movement'], **details
                )
        if return_dict['confirmed-by-volume'] and \
                not return_dict['confirmed-by-volume'].get('error'):
            if return_dict['confirmed-by-volume'].get('flag'):
                stdout_msg(
                    'Large {}% volume movement detected! Triggered over {}%\n'
                    'Price movement validated by volume!'.format(
                        return_dict['confirmed-by-volume'].get('moved-percentage'),
                        return_dict['confirmed-by-volume'].get('trigger-percentage')
                    ), ok=True
                )
        return_dict['risk'] = self.compute_price_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = False if return_dict['risk'] \
            > self.risk_tolerance or return_dict['risk'] == 0 else True
        return_dict['side'] = '' if not return_dict['trade'] \
            else return_dict['price-movement']['side']
        return return_dict


# CODE DUMP

#       details = kwargs['details']['history']
#       adx_top = float(kwargs.get('adx-top', self.adx_top))
#       adx_bottom = float(kwargs.get('adx-bottom', self.adx_bottom))
#       adx_values = {
#           'adx': [ float(details['adx'][index]['adx'])
#                   for index in range(len(details['adx'])) ],
#           '+di': [ float(details['adx'][index]['plusdi'])
#                   for index in range(len(details['adx'])) ],
#           '-di': [ float(details['adx'][index]['minusdi'])
#                   for index in range(len(details['adx'])) ],
#       }
#       scan = scan_value_sets(
#           adx_values['+di'], adx_values['-di'], look_for='crossover'
#       )
#       return_dict = {
#           'flag': False, #scan.get('flag', False),
#           'start-candle': details['adx'][len(details['adx'])-1]['backtrack'],
#           'stop-candle': details['adx'][0]['backtrack'],
#           'side': 'sell' if scan['flag'] else '',
#           'values': adx_values,
#           'scan': scan,
#       }



#{'flag': True, 'start1': 9, 'start2': 1, 'end1': 2, 'end2': 8, 'crossovers': [4], 'confirmed': True}

#       period_volume_avg = sum(volume_values) / len(volume_values)
#       min_val, max_val = min(volume_values), max(volume_values)
#       min_candle = [
#           item for item in details['volume']
#           if float(item['value']) == float(min_val)
#       ]
#       if min_candle:
#           min_candle = min_candle[0]['backtrack']
#       max_candle = [
#           item for item in details['volume']
#           if float(item['value']) == float(max_val)
#       ]
#       if max_candle:
#           max_candle = max_candle[0]['backtrack']
#       movement = max_val - min_val
#       move_percent = compute_percentage_of(movement, period_volume_avg)
#       return_dict = {
#           'flag': True if move_percent >= volume_movement else False,
#           'start-value': volume_values[-1],
#           'stop-value': volume_values[0],
#           'min-value': min_val,
#           'max-value': max_val,
#           'period-average': period_volume_avg,
#           'start-candle': details['volume'][len(volume_values)-1]['backtrack'],
#           'stop-candle': details['volume'][0]['backtrack'],
#           'min-candle': min_candle or None,
#           'max-candle': max_candle or None,
#           'side': '',
#           'moved': movement,
#           'moved-percentage': move_percent,
#           'trigger-percentage': volume_movement,
#       }
#       return {}


#           'buy' if return_dict['bullish-crossover']['flag'] \
#               else 'sell' if return_dict['bearish-crossover']['flag']
#       False if \
#           not (return_dict['bullish-crossover'] \
#                and return_dict['bearish-crossover']) \
#           or return_dict['risk'] > self.risk_tolerance \
#           or return_dict['risk'] == 0 else True


        # TODO - Research how to trade ADX
#       return_dict = {
#           'interval': kwargs.get('adx-interval', kwargs.get('interval')),
#           'period': kwargs.get('adx-period', kwargs.get('period')),
#           'value': kwargs.get('adx'),
#           'risk': 0,
#           'trade': False,
#           'description': 'Volume Strategy',
#       }
#       return_dict['risk'] = self.compute_adx_trade_risk(return_dict, **kwargs)
#       return_dict['trade'] = False if return_dict['risk'] \
#           > self.risk_tolerance or return_dict['risk'] == 0 else True
#       return return_dict

#       stdout_msg(
#           '\nStrategy Price {}'.format(pretty_dict_print(return_dict)),
#           red=False if return_dict['trade'] else True,
#           green=False if not return_dict['trade'] else True,
#       )



#           5: self.evaluate_high_risk_tolerance,
#       }
#       base_evaluators = {
#           'buy': self.evaluate_buy,
#           'sell': self.evaluate_sell,
#       }



#       trade_flag, risk_index, trade_side = False, 0, kwargs.get('side', 'auto')
#       if not self.base_evaluators:
#           return False
#       if trade_side == 'auto':
#           buy_flag, buy_risk = self.base_evaluators['buy'](
#               evaluations_dict, **kwargs
#           )
#           sell_flag, sell_risk = self.base_evaluators['sell'](
#               evaluations_dict, **kwargs
#           )
#           if buy_flag:
#               trade_flag, trade_side, risk_index = buy_flag, 'buy', buy_risk
#           elif sell_flag:
#               trade_flag, trade_side, risk_index = sell_flag, 'sell', sell_risk
#       else:
#           trade_flag, risk_index = self.base_evaluators[trade_side](
#               evaluations_dict, **kwargs
#           )
#       return trade_flag if risk_index <= 4 else False, risk_index, trade_side


#       trade_flag, risk_index, trade_side = False, 0, kwargs.get('side', 'auto')
#       if not self.base_evaluators:
#           return False
#       if trade_side == 'auto':
#           buy_flag, buy_risk = self.base_evaluators['buy'](
#               evaluations_dict, **kwargs
#           )
#           sell_flag, sell_risk = self.base_evaluators['sell'](
#               evaluations_dict, **kwargs
#           )
#           if buy_flag:
#               trade_flag, trade_side, risk_index = buy_flag, 'buy', buy_risk
#           elif sell_flag:
#               trade_flag, trade_side, risk_index = sell_flag, 'sell', sell_risk
#       else:
#           trade_flag, risk_index = self.base_evaluators[trade_side](
#               evaluations_dict, **kwargs
#           )
#       return trade_flag, risk_index, trade_side

