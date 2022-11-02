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
        cls.trading_indicator = TradingIndicator(**{
            'taapi-url': cls.taapi_url,
            'taapi-key': cls.taapi_key,
        })

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ar_indicator_ping(cls):
        response = cls.trading_indicator.ping()
        print(response)
        time.sleep(cls.delay_sec)
        cls.assertTrue(response)

    def test_ar_indicator_set_api_url(cls):
        response = cls.trading_indicator.set_api_url(cls.taapi_url)
        print(response)
        time.sleep(cls.delay_sec)
        cls.assertEqual(response, cls.taapi_url)

    def test_ar_indicator_set_api_key(cls):
        response = cls.trading_indicator.set_api_secret_key(cls.taapi_key)
        print(response)
        time.sleep(cls.delay_sec)
        cls.assertEqual(response, cls.taapi_key)

    def test_ar_indicator_format_target_url(cls):
        response = cls.trading_indicator.format_target_url(
            'rsi', secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        print(response)
        time.sleep(cls.delay_sec)
        cls.assertEqual(response, 'https://api.taapi.io/rsi?secret={}&exchange=binance&symbol=BTC/USDT&interval=1h'.format(cls.taapi_key))

    def test_ar_indicator_api_call(cls):
        formatted_url = cls.trading_indicator.format_target_url(
            'rsi', secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        response = cls.trading_indicator.api_call(formatted_url)
        type(response)
        print(response)
        write2file(response, file_path=cls.tmp_file, mode='w')
        try:
            response_dct = json2dict(cls.tmp_file)
            print(response_dct)
            cls.assertFalse(response_dct.get('error', False))
        except Exception as e:
            print(e)
        time.sleep(cls.delay_sec)
        cls.assertTrue(response)

    def test_ar_indicator_adx(cls):
        response = cls.trading_indicator.adx(
            secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        print(response)
        write2file(response, file_path=cls.tmp_file, mode='w')
        try:
            response_dct = json2dict(cls.tmp_file)
            print(response_dct)
            cls.assertFalse(response_dct.get('error', False))
        except Exception as e:
            print(e)
        time.sleep(cls.delay_sec)
        cls.assertTrue(response)

    def test_ar_indicator_macd(cls):
        response = cls.trading_indicator.macd(
            secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        print(response)
        write2file(response, file_path=cls.tmp_file, mode='w')
        try:
            response_dct = json2dict(cls.tmp_file)
            print(response_dct)
            cls.assertFalse(response_dct.get('error', False))
        except Exception as e:
            print(e)
        time.sleep(cls.delay_sec)
        cls.assertTrue(response)

    def test_ar_indicator_ma(cls):
        response = cls.trading_indicator.ma(
            secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        print(response)
        write2file(response, file_path=cls.tmp_file, mode='w')
        try:
            response_dct = json2dict(cls.tmp_file)
            print(response_dct)
            cls.assertFalse(response_dct.get('error', False))
        except Exception as e:
            print(e)
        time.sleep(cls.delay_sec)
        cls.assertTrue(response)

    def test_ar_indicator_rsi(cls):
        response = cls.trading_indicator.rsi(
            secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        print(response)
        write2file(response, file_path=cls.tmp_file, mode='w')
        try:
            response_dct = json2dict(cls.tmp_file)
            print(response_dct)
            cls.assertFalse(response_dct.get('error', False))
        except Exception as e:
            print(e)
        time.sleep(cls.delay_sec)
        cls.assertTrue(response)

    def test_ar_indicator_vwap(cls):
        response = cls.trading_indicator.vwap(
            secret=cls.taapi_key, exchange='binance', symbol='BTC/USDT',
            interval='1h'
        )
        print(response)
        write2file(response, file_path=cls.tmp_file, mode='w')
        try:
            response_dct = json2dict(cls.tmp_file)
            print(response_dct)
            cls.assertFalse(response_dct.get('error', False))
        except Exception as e:
            print(e)
        time.sleep(cls.delay_sec)
        cls.assertTrue(response)

