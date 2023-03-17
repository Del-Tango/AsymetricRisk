import unittest
import os

from src.ar_bot import TradingMarket, Trade
from src.backpack.bp_convertors import json2dict
from src.backpack.bp_general import pretty_dict_print


class TestARMarket(unittest.TestCase):

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
        }
    else:
        context = AR_DEFAULT
    binance_key = context.get('binance-key')
    binance_secret = context.get('binance-secret')
    taapi_key = context.get('taapi-key')
    trading_market = None
    market_data_scan_cache = {}

    # PREREQUISITS

    @classmethod
    def setUpClass(cls):
        print('\n[ TradingMarket ]: Functional test suit -\n')
        cls.trading_market = TradingMarket(cls.binance_key, cls.binance_secret)
        cls.trading_market.setup()

    @classmethod
    def tearDownClass(cls):
        print('\n[ DONE ]: TradingMarket\n')

    # MOCK

    # TODO
    def generate_mock_trade_instance(self):
        new_trade = Trade(**context)
        data = self.market_data_scan_cache
        # TODO - Fetch details from last market scan
        new_trade.update(**{
            'status': new_trade.STATUS_EVALUATED,
            'risk': 1,
            'base_quantity': 0.1,
            'quote_quantity': None,
            'side': new_trade.SIDE_BUY,
            'current_price': data.get(''),
            'stop_loss_price': data.get(''),
            'take_profit_price': data.get(''),
            'trade_fee': 0.1,
        })
        return new_trade

    # TESTERS

    # TODO
    def test_ar_market_run_trade(self):
        trade_obj = self.generate_mock_trade_instance()
        run = self.trading_market.run(trade_obj)

    def test_ar_market_scrape_data(self):
        print('\n[ TEST ]: Scrape market data...\n')
        data = self.trading_market.scan('all', **self.context)
        self.market_data_scan_cache = data
        pretty_dict_print(data)
        self.assertTrue(data)
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data.get('failures'), 0)
        self.assertTrue(data.get('account'))
        self.assertTrue(isinstance(data['account'], dict))
        self.assertTrue(data.get('ticker'))
        self.assertTrue(isinstance(data['ticker'], dict))
        self.assertTrue(data.get('api'))
        self.assertTrue(isinstance(data['api'], dict))
        self.assertTrue(data.get('indicators'))
        self.assertTrue(isinstance(data['indicators'], dict))

# CODE DUMP

