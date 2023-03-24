import unittest
import os
import pysnooper

from src.ar_bot import TradingMarket, TradingEngine, Trade, Signal

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
            'order-amount': 1,
            'stop-loss': 10,
            'take-profit': 30,
            'risk-tolerance': 5,
            'test': True,
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

    def generate_mock_signals(self, count):
        signals = []
        for item in range(count):
            sig = Signal(**self.context)
            sig.__dict__.update({
                'side': 'BUY',
                'risk': 5,
                'source_strategy': {
                    'price': {
                        'flag': True,
                        'side': 'BUY'
                    },
                    'volume': {
                        'flag': True,
                        'side': 'BUY',
                    }
                },
            })
            signals.append(sig)
        return signals

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
            self.assertTrue(isinstance(trade, Trade))
            stdout_msg('* ' + str(trade), green=True)

    def test_ar_engine_trade_bad_weather_state_flow(self):
        stdout_msg('\n[ TEST ]: Bad Weather Trade State Flow...', bold=True)
        signals = self.generate_mock_signals(3)

        # State: DRAFT
        trade = Trade(**self.context)
        load = trade.load_signals(self.market_data, *signals, **self.context)
        stdout_msg(
            f'{trade.status} Order\n' + str(pretty_dict_print(trade.unpack())),
            nok=True if not load else False,
            ok=True if load else False,
        )
        self.assertTrue(load)

        # State: DISCARDED
        discard = trade.discard()
        stdout_msg(
            f'{trade.status} Order\n' + str(pretty_dict_print(trade.unpack())),
            nok=True if not discard else False,
            ok=True if discard else False,
        )
        self.assertTrue(discard)

        # State: DRAFT
        previous = trade.previous_state()
        stdout_msg(
            f'{trade.status} Order (Previous)\n' \
            + str(pretty_dict_print(trade.unpack())),
            nok=True if not previous else False,
            ok=True if previous else False,
        )
        self.assertTrue(previous)

        # State: EXPIRED
        expire = trade.expire()
        stdout_msg(
            f'{trade.status} Order\n' + str(pretty_dict_print(trade.unpack())),
            nok=True if not expire else False,
            ok=True if expire else False,
        )
        self.assertTrue(expire)

    def test_ar_engine_trade_good_weather_state_flow(self):
        stdout_msg('\n[ TEST ]: Good Weather Trade State Flow...', bold=True)
        signals = self.generate_mock_signals(3)

        # State: DRAFT
        trade = Trade(**self.context)
        trade.load_signals(self.market_data, *signals, **self.context)

        # MOCK trade fee - not available in market data under testing conditions
        stdout_msg('[ ! ]: Adding mock trading fee of (0.1)')
        trade.trade_fee = 0.1

        check = trade.check_preconditions()
        stdout_msg(
            f'{trade.status} Order\n' + str(pretty_dict_print(trade.unpack())),
            nok=True if not check else False,
            ok=True if check else False,
        )
        self.assertTrue(check)

        # State: EVALUATED
        state_change = trade.next_state()
        self.assertTrue(state_change)

        check = trade.check_preconditions()
        stdout_msg(
            f'{trade.status} Order\n' + str(pretty_dict_print(trade.unpack())),
            nok=True if not check else False,
            ok=True if check else False,
        )
        self.assertTrue(check)

        # State: COMMITED
        state_change = trade.next_state()
        self.assertTrue(state_change)

        # MOCK result - Binance API response for binance.client.create_order()
        stdout_msg('[ ! ]: Adding mock order result ({"orderId": 1234, "test": True})')
        trade.result = {'orderId': 1234, 'test': True}

        check = trade.check_preconditions()
        stdout_msg(
            f'{trade.status} Order\n' + str(pretty_dict_print(trade.unpack())),
            nok=True if not check else False,
            ok=True if check else False,
        )
        self.assertTrue(check)

        # MOCK expiration date cleanup
        stdout_msg('[ ! ]: Clearing Trade expiration date')
        trade.expires_on = None

        # State: DONE
        state_change = trade.next_state()
        self.assertTrue(state_change)

        check = trade.check_preconditions()
        stdout_msg(
            f'{trade.status} Order\n' + str(pretty_dict_print(trade.unpack())),
            nok=True if not check else False,
            ok=True if check else False,
        )
        self.assertTrue(check)


