import unittest
import os

from src.ar_bot import TradingMarket, Trade
from src.backpack.bp_convertors import json2dict
from src.backpack.bp_general import pretty_dict_print
from src.backpack.bp_computers import compute_percentage


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
        new_trade = Trade(**self.context)
        data = self.trading_market.scan('all', **self.context)

        print(f'[ DEBUG ]: Market Scan Data: {data}')
        pretty_dict_print(data)

        if not data['ticker']['info']['ocoAllowed']:
            print(
                f"[ WARNING ]: Ticker symbol {data['ticker']['info']['ocoAllowed']} "
                "does not support OCO orders!"
            )
            self.assertTrue(False)
        new_trade.update(**{
            'status': new_trade.STATUS_EVALUATED,
            'risk': 1,
            'base_quantity': 0.1,
            'quote_quantity': None,
            'side': new_trade.SIDE_BUY,
            'current_price': data['ticker']['symbol']['lastPrice'],
            'stop_loss_price': compute_percentage(
                data['ticker']['symbol']['lastPrice'], 10, operation='subtract'
            ),
            'take_profit_price': compute_percentage(
                data['ticker']['symbol']['lastPrice'], 30, operation='add'
            ),
            'trade_fee': 0.1,
        })
        return new_trade

    # TESTERS

    def test_ar_market_run_trade(self):
        print('\n[ TEST ]: Execute trade order...\n')
        trade_obj = self.generate_mock_trade_instance()
        run = self.trading_market.run(trade_obj)
        self.assertTrue(run)
        self.assertTrue(isinstance(run, dict))
        self.assertTrue(isinstance(run.get('failures'), int))
        self.assertEqual(run['failures'], 0)
        self.assertTrue(run.get('ok'))
        self.assertTrue(isinstance(run['ok'], list))
        self.assertTrue(run.get('nok'))
        self.assertTrue(isinstance(run['nok'], list))

    def test_ar_market_scrape_data(self):
        print('\n[ TEST ]: Scrape market data...\n')
        data = self.trading_market.scan('all', **self.context)
#       print(f'[ DEBUG ]: Market Scan Data: {data}')
#       self.market_data_scan_cache = data
#       print(f'[ DEBUG ]: Market Scan Data: {self.market_data_scan_cache}')
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

