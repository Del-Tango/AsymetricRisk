import unittest

from src.ar_market import TradingMarket


class TestARMarket(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_key = 'yxdLHNgKWzka2HjzR5jZF0ZXTCZaHp2V1X9EgXjKBxLsfKoClFvET1PqIUW9ctAw'
        cls.api_secret = 'oPyuIoqWHBt5pvfCk1YLIslViuH87DJvRTgtOsLylGB58LRsEuHvu4KuZOv0DAv5'
        cls.taapi_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM2MmRkNThmYzVhOGFkZmVjM2ZhMmEzIiwiaWF0IjoxNjY3NzAxNzg5LCJleHAiOjMzMTcyMTY1Nzg5fQ.33yXXi5RK1oupATjS-RFMLKfD7grZdJ2r7GT4gH-tAE'
        cls.trading_market = TradingMarket(
            cls.api_key, cls.api_secret, sync=True, **{
                'base-currency': 'BTC',
                'api-url': 'https://testnet.binance.vision/api',
                'api-key': cls.api_key,
                'api-secret': cls.api_secret,
                'taapi-key': cls.taapi_key,
                'quote-currency': 'ETH',
            }
        )
        cls.buy_order = cls.trading_market.buy(0.0002, take_profit=30, stop_loss=10, trailing_stop=10)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ar_market_close_position(cls):
        buy_order = cls.trading_market.buy(0.0002, take_profit=30, stop_loss=10, trailing_stop=10)
        close_ok, close_nok = cls.trading_market.close_position(buy_order.get('orderId'))
        cls.assertTrue(isinstance(close_ok, list))
        cls.assertTrue(isinstance(close_nok, list))
        cls.assertFalse(close_nok)

    def test_ar_market_buy(cls):
        buy_order = cls.trading_market.buy(0.0002, take_profit=30, stop_loss=10, trailing_stop=10)
        cls.assertTrue(isinstance(buy_order, dict))

    def test_ar_market_sell(cls):
        sell_order = cls.trading_market.sell(0.0002, take_profit=30, stop_loss=10, trailing_stop=10)
        cls.assertTrue(isinstance(sell_order, dict))

    def test_ar_market_update_details(cls):
        update_details = cls.trading_market.update_details('all')
        cls.assertTrue(isinstance(update_details, dict))

    def test_ar_market_synced(cls):
        account_info = cls.trading_market.synced('get_account', recvWindow=60000)
        cls.assertTrue(account_info)


