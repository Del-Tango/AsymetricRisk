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
from binance.exceptions import (
    BinanceAPIException, BinanceOrderException, BinanceRequestException,
    BinanceWebsocketUnableToConnect, NotImplementedException, UnknownDateFormat,
)
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

#   @pysnooper.snoop()
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

#   @pysnooper.snoop()
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
#   @pysnooper.snoop()
    def scan_indicator_data(self, **context):
        log.debug('TODO - Under construction, building...')
        # TODO - Fetch indicator data from indicator manager
        return {}

#   @pysnooper.snoop()
    def scan_account_data(self, **context):
        log.debug('')
        recv_window = context.get('recv-window', self._context.get('recv-window', 60000))
        ticker = context.get('ticker-symbol', self._context.get('ticker-symbol', str())).replace('/', '')
        scan = {
            'account': self.get_account(recvWindow=recv_window),
            'trading-orders': self.get_all_orders(symbol=ticker, recvWindow=recv_window),
        }
        if context.get('extended'):
            scan.update({
                'deposit-history': self.get_deposit_history(recvWindow=recv_window),
                'status': self.get_account_status(recvWindow=recv_window),
                'withdraw-history': self.get_withdraw_history(recvWindow=recv_window),
            })
        return scan

#   @pysnooper.snoop()
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

#   @pysnooper.snoop()
    def scan_ticker_symbol_data(self, **context):
        '''
        get_ticker(**params)
            24 hour price change statistics.

            https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics

            :param symbol:
            :type symbol: str
            :returns: API response {
                "priceChange": "-94.99999800",
                "priceChangePercent": "-95.960",
                "weightedAvgPrice": "0.29628482",
                "prevClosePrice": "0.10002000",
                "lastPrice": "4.00000200",
                "bidPrice": "4.00000000",
                "askPrice": "4.00000200",
                "openPrice": "99.00000000",
                "highPrice": "100.00000000",
                "lowPrice": "0.10000000",
                "volume": "8913.30000000",
                "openTime": 1499783499040,
                "closeTime": 1499869899040,
                "fristId": 28385,   # First tradeId
                "lastId": 28460,    # Last tradeId
                "count": 76         # Trade count
            }
            OR
            [
                {
                    "priceChange": "-94.99999800",
                    "priceChangePercent": "-95.960",
                    "weightedAvgPrice": "0.29628482",
                    "prevClosePrice": "0.10002000",
                    "lastPrice": "4.00000200",
                    "bidPrice": "4.00000000",
                    "askPrice": "4.00000200",
                    "openPrice": "99.00000000",
                    "highPrice": "100.00000000",
                    "lowPrice": "0.10000000",
                    "volume": "8913.30000000",
                    "openTime": 1499783499040,
                    "closeTime": 1499869899040,
                    "fristId": 28385,   # First tradeId
                    "lastId": 28460,    # Last tradeId
                    "count": 76         # Trade count
                }
            ]
            :raises: BinanceRequestException, BinanceAPIException

        get_symbol_info(symbol) -> Optional[Dict]
            Return information about a symbol
            :param symbol: required e.g BNBBTC
            :type symbol: str
            :returns: Dict if found, None if not {
                "symbol": "ETHBTC",
                "status": "TRADING",
                "baseAsset": "ETH",
                "baseAssetPrecision": 8,
                "quoteAsset": "BTC",
                "quotePrecision": 8,
                "orderTypes": ["LIMIT", "MARKET"],
                "icebergAllowed": false,
                "filters": [
                    {
                        "filterType": "PRICE_FILTER",
                        "minPrice": "0.00000100",
                        "maxPrice": "100000.00000000",
                        "tickSize": "0.00000100"
                    }, {
                        "filterType": "LOT_SIZE",
                        "minQty": "0.00100000",
                        "maxQty": "100000.00000000",
                        "stepSize": "0.00100000"
                    }, {
                        "filterType": "MIN_NOTIONAL",
                        "minNotional": "0.00100000"
                    }
                ]
            }
            :raises: BinanceRequestException, BinanceAPIException

        get_historical_klines(
                symbol, interval, start_str=None, end_str=None, limit=1000,
                klines_type: binance.enums.HistoricalKlinesType = <HistoricalKlinesType.SPOT: 1>)
            Get Historical Klines from Binance
            :param symbol: Name of symbol pair e.g BNBBTC
            :type symbol: str
            :param interval: Binance Kline interval
            :type interval: str
            :param start_str: optional - start date string in UTC format or timestamp
                in milliseconds
            :type start_str: str|int
            :param end_str: optional - end date string in UTC format or timestamp in
                milliseconds (default will fetch everything up to now)
            :type end_str: str|int
            :param limit: Default 1000; max 1000.
            :type limit: int
            :param klines_type: Historical klines type: SPOT or FUTURES
            :type klines_type: HistoricalKlinesType
            :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume,
                Close time, Quote asset volume, Number of trades, Taker buy base asset
                volume, Taker buy quote asset volume, Ignore)

        get_exchange_info() -> Dict
            Return rate limits and list of symbols
            :returns: list - List of product dictionaries {
                "timezone": "UTC",
                "serverTime": 1508631584636,
                "rateLimits": [
                    {
                        "rateLimitType": "REQUESTS",
                        "interval": "MINUTE",
                        "limit": 1200
                    }, {
                        "rateLimitType": "ORDERS",
                        "interval": "SECOND",
                        "limit": 10
                    }, {
                    "rateLimitType": "ORDERS",
                    "interval": "DAY",
                    "limit": 100000
                    }
                ],
                "exchangeFilters": [],
                "symbols": [{
                    "symbol": "ETHBTC",
                    "status": "TRADING",
                    "baseAsset": "ETH",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "orderTypes": ["LIMIT", "MARKET"],
                    "icebergAllowed": false,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "0.00000100",
                            "maxPrice": "100000.00000000",
                            "tickSize": "0.00000100"
                        }, {
                            "filterType": "LOT_SIZE",
                            "minQty": "0.00100000",
                            "maxQty": "100000.00000000",
                            "stepSize": "0.00100000"
                        }, {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": "0.00100000"
                        }
                    ]
                ]}
            }
            :raises: BinanceRequestException, BinanceAPIException

        get_trade_fee(**params)
            Get trade fee.
            https://binance-docs.github.io/apidocs/spot/en/#trade-fee-sapi-user_data
            :param symbol: optional
            :type symbol: str
            :param recvWindow: the number of milliseconds the request is valid for
            :type recvWindow: int
            :returns: API response [
                {
                    "symbol": "ADABNB",
                    "makerCommission": "0.001",
                    "takerCommission": "0.001"
                }, {
                    "symbol": "BNBBTC",
                    "makerCommission": "0.001",
                    "takerCommission": "0.001"
                }
            ]
        '''
        log.debug('')
        recv_window = context.get('recv-window', self._context.get('recv-window', 60000))
        ticker = context.get('ticker-symbol', self._context.get('ticker-symbol', str())).replace('/', '')
        interval = context.get('interval', self._context.get('interval'))
        period = context.get('period', self._context.get('period'))
        scan = {
            'symbol': self.get_ticker(symbol=ticker),
            'info': self.get_symbol_info(ticker),
            'historical-klines': self.get_historical_klines(ticker, interval, limit=period),
            'exchange': self.get_exchange_info(),
        }
        if context.get('extended'):
            scan.update({
                'trade-fee': self.get_trade_fee(symbol=ticker, recvWindow=recv_window),
            })
        return scan

    # GENERAL

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
        log.debug('TODO - Under construction, building...')
        # Validate API keys
        # Run preliminary market scan
#       print(f'[ DEBUG ]: API_KEY {self.API_KEY}')
#       print(f'[ DEBUG ]: API_SECRET {self.API_SECRET}')
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

        [ RESPONSE ]: create_oco_order() -> {
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

        [ RETURN ]: {
            'failures': 0,
            'ok': [Trade(), Trade(), ...],
            'nok': [],
        }

        '''
        log.debug('')
        failures, ok, nok = 0, [], []
        for trade in trades:
            order_kwargs = trade.unpack()
            log.debug(f'Trade order kwargs: {order_kwargs}')
            if not order_kwargs:
                stdout_msg(f'Failed to unpack Trade() instance!', err=True)
                nok.append(trade)
            try:
                order = self.create_order(**order_kwargs)
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
            trade.update(**order)
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


