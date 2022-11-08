import unittest

from src.ar_bot import TradingBot


class TestARBot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_key = 'yxdLHNgKWzka2HjzR5jZF0ZXTCZaHp2V1X9EgXjKBxLsfKoClFvET1PqIUW9ctAw'
        cls.api_secret = 'oPyuIoqWHBt5pvfCk1YLIslViuH87DJvRTgtOsLylGB58LRsEuHvu4KuZOv0DAv5'
        cls.taapi_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM2MmRkNThmYzVhOGFkZmVjM2ZhMmEzIiwiaWF0IjoxNjY3NzAxNzg5LCJleHAiOjMzMTcyMTY1Nzg5fQ.33yXXi5RK1oupATjS-RFMLKfD7grZdJ2r7GT4gH-tAE'
        tbot_kwargs = cls.fetch_trading_market_kwargs('BTC', 'USDT')
        cls.trading_bot = TradingBot(**tbot_kwargs)

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
        }

    def test_select_market(self):
        action_kwargs = self.fetch_trading_market_kwargs('ETH', 'BTC')
        enter_market = self.trading_bot.enter_market(**action_kwargs)
        select_market = self.trading_bot.select_market('ETH/BTC')
        self.assertTrue(select_market)

    def test_enter_market(self):
        action_kwargs = self.fetch_trading_market_kwargs('ETH', 'BTC')
        enter_market = self.trading_bot.enter_market(**action_kwargs)
        self.assertTrue(enter_market)

    def test_exit_market(self):
        exit_market = self.trading_bot.exit_market('BTC/USDT')
        self.assertTrue(exit_market)
        self.assertFalse(exit_market.get('error', False))

    # TODO
    def test_setup_reporter(self):
        pass
    def test_trade(self):
        pass
    def test_close_trade(self):
        pass
    def test_view_trades(self):
        pass
    def test_view_trade_history(self):
        pass
    def test_generate_report(self):
        pass
