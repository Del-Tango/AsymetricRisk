import unittest
import os
import pysnooper

from src.ar_bot import TradingMarket, Trade, Signal
from src.backpack.bp_convertors import json2dict
from src.backpack.bp_general import stdout_msg, pretty_dict_print
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
        stdout_msg('\n[ TradingMarket ]: Functional test suit -', bold=True)
        cls.trading_market = TradingMarket(cls.binance_key, cls.binance_secret)
        cls.trading_market.setup()

    @classmethod
    def tearDownClass(cls):
        stdout_msg('\n[ CLEANUP ]: Closing trades...', bold=True)
        order_ids = [item['orderId'] for item in cls.trading_market.get_open_orders()]
        for order_id in order_ids:
            stdout_msg(f"[ {cls.context['ticker-symbol']} ]: {order_id}")
            try:
                cls.trading_market.cancel_order(
                    symbol=cls.context['ticker-symbol'].replace('/', ''),
                    orderId=order_id
                )
            except Exception as e:
                stdout_msg(f'{e}', warn=True)
        stdout_msg('\n[ DONE ]: TradingMarket AutoTesters', bold=True)

    # MOCK

#   @pysnooper.snoop()
    def generate_mock_buy_trade_instance(self):
        new_trade = Trade(**self.context)
        data = self.trading_market.scan('all', **self.context)
        if not data['ticker']['info']['ocoAllowed']:
            stdout_msg(
                f"Ticker symbol {data['ticker']['info']['ocoAllowed']} "
                "does not support OCO orders!", warn=True
            )
            raise
        new_trade.update(**{
            'status': new_trade.STATUS_EVALUATED,
            'risk': 1,
            'base_quantity': self.context.get('order-amount', 100),
            'side': new_trade.SIDE_BUY,
            'current_price': float(data['ticker']['symbol']['lastPrice']),
            'stop_loss_price': round(
                float(data['ticker']['symbol']['lastPrice']) \
                * (1 + self.context['stop-loss'] / 100), 4
            ),
            'take_profit_price': round(
                float(data['ticker']['symbol']['lastPrice']) \
                * (1 - self.context['take-profit'] / 100), 4
            ),
            'trade_fee': 0.1, # Cannot be fetched by market using testnet API keys
        })
        new_trade.quote_quantity = round(float(
            new_trade.base_quantity * new_trade.current_price
        ), 8)
        new_trade.filter_check(*data['ticker']['info']['filters'])
        new_trade._signals = [Signal(), Signal()]
        return new_trade

#   @pysnooper.snoop()
    def generate_mock_sell_trade_instance(self):
        new_trade = Trade(**self.context)
        data = self.trading_market.scan('all', **self.context)
        if not data['ticker']['info']['ocoAllowed']:
            stdout_msg(
                f"Ticker symbol {data['ticker']['info']['ocoAllowed']} "
                "does not support OCO orders!", warn=True
            )
            raise
        new_trade.update(**{
            'status': new_trade.STATUS_EVALUATED,
            'risk': 1,
            'base_quantity': self.context.get('order-amount', 100),
            'side': new_trade.SIDE_SELL,
            'current_price': float(data['ticker']['symbol']['lastPrice']),
            'stop_loss_price': round(
                float(data['ticker']['symbol']['lastPrice']) \
                * (1 - self.context['stop-loss'] / 100), 4
            ),
            'take_profit_price': round(
                float(data['ticker']['symbol']['lastPrice']) \
                * (1 + self.context['take-profit'] / 100), 4
            ),
            'trade_fee': 0.1, # Cannot be fetched by market using testnet API keys
        })
        new_trade.quote_quantity = round(float(
            new_trade.base_quantity * new_trade.current_price
        ), 8)
        new_trade.filter_check(*data['ticker']['info']['filters'])
        new_trade._signals = [Signal(), Signal()]
        return new_trade

    # TESTERS

    def test_ar_market_run_sell_trade(self):
        stdout_msg('\n[ TEST ]: Execute SELL trade order...', bold=True)
        trade_obj = self.generate_mock_sell_trade_instance()
        check = trade_obj.check_preconditions()
        self.assertTrue(check)
        change_state = trade_obj.next_state()
        self.assertTrue(change_state)
        run = self.trading_market.run(trade_obj)
        self.assertTrue(run)
        self.assertTrue(isinstance(run, dict))
        self.assertTrue(isinstance(run.get('failures'), int))
        self.assertEqual(run['failures'], 0)
        self.assertTrue(run.get('ok'))
        self.assertTrue(isinstance(run['ok'], list))
        self.assertFalse(run.get('nok'))
        self.assertTrue(isinstance(run['nok'], list))

    def test_ar_market_run_buy_trade(self):
        stdout_msg('\n[ TEST ]: Execute BUY trade order...', bold=True)
        trade_obj = self.generate_mock_buy_trade_instance()
        check = trade_obj.check_preconditions()
        self.assertTrue(check)
        change_state = trade_obj.next_state()
        self.assertTrue(change_state)
        run = self.trading_market.run(trade_obj)
        self.assertTrue(run)
        self.assertTrue(isinstance(run, dict))
        self.assertTrue(isinstance(run.get('failures'), int))
        self.assertEqual(run['failures'], 0)
        self.assertTrue(run.get('ok'))
        self.assertTrue(isinstance(run['ok'], list))
        self.assertFalse(run.get('nok'))
        self.assertTrue(isinstance(run['nok'], list))

    def test_ar_market_scrape_data(self):
        stdout_msg('\n[ TEST ]: Scrape market data...', bold=True)
        data = self.trading_market.scan('all', **self.context)
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

