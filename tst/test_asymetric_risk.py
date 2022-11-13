import unittest
import os
import threading
import time

#   from src.ar_bot import TradingBot
#   from src.ar_strategy import TradingStrategy
#   from src.ar_reporter import TradingReporter
from . import asymetric_risk


class TestAsymetricRiskInterface(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_key = 'yxdLHNgKWzka2HjzR5jZF0ZXTCZaHp2V1X9EgXjKBxLsfKoClFvET1PqIUW9ctAw'
        cls.api_secret = 'oPyuIoqWHBt5pvfCk1YLIslViuH87DJvRTgtOsLylGB58LRsEuHvu4KuZOv0DAv5'
        cls.taapi_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM2MmRkNThmYzVhOGFkZmVjM2ZhMmEzIiwiaWF0IjoxNjY3NzAxNzg5LCJleHAiOjMzMTcyMTY1Nzg5fQ.33yXXi5RK1oupATjS-RFMLKfD7grZdJ2r7GT4gH-tAE'
        cls.trading_strategies = (
            'rsi', 'vwap', 'ma', 'ema', 'macd', 'adx', 'price', 'volume'
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test_(self):
        pass
#       view = self.trading_bot.view_trade_history()
#       self.assertTrue(view)


