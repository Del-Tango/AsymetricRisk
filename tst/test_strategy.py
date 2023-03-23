
import unittest
import os
import pysnooper

from src.ar_bot import (
    TradingMarket, TradingStrategy, Signal, PriceEvaluator, VolumeEvaluator,
    RSIEvaluator, MACDEvaluator, MAEvaluator, EMAEvaluator, ADXEvaluator,
    VWAPEvaluator
)
from src.backpack.bp_convertors import json2dict
from src.backpack.bp_general import stdout_msg, pretty_dict_print
from src.backpack.bp_computers import compute_percentage


class TestARStrategy(unittest.TestCase):

    conf_file = 'conf/asymetric_risk.conf.json' \
        if os.path.exists('conf/asymetric_risk.conf.json') else ''
    AR_DEFAULT = json2dict(conf_file)['AR_DEFAULT']
    if not AR_DEFAULT:
        context = {
            'ticker-symbol': 'XRP/USDT',
            'base-currency': 'XRP',
            'quote-currency': 'USDT',
            'taapi-url': 'https://api.taapi.io',
            'binance-url': 'https://testnet.binance.vision/api',
            'binance-key': os.environ.get('BINANCE_KEY'),
            'binance-secret': os.environ.get('BINANCE_SECRET'),
            'taapi-key': os.environ.get('TAAPI_KET'),
            'strategy': 'price,volume',
        }
    else:
        context = AR_DEFAULT
    binance_key = context.get('binance-key')
    binance_secret = context.get('binance-secret')
    taapi_key = context.get('taapi-key')
    trading_market = None
    market_data = {}
    strategy = None
    mock_evaluation_base_keys = [
        "interval", "period", "value", "risk", "side", "trade", "description",
    ]

    # PREREQUISITS

    @classmethod
    def setUpClass(cls):
        stdout_msg('\n[ TradingStrategy ]: Functional test suit -', bold=True)
        # TODO - Mock me wiggle
        cls.trading_market = TradingMarket(cls.binance_key, cls.binance_secret)
        cls.trading_market.setup()
        stdout_msg('\n[ SETUP ]: Scrape market data...', bold=True)
        cls.market_data = cls.trading_market.scan('all', **cls.context)
        cls.strategy = TradingStrategy(**cls.context)


    @classmethod
    def tearDownClass(cls):
        stdout_msg('\n[ DONE ]: TradingStrategy AutoTesters', bold=True)

    # MOCK
    # TODO - Mock market data

    # TESTERS

    def test_ar_strategy_evaluation_of_market_data(self):
        stdout_msg(
            '\n[ TEST ]: Evaluate market data and generate Signals...', bold=True
        )
        evaluation = self.strategy.evaluate(self.market_data, **self.context)
        self.assertTrue(isinstance(evaluation, list))
        self.assertTrue(evaluation)
        stdout_msg(f'Trading Signals: {evaluation}', ok=True)
        for signal in evaluation:
            stdout_msg('* ' + str(signal), green=True)

    def test_ar_strategy_price(self):
        stdout_msg('\n[ TEST ]: Price Action Strategy Evaluator...', bold=True)
        obj = PriceEvaluator(**self.context)
        evaluation = obj.evaluate(self.market_data, **self.context)
        self.assertTrue(evaluation)
        self.assertTrue(isinstance(evaluation, dict))
        self.assertTrue(evaluation.get('price-movement'))
        self.assertTrue(isinstance(evaluation['price-movement'], dict))
        for key in self.mock_evaluation_base_keys:
            if key not in evaluation:
                msg = f'Key not found! ({key})\nEvaluation: ' \
                    + str(pretty_dict_print(evaluation))
                stdout_msg(msg, nok=True)
                self.assertTrue(evaluation.get(key))
        stdout_msg('Evaluation: ' + str(pretty_dict_print(evaluation)), ok=True)

    def test_ar_strategy_volume(self):
        stdout_msg('\n[ TEST ]: Trading Volume Strategy Evaluator', bold=True)
        obj = VolumeEvaluator(**self.context)
        evaluation = obj.evaluate(self.market_data, **self.context)
        self.assertTrue(evaluation)
        self.assertTrue(isinstance(evaluation, dict))
        self.assertTrue(evaluation.get('volume-movement'))
        self.assertTrue(isinstance(evaluation['volume-movement'], dict))
        for key in self.mock_evaluation_base_keys:
            if key not in evaluation:
                msg = f'Key not found! ({key})\nEvaluation: ' \
                    + str(pretty_dict_print(evaluation))
                stdout_msg(msg, nok=True)
                self.assertTrue(evaluation.get(key))
        stdout_msg('Evaluation: ' + str(pretty_dict_print(evaluation)), ok=True)

    # TODO
    def test_ar_strategy_rsi(self):
        stdout_msg('\n[ TEST ]: ...', bold=True)
        obj = RSIEvaluator(**self.context)
#       evaluation = obj.evaluate(**self.market_data)
    def test_ar_strategy_ma(self):
        stdout_msg('\n[ TEST ]: ...', bold=True)
        obj = MAEvaluator(**self.context)
#       evaluation = obj.evaluate(**self.market_data)
    def test_ar_strategy_ema(self):
        stdout_msg('\n[ TEST ]: ...', bold=True)
        obj = EMAEvaluator(**self.context)
#       evaluation = obj.evaluate(**self.market_data)
    def test_ar_strategy_macd(self):
        stdout_msg('\n[ TEST ]: ...', bold=True)
        obj = MACDEvaluator(**self.context)
#       evaluation = obj.evaluate(**self.market_data)
    def test_ar_strategy_adx(self):
        stdout_msg('\n[ TEST ]: ...', bold=True)
        obj = ADXEvaluator(**self.context)
#       evaluation = obj.evaluate(**self.market_data)
    def test_ar_strategy_vwap(self):
        stdout_msg('\n[ TEST ]: ...', bold=True)
        obj = VWAPEvaluator(**self.context)
#       evaluation = obj.evaluate(**self.market_data)

