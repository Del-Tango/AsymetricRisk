import unittest
import time
import json

from src.ar_strategy import TradingStrategy


class TestARStrategyAnalyzer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.analyzer = TradingStrategy(**{'risk-tolerance': 5})
        cls.strategy = 'vwap,rsi,macd,ema,ma,adx,volume,price'
        cls.side = 'auto'
        cls.analyzer_details = cls.format_risk_analyzer_mock_details()
        cls.evaluator_details = cls.format_evaluator_mock_details()
        cls.evaluator_kwargs = cls.format_evaluator_kwargs()

    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def format_risk_analyzer_mock_details(cls):
        return {
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
                'adx': [
                    {'value': 25.79249660682844, 'backtrack': 1},
                    {'value': 25.79249660682844, 'backtrack': 2}
                ],
                'macd': [
                    {'value': -55.08962670456458, 'backtrack': 1},
                    {'value': -55.08962670456458, 'backtrack': 2}
                ],
                'macd-signal': [
                    {'value': -18.088430567653305, 'backtrack': 1},
                    {'value': -18.088430567653305, 'backtrack': 2}
                ],
                'macd-hist': [
                    {'value': -37.001196136911275, 'backtrack': 1},
                    {'value': -37.001196136911275, 'backtrack': 2}
                ],
                'ma': [
                    {'value': 21216.220666666643, 'backtrack': 1},
                    {'value': 21216.220666666643, 'backtrack': 2}
                ],
                'ema': [
                    {'value': 21216.220700066643, 'backtrack': 1},
                    {'value': 21216.220700066643, 'backtrack': 2}
                ],
                'rsi': [
                    {'value': 25.931456303405913, 'backtrack': 1},
                    {'value': 25.931456303405913, 'backtrack': 2}
                ],
                'vwap': [
                    {'value': 20592.650164735693, 'backtrack': 1},
                    {'value': 20592.650164735693, 'backtrack': 2}
                ],
                'buy-price': [
                    {'value': 20903.77, 'backtrack': 1},
                    {'value': 20903.77, 'backtrack': 2}
                ],
                'sell-price': [
                    {'value': 20904.5, 'backtrack': 1},
                    {'value': 20904.5, 'backtrack': 2}
                ],
                'volume': [
                    {'value': 7270.56273, 'backtrack': 1},
                    {'value': 7270.56273, 'backtrack': 2}
                ],
            }
        }

    @classmethod
    def format_evaluator_mock_details(cls):
        return {
            'buy-price': {
                'price-movement': {
                    'flag': True, 'start-value': 20603.77, 'stop-value': 20903.77
                },
                'confirmed-by-volume': {
                    'flag': True, 'start-value': 7100.56273, 'stop-value': 7270.56273
                },
                'interval': '1h',
                'value': 20903.77,
                'risk': 0,
                'trade': True,
                'description': 'Price Action Strategy',
            },
            'sell-price': {
                'price-movement': {
                    'flag': False, 'start-value': 20603.77, 'stop-value': 20903.77
                },
                'confirmed-by-volume': {
                    'flag': False, 'start-value': 7100.56273, 'stop-value': 7270.56273
                },
                'interval': '1h',
                'value': 20903.77,
                'risk': 0,
                'trade': False,
                'description': 'Price Action Strategy',
            },
        }

    @classmethod
    def format_evaluator_kwargs(cls):
        return {
            'strategy': cls.strategy,
            'side': cls.side,
            'details': cls.analyzer_details or cls.format_risk_analyzer_mock_details()
        }

    def new_strategy(self, *args, **kwargs):
        return {
            'error': False,
        }

    def test_load_strategy(self):
        load = self.analyzer.load_strategy(**{'new': self.new_strategy})
        self.assertTrue(load)
        self.assertTrue(isinstance(load, dict))
        self.assertFalse(load.get('error', False))
        self.assertTrue(self.analyzer.strategies.get('new', False))

    def test_set_risk_tolerance(self):
        set_risk = self.analyzer.set_risk_tolerance(1)
        self.assertTrue(set_risk)
        self.assertTrue(isinstance(set_risk, int))

    def test_analyze_risk(self):
        trade_flag, risk_index, trade_side, exit_code = self.analyzer.analyze_risk(
            **self.evaluator_kwargs
        )
        self.assertTrue(isinstance(trade_flag, bool))
        self.assertTrue(isinstance(risk_index, int))
        self.assertTrue(isinstance(trade_side, str))
        self.assertEquals(exit_code, 0)

    def test_evaluate_high_risk_tolerance(self):
        trade_flag, risk_index, trade_side = self.analyzer.evaluate_high_risk_tolerance(
            self.evaluator_details, **self.evaluator_kwargs
        )
        self.assertTrue(isinstance(trade_flag, bool))
        self.assertTrue(isinstance(risk_index, int))
        self.assertTrue(isinstance(trade_side, str))

    def test_evaluate_mid_high_risk_tolerance(self):
        trade_flag, risk_index, trade_side = self.analyzer.evaluate_mid_high_risk_tolerance(
            self.evaluator_details, **self.evaluator_kwargs
        )
        self.assertTrue(isinstance(trade_flag, bool))
        self.assertTrue(isinstance(risk_index, int))
        self.assertTrue(isinstance(trade_side, str))

    def test_evaluate_mid_risk_tolerance(self):
        trade_flag, risk_index, trade_side = self.analyzer.evaluate_mid_risk_tolerance(
            self.evaluator_details, **self.evaluator_kwargs
        )
        self.assertTrue(isinstance(trade_flag, bool))
        self.assertTrue(isinstance(risk_index, int))
        self.assertTrue(isinstance(trade_side, str))

    def test_evaluate_low_mid_risk_tolerance(self):
        trade_flag, risk_index, trade_side = self.analyzer.evaluate_low_mid_risk_tolerance(
            self.evaluator_details, **self.evaluator_kwargs
        )
        self.assertTrue(isinstance(trade_flag, bool))
        self.assertTrue(isinstance(risk_index, int))
        self.assertTrue(isinstance(trade_side, str))

    def test_evaluate_low_risk_tolerance(self):
        trade_flag, risk_index, trade_side = self.analyzer.evaluate_low_risk_tolerance(
            self.evaluator_details, **self.evaluator_kwargs
        )
        self.assertTrue(isinstance(trade_flag, bool))
        self.assertTrue(isinstance(risk_index, int))
        self.assertTrue(isinstance(trade_side, str))

    # TODO
    def test_strategy_vwap(self):
        pass
    def test_strategy_rsi(self):
        pass
    def test_strategy_macd(self):
        pass
    def test_strategy_ma(self):
        pass
    def test_strategy_ema(self):
        pass
    def test_strategy_adx(self):
        pass
    def test_strategy_volume(self):
        pass


    def test_strategy_price(self):
        mock_details = self.format_risk_analyzer_mock_details()
        buy_strategy = self.analyzer.strategy_price(
            side='buy', **mock_details
        )
        self.assertTrue(buy_strategy)
        self.assertTrue(isinstance(buy_strategy, dict))
        self.assertFalse(buy_strategy.get('error', False))

        sell_strategy = self.analyzer.strategy_price(
            side='sell', **mock_details
        )
        self.assertTrue(sell_strategy)
        self.assertTrue(isinstance(sell_strategy, dict))
        self.assertFalse(sell_strategy.get('error', False))

        auto_strategy = self.analyzer.strategy_price(
            side='auto', **mock_details
        )
        self.assertTrue(auto_strategy)
        self.assertTrue(isinstance(auto_strategy, dict))
        self.assertFalse(auto_strategy.get('error', False))




# CODE DUMP

#   strategy_x

#       return {
#           'price-movement': {flag: True, start-value: , stop-value},
#           'confirmed-by-volume': {flag: True, start-value: , stop-value},
#           'interval': '1h',
#           'value': 20903.77,
#           'risk': 0,
#           'trade': True,
#           'description': 'Price Action Strategy',
#       }
