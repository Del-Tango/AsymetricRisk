#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADING BOT

import logging

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

    # TODO
    def check_large_price_movement(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
    def check_large_volume_movement(*args, **kwargs):
        log.debug('TODO - Under construction, building...')
    def check_price_movement_confirmed_by_volume(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')

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

    def analyze_risk(self, strategy='vwap', side='auto', **kwargs):
        log.debug('')
        failures = 0
        trade_flag, risk_index, trade_side, evaluations = False, 0, side, {}
        for strategy_label in strategy.split(','):
            if strategy_label not in self.strategies:
                failures += 1
                continue
            evaluations[strategy_label] = self.strategies[strategy_label](**kwargs)
        trade_flag, risk_index, trade_side = self.risk_evaluators[self.risk_tolerance](
            evaluations, side=side, details=kwargs.get('details', {})
        )
        return trade_flag, risk_index, trade_side, failures

    # COMPUTERS

    # TODO
    def compute_volume_trade_risk(self, return_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0
    def compute_price_trade_risk(self, return_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return 0

    # EVALUATORS

    # TODO
    def compute_trade_flag(self, evaluations_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
    def compute_risk_index(self, evaluations_dict, **kwargs):
        log.debug('TODO - Under construction, building...')

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
            'buy-price': {value: , interval: , risk: , trade: , description: },
            'sell-price': {value: , interval: , risk: , trade: , description: },
            'volume': {value: , interval: , risk: , trade: , description: },
            ...
        }
        '''
        log.debug('TODO - Under construction, building...')
        if not evaluations_dict:
            return False
        trade_flag, risk_index = False, 0
        risk_values = [
            int(evaluations_dict[indicator_label]['risk'])
            for indicator_label in evaluations_dict
        ]
        risk_index = sum(risk_values) / len(risk_values)
        trade_flag = True if risk_index <= self.risk_tolerance \
            and risk_index != 0 else False
        return trade_flag, risk_index
    def evaluate_buy(self, evaluations_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return self.evaluate_risk(evaluations_dict, **kwargs)
#       if not evaluations_dict:
#           return False
#       trade_flag, risk_index = False, 0
#       return trade_flag, risk_index
    def evaluate_sell(self, evaluations_dict, **kwargs):
        log.debug('TODO - Under construction, building...')
        return self.evaluate_risk(evaluations_dict, **kwargs)
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
        # return {value: 2435.897674764, interval: 5m, risk: 3, trade: False, description: VWAP}
    def strategy_rsi(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
    def strategy_macd(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
    def strategy_ma(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
    def strategy_ema(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
    def strategy_adx(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
        return_dict = {
#           'volume-movement': self.check_large_volume_movement(*args, **kwargs),
            'interval': kwargs.get('interval'),
            'value': kwargs.get('volume'),
            'risk': 0,
            'trade': False,
            'description': 'Volume Strategy',
        }
        return_dict['risk'] = self.compute_volume_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = False if return_dict['risk'] \
            > self.risk_tolerance else True
        return return_dict


    def strategy_volume(self, *args, **kwargs):
        log.debug('')
        return_dict = {
            'volume-movement': self.check_large_volume_movement(*args, **kwargs),
            'interval': kwargs.get('interval'),
            'value': kwargs.get('volume'),
            'risk': 0,
            'trade': False,
            'description': 'Volume Strategy',
        }
        return_dict['risk'] = self.compute_volume_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = False if return_dict['risk'] \
            > self.risk_tolerance else True
        return return_dict

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
                'adx': [{'value': 1234, backtrack: 1}, ...],
                'macd': [{'value': 1234, backtrack: 1}, ...],
                'macd-signal': [{'value': 1234, backtrack: 1}, ...],
                'macd-hist': [{'value': 1234, backtrack: 1}, ...],
                'ma': [{'value': 1234, backtrack: 1}, ...],
                'ema': [{'value': 1234, backtrack: 1}, ...],
                'rsi': [{'value': 1234, backtrack: 1}, ...],
                'vwap': [{'value': 1234, backtrack: 1}, ...],
                'buy-price': [{'value': 1234, backtrack: 1}, ...],
                'sell-price': [{'value': 1234, backtrack: 1}, ...],
                'volume': [{'value': 1234, backtrack: 1}, ...],
            }
        }

        [ RETURN ]: {
            'price-movement': {flag: True, start-value: , stop-value},
            'confirmed-by-volume': {flag: True, start-value: , stop-value},
            'interval': '1h',
            'value': 20903.77,
            'risk': 0,
            'trade': True,
            'description': 'Price Action Strategy',
        }

        '''
        log.debug('')
        return_dict = {
            'price-movement': self.check_large_price_movement(*args, **kwargs),
            'confirmed-by-volume': self.check_price_movement_confirmed_by_volume(
                *args, **kwargs
            ),
            'interval': kwargs.get('interval'),
            'value': kwargs.get('details', {}).get('sell-price') \
                if kwargs.get('side') == 'sell' \
                else kwargs.get('details', {}).get('buy-price'),
            'risk': 0,
            'trade': False,
            'description': 'Price Action Strategy',
        }
        return_dict['risk'] = self.compute_price_trade_risk(return_dict, **kwargs)
        return_dict['trade'] = False if return_dict['risk'] \
            > self.risk_tolerance else True
        return return_dict


# CODE DUMP

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

