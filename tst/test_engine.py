import unittest
import os
import pysnooper

from src.ar_bot import TradingMarket, TradingEngine

from src.backpack.bp_convertors import json2dict
from src.backpack.bp_general import stdout_msg, pretty_dict_print
from src.backpack.bp_computers import compute_percentage


class TestAREngine(unittest.TestCase):

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
    trading_engine = None

    # PREREQUISITS

    @classmethod
    def setUpClass(cls):
        stdout_msg('\n[ TradingEngine ]: Functional test suit -', bold=True)
        # TODO - Mock me wiggle
        cls.trading_market = TradingMarket(cls.binance_key, cls.binance_secret)
        cls.trading_market.setup()
        stdout_msg('\n[ SETUP ]: Scrape market data...', bold=True)
        cls.market_data = cls.trading_market.scan('all', **cls.context)
        cls.engine = TradingEngine(**cls.context)
        cls.engine.setup(**cls.context)


    @classmethod
    def tearDownClass(cls):
        stdout_msg('\n[ DONE ]: TradingEngine AutoTesters', bold=True)

    # MOCK
    # TODO - Mock market data

    # TESTERS

    def test_ar_engine_evaluation_of_market_data(self):
        stdout_msg(
            '\n[ TEST ]: Evaluate market data and generate Trades...', bold=True
        )
        trades = self.engine.evaluate(self.market_data, **self.context)
        self.assertTrue(isinstance(trades, list))
        self.assertTrue(trades)
        stdout_msg(f'Trades: {trades}', ok=True)
        for trade in trades:
            stdout_msg('* ' + str(trade), green=True)

