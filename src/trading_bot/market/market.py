#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADING MARKET

import os
import logging
import time
import datetime
import json
import pysnooper
import pandas
import numpy

from binance.client import Client
#from .indicators import TradingIndicator
from src.backpack.bp_general import stdout_msg, pretty_dict_print

log = logging.getLogger('AsymetricRisk')


class TradingMarket(Client):
    '''
    [ NOTE ]: Responsibilities:
        * Scrape market data
            * Ticker data
                * Limitations
                * Rules
            * Market Data
                * Price action
                * Volume
                * Indicators
        * Cache scraped data
        * Execute trade objects
    '''

    @pysnooper.snoop()
    def __init__(self, binance_key, binance_secret, *args, sync=True, **context):
        super().__init__(binance_key, binance_secret, *args)
        self.API_URL = context.get('binance-url', 'https://testnet.binance.vision/api')
        if not self.API_KEY:
            self.API_KEY = binance_key \
                or context.get('binance-key', os.environ.get('BINANCE_KEY'))
        if not self.API_SECRET:
            self.API_SECRET = binance_secret \
                or context.get('binance-secret', os.environ.get('BINANCE_SECRET'))
        self._context = context
        self._cache = {}
        self._time_offset = 0
        if sync:
            self._time_offset = self._fetch_time_offset()

    # FETCHERS

    @pysnooper.snoop()
    def _fetch_time_offset(self):
        log.debug('')
        res = self.get_server_time()
        return res.get('serverTime') - int(time.time() * 1000)

    # UPDATES

    def update_context(self, **new_updates):
        log.debug('')
        self._context.update(new_updates)
        return self._context

    # GENERAL

    # SCANNERS

    # TODO
    @pysnooper.snoop()
    def scan_indicator_data(self, **context):
        log.debug('TODO - Under construction, building...')
        # TODO - Fetch indicator data from indicator manager
        return {}

    @pysnooper.snoop()
    def scan_account_data(self, **context):
        log.debug('')
        recv_window = context.get('recv-window', self._context.get('recv-window', 60000))
        ticker = context.get('ticker-symbol', self._context.get('ticker-symbol', str())).replace('/', '')
        return {
            'account': self.get_account(recvWindow=recv_window),
            'trading-orders': self.get_all_orders(symbol=ticker, recvWindow=recv_window),
        }
        if context.get('extended')
            scan.update({
                'deposit-history': self.get_deposit_history(recvWindow=recv_window),
                'status': self.get_account_status(recvWindow=recv_window),
                'withdraw-history': self.get_withdraw_history(recvWindow=recv_window),
            })
        return scan

    @pysnooper.snoop()
    def scan_api_data(self, **context):
        log.debug('')
        recv_window = context.get('recv-window', self._context.get('recv-window', 60000))
        scan = {
            'server-time': self.get_server_time(),
        }
        if context.get('extended'):
            scan.update({
                'permissions': self.get_account_api_permissions(recvWindow=recv_window),
                'trading-status': self.get_account_api_trading_status(recvWindow=recv_window),
            })
        return scan

    @pysnooper.snoop()
    def scan_ticker_symbol_data(self, **context):
        log.debug('')
        recv_window = context.get('recv-window', self._context.get('recv-window', 60000))
        ticker = context.get('ticker-symbol', self._context.get('ticker-symbol', str())).replace('/', '')
        interval = context.get('interval', self._context.get('interval'))
        period = context.get('period', self._context.get('period'))
        scan = {
            'ticker': self.get_ticker(symbol=ticker),
            'info': self.get_symbol_info(ticker),
            'historical-klines': self.get_historical_klines(ticker, interval, limit=period),
        }
        if context.get('extended'):
            scan.update({
                'trade-fee': self.get_trade_fee(symbol=ticker, recvWindow=recv_window),
            })
        return scan

    # GENERAL

    # TODO - Unpack trade object into oco order kwargs
    def unpack(self, trade, **context) -> dict:
        log.debug('TODO - Under construction')
        return {
#           '': ,
        }

    def update_cache(self, data, cache, **context):
        log.debug('')
        cache.update(data)
        return cache

    # ACTIONS

    # TODO
    def setup(self):
        '''
        [ NOTE ]: Validates API keys, executes a preliminary market scan to update
            the cache and run a short series of tests.
        '''
        log.debug('')
        # Validate API keys
        # Run preliminary market scan
        print(f'[ DEBUG ]: API_KEY {self.API_KEY}')
        print(f'[ DEBUG ]: API_SECRET {self.API_SECRET}')
        # Add scan results to cache
        # Run sanity tests

#   @pysnooper.snoop()
    def scan(self, *targets: str, **context) -> dict:
        '''
        [ NOTE ]: Scan market and retrieve data on the ticker symbol, account,
            api and market indicators.
        '''
        log.debug('')
        failures, scan, scanners = 0, {}, {
            'ticker': self.scan_ticker_symbol_data,
            'account': self.scan_account_data,
            'api': self.scan_api_data,
            'indicator': self.scan_indicator_data,
        }
        if 'all' in targets or 'ALL' in targets:
            targets = list(scanners.keys())
        for target in targets:
            scan[target] = scanners[target](**context)
            if not scan[target]:
                failures += 1
        self.update_cache(scan, self._cache, **context)
        scan['failures'] = failures
        log.debug(f'Market scan: {scan}')
        return scan

    def run(self, *trades, **context) -> dict:
        '''
        [ NOTE ]: Takes in any number of Trade() instances and executes them as
            SPOT account OCO trades.

        [ RESPONSE ]: {
            "orderListId": 0,
            "contingencyType": "OCO",
            "listStatusType": "EXEC_STARTED",
            "listOrderStatus": "EXECUTING",
            "listClientOrderId": "JYVpp3F0f5CAG15DhtrqLp",
            "transactionTime": 1563417480525,
            "symbol": "LTCBTC",
            "orders": [
                {
                "symbol": "LTCBTC",
                "orderId": 2,
                "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos"
                },
                {
                "symbol": "LTCBTC",
                "orderId": 3,
                "clientOrderId": "xTXKaGYd4bluPVp78IVRvl"
                }
            ],
            "orderReports": [
                {
                "symbol": "LTCBTC",
                "orderId": 2,
                "orderListId": 0,
                "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos",
                "transactTime": 1563417480525,
                "price": "0.000000",
                "origQty": "0.624363",
                "executedQty": "0.000000",
                "cummulativeQuoteQty": "0.000000",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "STOP_LOSS",
                "side": "BUY",
                "stopPrice": "0.960664",
                "workingTime": -1,
                "selfTradePreventionMode": "NONE"
                },
                {
                "symbol": "LTCBTC",
                "orderId": 3,
                "orderListId": 0,
                "clientOrderId": "xTXKaGYd4bluPVp78IVRvl",
                "transactTime": 1563417480525,
                "price": "0.036435",
                "origQty": "0.624363",
                "executedQty": "0.000000",
                "cummulativeQuoteQty": "0.000000",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT_MAKER",
                "side": "BUY",
                "workingTime": 1563417480525,
                "selfTradePreventionMode": "NONE"
                }
            ]
        }

        '''
        log.debug('')
        failures, ok, nok = 0, [], []
        for trade in trades:
            order_kwargs = self.unpack(trade, **context)
            if not order_kwargs:
                stdout_msg(f'Failed to unpack Trade() instance!', err=True)
                nok.append(trade)
            try:
                order = self.create_oco_order(**order_kwargs)
            except BinanceAPIException as e:
                stdout_msg(f'Binance API: {e}', err=True)
                nok.append(trade)
                continue
            except BinanceOrderException as e:
                stdout_msg(f'Binance Order: {e}', err=True)
                nok.append(trade)
                continue
            except BinanceRequestException as e:
                stdout_msg(f'Binance Request: {e}', err=True)
                nok.append(trade)
                continue
            except BinanceWebsocketUnableToConnect as e:
                stdout_msg(f'Binance Websocket: {e}', err=True)
                nok.append(trade)
                continue
            except NotImplementedException as e:
                stdout_msg(f'Binance Not Implemenented: {e}', err=True)
                nok.append(trade)
                continue
            except UnknownDateFormat as e:
                stdout_msg(f'Binance Unknown Date Format: {e}', err=True)
                nok.append(trade)
                continue
            except Exception as e:
                nok.append(trade)
                continue
            trade.update(order)
            ok.append(trade)
        return {
            'failures': failures,
            'ok': ok,
            'nok': nok,
        }

# CODE DUMP

#   @pysnooper.snoop()
#   def raw_api_response_convertor(self, raw_value):
#       log.debug('')
#       sanitized = ''.join(list(raw_value)[1:]).replace("'", '')
#       return json.loads(sanitized)

# TODO - DEPRECATED
#   def synced(self, func_name, **kwargs):
#       log.debug('')
#       kwargs['timestamp'] = int(time.time() - self.time_offset)
#       return getattr(self, func_name)(**kwargs)

