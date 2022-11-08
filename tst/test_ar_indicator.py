import unittest
import time
import json

from src.ar_indicator import TradingIndicator
from src.backpack.bp_convertors import json2dict, dict2json
from src.backpack.bp_general import write2file


class TestARIndicator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.taapi_url = 'https://api.taapi.io'
        cls.taapi_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM2MmRkNThmYzVhOGFkZmVjM2ZhMmEzIiwiaWF0IjoxNjY3NDI0MDgzLCJleHAiOjMzMTcxODg4MDgzfQ.3QU6D_eERXZB4Ir2Dq4FLcDvzuVE_vIUfw5rLDiOFoM'
        cls.tmp_file = '/tmp/.ar_test.tmp'
        cls.delay_sec = 1
        cls.nok_codes = [401]
        cls.trading_indicator = TradingIndicator(**{
            'taapi-url': cls.taapi_url,
            'taapi-key': cls.taapi_key,
        })

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ar_indicator_ping(cls):
        response_raw = cls.trading_indicator.ping()
        time.sleep(cls.delay_sec)
        cls.assertTrue(response_raw)

    def test_ar_indicator_set_api_url(cls):
        response_raw = cls.trading_indicator.set_api_url(cls.taapi_url)
        time.sleep(cls.delay_sec)
        cls.assertEqual(response_raw, cls.taapi_url)

    def test_ar_indicator_set_api_key(cls):
        response_raw = cls.trading_indicator.set_api_secret_key(cls.taapi_key)
        time.sleep(cls.delay_sec)
        cls.assertEqual(response_raw, cls.taapi_key)

    def test_ar_indicator_format_target_url(cls):
        response = cls.trading_indicator.format_target_url(
            'rsi', secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        time.sleep(cls.delay_sec)
        cls.assertEqual(response, 'https://api.taapi.io/rsi?secret={}&exchange=binance&symbol=BTC/USDT&interval=1h'.format(cls.taapi_key))

    def test_ar_indicator_api_call(cls):
        formatted_url = cls.trading_indicator.format_target_url(
            'rsi', secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        response_raw = cls.trading_indicator.api_call(formatted_url)
        sanitized = ''.join(list(response_raw)[1:]).replace("'", '')
        response_dict = json.loads(sanitized)
        if response_dict['statusCode'] in cls.nok_codes:
            return False
        time.sleep(cls.delay_sec)
        cls.assertTrue(response_raw)

    def test_ar_indicator_adx(cls):
        response_raw = cls.trading_indicator.adx(
            secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        sanitized = ''.join(list(response_raw)[1:]).replace("'", '')
        response_dict = json.loads(sanitized)
        if response_dict['statusCode'] in cls.nok_codes:
            return False
        time.sleep(cls.delay_sec)
        cls.assertTrue(response_raw)

    def test_ar_indicator_macd(cls):
        response_raw = cls.trading_indicator.macd(
            secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        sanitized = ''.join(list(response_raw)[1:]).replace("'", '')
        response_dict = json.loads(sanitized)
        if response_dict['statusCode'] in cls.nok_codes:
            return False
        time.sleep(cls.delay_sec)
        cls.assertTrue(response_raw)

    def test_ar_indicator_ma(cls):
        response_raw = cls.trading_indicator.ma(
            secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        sanitized = ''.join(list(response_raw)[1:]).replace("'", '')
        response_dict = json.loads(sanitized)
        if response_dict['statusCode'] in cls.nok_codes:
            return False
        time.sleep(cls.delay_sec)
        cls.assertTrue(response_raw)

    def test_ar_indicator_rsi(cls):
        response_raw = cls.trading_indicator.rsi(
            secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        sanitized = ''.join(list(response_raw)[1:]).replace("'", '')
        response_dict = json.loads(sanitized)
        if response_dict['statusCode'] in cls.nok_codes:
            return False
        time.sleep(cls.delay_sec)
        cls.assertTrue(response_raw)

    def test_ar_indicator_vwap(cls):
        response_raw = cls.trading_indicator.vwap(
            secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        sanitized = ''.join(list(response_raw)[1:]).replace("'", '')
        response_dict = json.loads(sanitized)
        if response_dict['statusCode'] in cls.nok_codes:
            return False
        time.sleep(cls.delay_sec)
        cls.assertTrue(response_raw)

