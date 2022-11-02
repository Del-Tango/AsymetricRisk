import unittest

from src.ar_market import TradingMarket


class TestARMarket(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_key = 'yxdLHNgKWzka2HjzR5jZF0ZXTCZaHp2V1X9EgXjKBxLsfKoClFvET1PqIUW9ctAw'
        cls.api_secret = 'oPyuIoqWHBt5pvfCk1YLIslViuH87DJvRTgtOsLylGB58LRsEuHvu4KuZOv0DAv5'
        cls.trading_market = TradingMarket(
            cls.api_key, cls.api_secret, sync=True, **{
                'crypto': 'BTC',
                'api-url': 'https://testnet.binance.vision/api',
                'api-key': cls.api_key,
                'api-secret': cls.api_secret,
                'exchange-crypto': 'ETH',
            }
        )
        cls.buy_order = cls.trading_market.buy(0.0002, take_profit=30, stop_loss=10, trailing_stop=10)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ar_market_buy(cls):
        buy_order = cls.trading_market.buy(0.0002, take_profit=30, stop_loss=10, trailing_stop=10)
        cls.assertTrue(isinstance(buy_order, dict))

    def test_ar_market_sell(cls):
        sell_order = cls.trading_market.sell(0.0002, take_profit=30, stop_loss=10, trailing_stop=10)
        cls.assertTrue(isinstance(sell_order, dict))

    def test_ar_market_indicators(cls):
        indicators = cls.trading_market.indicators('rsi', 'macd', 'adx', 'ma', 'vwap')
        cls.assertTrue(isinstance(indicators, dict))

    def test_ar_market_close_position(cls):
        close_position = cls.trading_market.close_position()
        cls.assertTrue(isinstance(close_position, dict))

    def test_ar_market_update_details(cls):
        update_details = cls.trading_market.update_details()
        cls.assertTrue(isinstance(update_details, dict))

    def test_ar_market_synced(cls):
        account_info = cls.trading_market.synced('get_account', recvWindow=60000)
        cls.assertTrue(account_info)


