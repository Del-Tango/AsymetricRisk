#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADING BOT

import logging
import pysnooper
import pprint

from src.backpack.bp_general import stdout_msg, pretty_dict_print
from src.backpack.bp_computers import compute_percentage, compute_percentage_of

log = logging.getLogger('AsymetricRisk')


class TradingStrategy():

    def __init__(self, *args, **kwargs):
        log.debug('')
        self.risk_tolerance = kwargs.get('risk-tolerance', 1) # less-risk 1, 2, 3, 4, 5 more-risk
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

    @pysnooper.snoop()
    def check_price_movement_confirmed_by_volume(self, price_dict, **kwargs):
        log.debug('')
        check_volume = self.check_large_volume_movement(**kwargs)
        # check_price = self.check_large_price_movement(*args, **kwargs)
        return_dict = {
            'flag': False if not price_dict['flag'] else check_volume['flag'],
            'volume': check_volume,
        }
        if not return_dict['flag']:
            if price_dict['flag']:
                log.debug(
                    'Large price movement was not confirmed by volume movement.'
                )
        else:
            log.debug('Large price movement confirmed by large volume movement!',)
        return return_dict

    @pysnooper.snoop()
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
            'start-candle': details['volume'][len(volume_values) - 1]['backtrack'],
            'stop-candle': details['volume'][0]['backtrack'],
            'min-candle-index': min_candle or None,
            'max-candle-index': max_candle or None,
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
                'No large volume movement occured over period. Moved by {}%'.format(
                    move_percent
                )
            )
        return return_dict

    @pysnooper.snoop()
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
            'start-candle': details['price'][len(price_values) - 1]['backtrack'],
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
                'No large price movement occured over period. Moved by {}%'.format(
                    move_percent
                )
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

#       stdout_msg(
#           '\nStrategy Price {}'.format(),
#           red=False if return_dict['trade'] else True,
#           green=False if not return_dict['trade'] else True,
#       )

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
    def compute_trade_flag(self, evaluations_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_risk_index(self, evaluations_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_adx_trade_risk(self, return_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_volume_trade_risk(self, return_dict, **kwargs):
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
        '''
        log.debug('TODO - Under construction, building...')
        return 0

    # EVALUATORS

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
            stdout_msg('[ ERROR ]: Necessary data set for risk evaluation not found!')
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
    def strategy_vwap(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
        # TODO - Research
    def strategy_rsi(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
        # TODO - Research
    def strategy_macd(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
        # TODO - Research
    def strategy_ma(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
        # TODO - Research
    def strategy_ema(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
        # TODO - Research
    def strategy_adx(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
        # TODO - Research how to trade ADX
        return_dict = {
            'interval': kwargs.get('adx-interval', kwargs.get('interval')),
            'period': kwargs.get('adx-period', kwargs.get('period')),
            'value': kwargs.get('adx'),
            'risk': 0,
            'trade': False,
            'description': 'Volume Strategy',
        }
        return_dict['risk'] = self.compute_adx_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = False if return_dict['risk'] \
            > self.risk_tolerance else True
        return return_dict


    def strategy_volume(self, *args, **kwargs):
        '''
        [ RETURN ]: {
            'volume-movement': {flag: True, ...},
            'interval': '1h',
            'period': 14,
            'value': 20903.77,
            'risk': 0,
            'trade': True,
            'description': 'Price Action Strategy',
        }
        '''
        log.debug('')
        return_dict = {
            'volume-movement': self.check_large_volume_movement(*args, **kwargs),
            'interval': kwargs.get('volume-interval', kwargs.get('interval')),
            'period': kwargs.get('volume-period', kwargs.get('period')),
            'value': kwargs.get('volume'),
            'risk': 0,
            'trade': False,
            'description': 'Volume Strategy',
        }
        return_dict['risk'] = self.compute_volume_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = False if return_dict['risk'] \
            > self.risk_tolerance else True
        return return_dict

    @pysnooper.snoop()
    def strategy_price(self, *args, **kwargs):
        '''
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
                'adx': [{'value': 1234, backtrack: 1}, ...],
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
            'price-movement': {flag: True, start-value: , stop-value},
            'confirmed-by-volume': {flag: True, volume: {flag: ...}},
            'interval': '1h',
            'period': 14,
            'value': 20903.77,
            'risk': 0,
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
            'trade': False,
            'description': 'Price Action Strategy',
        }
        if return_dict['price-movement']['flag']:
            stdout_msg(
                'Large {}% price movement detected! Triggered over {}%'.format(
                    move_percent, price_movement
                ), ok=True
            )
            return_dict['confirmed-by-volume'] = \
                self.check_price_movement_confirmed_by_volume(
                    return_dict['price-movement'], **kwargs
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

        # TODO
        return_dict['risk'] = self.compute_price_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = False if return_dict['risk'] \
            > self.risk_tolerance else True
        return return_dict


# CODE DUMP

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

