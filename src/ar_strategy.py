#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADING BOT

import logging

log = logging.getLogger('AsymetricRisk')


class TradingStrategy():

    # TODO
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

    # FETCHERS

    # SETTERS

    def set_risk_tolerance(self, risk_index):
        log.debug('')
        if risk_index > 5 or risk_index < 0:
            return False
        self.risk_tolerance = risk_index
        return self.risk_tolerance

    # GENERAL

    def load_strategy(self, **kwargs):
        log.debug('')
        if not kwargs:
            return False
        self.strategies.update(kwargs)
        return self.strategies

    # ACTIONS

    # TODO
    def evaluate_buy(self, evaluations_dict, **kwargs):
        log.debug('')
#       trade_flag, risk_index, trade_side = False, 0, kwargs.get('side', 'auto')
#       return trade_flag, risk_index
    def evaluate_sell(self, evaluations_dict, **kwargs):
        log.debug('')
#       trade_flag, risk_index, trade_side = False, 0, kwargs.get('side', 'auto')
#       return trade_flag, risk_index
    def evaluate_low_risk_tolerance(self, evaluations_dict, **kwargs):
        log.debug('')
#       trade_flag, risk_index, trade_side = False, 0, kwargs.get('side', 'auto')
#       if not kwargs.get('evaluators'):
#           return False
#       if trade_side == 'auto':
#           buy_flag, buy_risk = kwargs['evaluators']['buy'](evaluations_dict, **kwargs)
#           sell_flag, sell_risk = kwargs['evaluators']['sell'](evaluations_dict, **kwargs)
#           if buy_flag:
#               trade_flag, trade_side, risk_index = buy_flag, 'buy', buy_risk
#           elif sell_flag:
#               trade_flag, trade_side, risk_index = sell_flag, 'sell', sell_risk
#       else:
#           trade_flag, risk_index = kwargs['evaluators'][trade_side](evaluations_dict, **kwargs)
#       return trade_flag, risk_index, trade_side
    def evaluate_low_mid_risk_tolerance(self, evaluations_dict, **kwargs):
        log.debug('')
#       trade_flag, risk_index, trade_side = False, 0, kwargs.get('side', 'auto')
#       if not kwargs.get('evaluators'):
#           return False
#       if trade_side == 'auto':
#           buy_flag, buy_risk = kwargs['evaluators']['buy'](evaluations_dict, **kwargs)
#           sell_flag, sell_risk = kwargs['evaluators']['sell'](evaluations_dict, **kwargs)
#           if buy_flag:
#               trade_flag, trade_side, risk_index = buy_flag, 'buy', buy_risk
#           elif sell_flag:
#               trade_flag, trade_side, risk_index = sell_flag, 'sell', sell_risk
#       else:
#           trade_flag, risk_index = kwargs['evaluators'][trade_side](evaluations_dict, **kwargs)
#       return trade_flag, risk_index, trade_side
    def evaluate_mid_risk_tolerance(self, evaluations_dict, **kwargs):
        log.debug('')
#       trade_flag, risk_index, trade_side = False, 0, kwargs.get('side', 'auto')
#       if not kwargs.get('evaluators'):
#           return False
#       if trade_side == 'auto':
#           buy_flag, buy_risk = kwargs['evaluators']['buy'](evaluations_dict, **kwargs)
#           sell_flag, sell_risk = kwargs['evaluators']['sell'](evaluations_dict, **kwargs)
#           if buy_flag:
#               trade_flag, trade_side, risk_index = buy_flag, 'buy', buy_risk
#           elif sell_flag:
#               trade_flag, trade_side, risk_index = sell_flag, 'sell', sell_risk
#       else:
#           trade_flag, risk_index = kwargs['evaluators'][trade_side](evaluations_dict, **kwargs)
#       return trade_flag, risk_index, trade_side
    def evaluate_mid_high_risk_tolerance(self, evaluations_dict, **kwargs):
        log.debug('')
#       trade_flag, risk_index, trade_side = False, 0, kwargs.get('side', 'auto')
#       if not kwargs.get('evaluators'):
#           return False
#       if trade_side == 'auto':
#           buy_flag, buy_risk = kwargs['evaluators']['buy'](evaluations_dict, **kwargs)
#           sell_flag, sell_risk = kwargs['evaluators']['sell'](evaluations_dict, **kwargs)
#           if buy_flag:
#               trade_flag, trade_side, risk_index = buy_flag, 'buy', buy_risk
#           elif sell_flag:
#               trade_flag, trade_side, risk_index = sell_flag, 'sell', sell_risk
#       else:
#           trade_flag, risk_index = kwargs['evaluators'][trade_side](evaluations_dict, **kwargs)
#       return trade_flag, risk_index, trade_side

    def evaluate_high_risk_tolerance(self, evaluations_dict, **kwargs):
        log.debug('')
        trade_flag, risk_index, trade_side = False, 0, kwargs.get('side', 'auto')
        if not kwargs.get('evaluators'):
            return False
        if trade_side == 'auto':
            buy_flag, buy_risk = kwargs['evaluators']['buy'](evaluations_dict, **kwargs)
            sell_flag, sell_risk = kwargs['evaluators']['sell'](evaluations_dict, **kwargs)
            if buy_flag:
                trade_flag, trade_side, risk_index = buy_flag, 'buy', buy_risk
            elif sell_flag:
                trade_flag, trade_side, risk_index = sell_flag, 'sell', sell_risk
        else:
            trade_flag, risk_index = kwargs['evaluators'][trade_side](evaluations_dict, **kwargs)
        return trade_flag, risk_index, trade_side

    def analyze_risk(self, strategy='vwap', side='auto', **kwargs):
        log.debug('')
        trade_flag, risk_index, trade_side, evaluations = False, 0, side, {}
        for strategy_label in strategy.split(','):
            if strategy_label not in self.strategies:
                continue
            evaluations[strategy_label] = self.strategies[strategy_label](**kwargs)
        risk_evaluators = {
            1: self.evaluate_low_risk_tolerance,
            2: self.evaluate_low_mid_risk_tolerance,
            3: self.evaluate_mid_risk_tolerance,
            4: self.evaluate_mid_high_risk_tolerance,
            5: self.evaluate_high_risk_tolerance,
        }
        base_evaluators = {
            'buy': self.evaluate_buy,
            'sell': self.evaluate_sell,
        }
        trade_flag, risk_index, trade_side = risk_evaluators[self.risk_tolerance](
            evaluations, side=side, evaluators=base_evaluators}
        )
        return trade_flag, risk_index, trade_side

    # STRATEGIES

    # TODO
    def strategy_vwap(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
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
    def strategy_volume(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
    def strategy_price(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
