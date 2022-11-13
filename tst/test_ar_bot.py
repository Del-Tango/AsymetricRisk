import unittest
import os
import threading
import time

from src.ar_bot import TradingBot
from src.ar_strategy import TradingStrategy
from src.ar_reporter import TradingReporter


class TestARBot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_key = 'yxdLHNgKWzka2HjzR5jZF0ZXTCZaHp2V1X9EgXjKBxLsfKoClFvET1PqIUW9ctAw'
        cls.api_secret = 'oPyuIoqWHBt5pvfCk1YLIslViuH87DJvRTgtOsLylGB58LRsEuHvu4KuZOv0DAv5'
        cls.taapi_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM2MmRkNThmYzVhOGFkZmVjM2ZhMmEzIiwiaWF0IjoxNjY3NzAxNzg5LCJleHAiOjMzMTcyMTY1Nzg5fQ.33yXXi5RK1oupATjS-RFMLKfD7grZdJ2r7GT4gH-tAE'
        cls.trading_strategies = (
            'rsi', 'vwap', 'ma', 'ema', 'macd', 'adx', 'price', 'volume'
        )
        cls.tbot_kwargs = cls.fetch_trading_market_kwargs('BTC', 'USDT')
        cls.trading_bot = TradingBot(**cls.tbot_kwargs)

    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def fetch_trading_market_kwargs(cls, base_currency, quote_currency):
        return {
            'base-currency': base_currency,
            'quote-currency': quote_currency,
            'ticker-symbol': base_currency + '/' + quote_currency,
            'api-url': 'https://testnet.binance.vision/api',
            'api-key': cls.api_key,
            'api-secret': cls.api_secret,
            'taapi-key': cls.taapi_key,
            'market-sync': True,
            'test': True,
        }

    @classmethod
    def fetch_trade_kwargs(cls, **kwargs):
        return {
            'test': True,
            'analyze-risk': kwargs.get('analyze-risk', True),
            'strategy': kwargs.get('strategy', ','.join(cls.trading_strategies)),
            'side': kwargs.get('side', 'auto'),
            'price-movement': kwargs.get('price-movement', 5),
            'rsi-top': kwargs.get('rsi-top', 70),
            'rsi-bottom': kwargs.get('rsi-bottom', 30),
            'interval': kwargs.get('interval', '5m'),
            'rsi-period': kwargs.get('rsi-period', 14),
            'rsi-backtrack': kwargs.get('rsi-backtrack', 5),
            'rsi-backtracks': kwargs.get('rsi-backtracks', 12),
            'rsi-chart': kwargs.get('rsi-chart', 'candles'),
            'rsi-interval': kwargs.get('rsi-interval', '5m'),
            'volume-movement': kwargs.get('volume-movement', 5),
            'volume-interval': kwargs.get('volume-interval', '5m'),
            'ma-period': kwargs.get('ma-period', 30),
            'ma-backtrack': kwargs.get('ma-backtrack', 5),
            'ma-backtracks': kwargs.get('ma-backtracks', 12),
            'ma-chart': kwargs.get('ma-chart', 'candles'),
            'ma-interval': kwargs.get('ma-interval', '5m'),
            'ema-period': kwargs.get('ema-period', 30),
            'ema-backtrack': kwargs.get('ema-backtrack', 5),
            'ema-backtracks': kwargs.get('ema-backtracks', 12),
            'ema-chart': kwargs.get('ema-chart', 'candles'),
            'ema-interval': kwargs.get('ema-interval', '5m'),
            'macd-backtrack': kwargs.get('macd-backtrack', 5),
            'macd-backtracks': kwargs.get('macd-backtracks', 12),
            'macd-chart': kwargs.get('macd-chart', 'candles'),
            'macd-fast-period': kwargs.get('macd-fast-period', 12),
            'macd-slow-period': kwargs.get('macd-slow-period', 26),
            'macd-signal-period': kwargs.get('macd-signal-period', 9),
            'macd-interval': kwargs.get('macd-interval', '5m'),
            'adx-period': kwargs.get('adx-period', 14),
            'adx-backtrack': kwargs.get('adx-backtrack', 5),
            'adx-backtracks': kwargs.get('adx-backtracks', 12),
            'adx-chart': kwargs.get('adx-chart', 'candles'),
            'adx-interval': kwargs.get('adx-interval', '5m'),
            'vwap-period': kwargs.get('vwap-period', 14),
            'vwap-backtrack': kwargs.get('vwap-backtrack', 5),
            'vwap-backtracks': kwargs.get('vwap-backtracks', 12),
            'vwap-chart': kwargs.get('vwap-chart', 'candles'),
            'vwap-interval': kwargs.get('vwap-interval', '5m'),
        }

    @classmethod
    def fetch_trading_report_setup_kwargs(cls, **kwargs):
        return cls.tbot_kwargs

    @classmethod
    def fetch_strategy_analyzer_setup_kwargs(cls, **kwargs):
        return cls.tbot_kwargs


    # TODO
    def test_generate_report(self):
        pass


    def test_select_market(self):
        action_kwargs = self.fetch_trading_market_kwargs('BTC', 'USDT')
        enter_market = self.trading_bot.enter_market(**action_kwargs)
        select_market = self.trading_bot.select_market('BTC/USDT')
        self.assertTrue(select_market)

    def test_enter_market(self):
        action_kwargs = self.fetch_trading_market_kwargs('BTC', 'USDT')
        enter_market = self.trading_bot.enter_market(**action_kwargs)
        self.assertTrue(enter_market)

    def test_exit_market(self):
        exit_market = self.trading_bot.exit_market('BTC/USDT')
        self.assertTrue(exit_market)
        self.assertTrue(isinstance(exit_market, dict))
        self.assertFalse(exit_market.get('error', False))

    def test_trade(self):
        trade = self.trading_bot.trade(
            *self.trading_strategies, **self.fetch_trade_kwargs()
        )
        self.assertFalse(trade.get('error', True))

    def test_watchdog(self):
        process_anchor_file = '.ar.test.anch'
        with open(process_anchor_file, 'w') as fl:
            fl.write('.')
        t = threading.Thread(
            target=self.remove_file,
            args=(process_anchor_file,),
            name='Watchdog Killer'
        )
        t.daemon = True
        t.start()
        trade = self.trading_bot.trade_watchdog(
            **{'anchor-file': process_anchor_file}
        )
        self.assertEqual(trade, 0)

    def test_setup_reporter(self):
        action_kwargs = self.fetch_trading_report_setup_kwargs()
        setup = self.trading_bot.setup_reporter(**action_kwargs)
        self.assertTrue(isinstance(setup, TradingReporter))

    def test_setup_analyzer(self):
        action_kwargs = self.fetch_strategy_analyzer_setup_kwargs()
        setup = self.trading_bot.setup_analyzer(**action_kwargs)
        self.assertTrue(isinstance(setup, TradingStrategy))

    def test_close_trade(self):
        trade = self.trading_bot.trade(
            *self.trading_strategies, **self.fetch_trade_kwargs()
        )
        closed, failed_to_close = self.trading_bot.close_trade(
            trade.get('id'), **{
                'symbol': self.fetch_trading_market_kwargs('BTC', 'USDT')['ticker-symbol'],
                'recvWindow': 60000,
            }
        )
        self.assertFalse(failed_to_close)
        self.assertTrue(isinstance(closed, list))
        self.assertTrue(closed)

    def test_view_trades(self):
        view = self.trading_bot.view_trades()
        self.assertTrue(view)

    def test_view_trade_history(self):
        view = self.trading_bot.view_trade_history()
        self.assertTrue(view)

    def remove_file(self, file_path, *args, delay=3, **kwargs):
        time.sleep(delay)
        if not os.path.exists(file_path):
            return False
        return os.remove(file_path)


