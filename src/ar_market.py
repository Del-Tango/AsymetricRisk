#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADING MARKET

import os
import logging
import time
# import pandas as pd
# import ta-lib
import pysnooper

from binance.client import Client
from binance import ThreadedWebsocketManager
from src.ar_indicator import TradingIndicator

log = logging.getLogger('AsymetricRisk')


class TradingMarket(Client):

    def __init__(self, *args, sync=False, **kwargs):
        calling_all_ancestors_from_beyond_the_grave = super().__init__(*args)
        self.base_currency = kwargs.get('base-currency', 'BTC')
        self.API_URL = kwargs.get('api-url', 'https://testnet.binance.vision/api')      # Place trades at
        if not self.API_KEY:
            self.API_KEY = kwargs.get('api-key', os.environ.get('binance_api'))
        if not self.API_SECRET:
            self.API_SECRET = kwargs.get('api-secret', os.environ.get('binance_secret'))
        self.quote_currency = kwargs.get('quote-currency', 'ETH')
        self.period_start = kwargs.get('period-start', '1/09/2022')
        self.period_end = kwargs.get('period-end', '1/10/2022')
        self.cache_size_limit = kwargs.get('cache-size-limit', 20)
        self.indicator = TradingIndicator(**kwargs)
        self.time_offset = 0
        self.buy_price = None
        self.sell_price = None
        self.volume = None
        self.adx = None
        self.macd = None
        self.ma = None
        self.rsi = None
        self.vwap = None
        self.active_trades = {} #{id: {<value-key>: <value>}} - {'id': 54569, 'price': '328.30000000', 'qty': '2.02000000', 'quoteQty': '663.16600000', 'time': 1667254909509, 'isBuyerMaker': False, 'isBestMatch': True}
        self.trades_to_report = {} # {id: {<value-key>: <value>}} - {'id': 54569, 'price': '328.30000000', 'qty': '2.02000000', 'quoteQty': '663.16600000', 'time': 1667254909509, 'isBuyerMaker': False, 'isBestMatch': True}
        self.success_count = 0
        self.failure_count = 0
        self.update_details()
        self.recent_trades_cache = {}
        self.account_cache = {}
        self.coin_info_cache = {}
        self.trade_fee_cache = {}
        if sync:
            self.time_offset = self._fetch_time_offset()
        return calling_all_ancestors_from_beyond_the_grave

    # FETCHERS

    def _fetch_time_offset(self):
        res = self.get_server_time()
        return res.get('serverTime') - int(time.time() * 1000)

    # UPDATERS

    def update_cache(self, element, cache_dict, **kwargs):
        size_limit = kwargs.get('size_limit', self.cache_size_limit)
        if len(cache_dict.keys()) > size_limit:
            truncate_cache = truncate_cache(cache_dict, size_limit - 1)
            if not truncate_cache:
                return 1
        label = kwargs.get('label', str(time.time()))
        cache_dict[label] = element
        return cache_dict

    # GENERAL

    def truncate_cache(cache_dict, size_limit):
        if not cache_dict or not isinstance(size_limit, int) or size_limit > len(cache_dict):
            return False
        size_limit -= 1
        keys_to_remove = list(reversed(sorted(cache_dict)))[size_limit:]
        for key in keys_to_remove:
            del cache_dict[key]

    def synced(self, func_name, **args):
        args['timestamp'] = int(time.time() - self.time_offset)
        return getattr(self, func_name)(**args)

    # TODO
    def buy(self, amount, *args, take_profit=None, stop_loss=None, trailing_stop=None, **kwargs):
        return {}

    # TODO
    def sell(self, amount, *args, take_profit=None, stop_loss=None, trailing_stop=None,  **kwargs):
        return {}

    # TODO
    def indicators(self, *indicators):
        return {}

    # TODO
    def close_position(self, *trade_ids):
        return {}

    # TODO
    @pysnooper.snoop()
    def update_details(self):
        log.debug('TODO - Compute indicators')
        timestamp = str(time.time())
        ticker_symbol = str(self.base_currency) \
            + str(self.quote_currency)
        self.update_cache(
            self.get_all_coins_info(recvWindow=60000),
            self.coin_info_cache, label=timestamp,
        )
        for coin_dict in self.coin_info_cache[timestamp]:
            if coin_dict['coin'] != self.base_currency:
                continue
            self.buy_price = coin_dict['bidPrice']
            self.sell_price = coin_dict['askPrice']
            self.volume = coin_dict['volume']
        self.update_cache(
            self.get_trade_fee(symbol=ticker_symbol, recvWindow=60000),
            self.trade_fee_cache, label=timestamp,
        )
#       self.adx = None
#       self.macd = None
#       self.ma = None
#       self.rsi = None
#       self.vwap = None
        return {
            'ticker-symbol': ticker_symbol,
            'buy-price': self.buy_price,
            'sell-price': self.sell_price,
            'volume': self.volume,
            'indicators': {
                'adx': self.adx,
                'macd': self.macd,
                'ma': self.ma,
                'rsi': self.rsi,
                'vwap': self.vwap,
            },
            'caches': {
                'coin-info-cache': self.coin_info_cache,
                'trade-fee-cache': self.trade_fee_cache
            }
        }

# CODE DUMP

#   >>> tmarket.get_symbol_info(symbol='BTCBUSD')
#   {'symbol': 'BTCBUSD', 'status': 'TRADING', 'baseAsset': 'BTC', 'baseAssetPrecision': 8, 'quoteAsset': 'BUSD', 'quotePrecision': 8, 'quoteAssetPrecision': 8, 'baseCommissionPrecision': 8, 'quoteCommissionPrecision': 8, 'orderTypes': ['LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'], 'icebergAllowed': True, 'ocoAllowed': True, 'quoteOrderQtyMarketAllowed': True, 'allowTrailingStop': True, 'cancelReplaceAllowed': True, 'isSpotTradingAllowed': True, 'isMarginTradingAllowed': False, 'filters': [{'filterType': 'PRICE_FILTER', 'minPrice': '0.01000000', 'maxPrice': '1000000.00000000', 'tickSize': '0.01000000'}, {'filterType': 'PERCENT_PRICE', 'multiplierUp': '5', 'multiplierDown': '0.2', 'avgPriceMins': 1}, {'filterType': 'LOT_SIZE', 'minQty': '0.00000100', 'maxQty': '900.00000000', 'stepSize': '0.00000100'}, {'filterType': 'MIN_NOTIONAL', 'minNotional': '10.00000000', 'applyToMarket': True, 'avgPriceMins': 1}, {'filterType': 'ICEBERG_PARTS', 'limit': 10}, {'filterType': 'MARKET_LOT_SIZE', 'minQty': '0.00000000', 'maxQty': '100.00000000', 'stepSize': '0.00000000'}, {'filterType': 'TRAILING_DELTA', 'minTrailingAboveDelta': 10, 'maxTrailingAboveDelta': 2000, 'minTrailingBelowDelta': 10, 'maxTrailingBelowDelta': 2000}, {'filterType': 'MAX_NUM_ORDERS', 'maxNumOrders': 200}, {'filterType': 'MAX_NUM_ALGO_ORDERS', 'maxNumAlgoOrders': 5}], 'permissions': ['SPOT']}

#   >>> tmarket.get_symbol_ticker(symbol='LTCBTC')
#   {'symbol': 'LTCBTC', 'price': '0.00269500'}

#   >>> tmarket.get_system_status()
#   {'status': 0, 'msg': 'normal'}

#   >>> tmarket.get_ticker(symbol='LTCBTC')
#   {'symbol': 'LTCBTC', 'priceChange': '0.00002600', 'priceChangePercent': '0.973', 'weightedAvgPrice': '0.00269486', 'prevClosePrice': '0.00267100', 'lastPrice': '0.00269700', 'lastQty': '2.41009000', 'bidPrice': '0.00269700', 'bidQty': '0.25955000', 'askPrice': '0.00269800', 'askQty': '2.00149000', 'openPrice': '0.00267100', 'highPrice': '0.01342800', 'lowPrice': '0.00264400', 'volume': '7235.01344000', 'quoteVolume': '19.49735839', 'openTime': 1667169088911, 'closeTime': 1667255488911, 'firstId': 39165, 'lastId': 42447, 'count': 3283}

#   >>> tmarket.__dict__
#   {'tld': 'com', 'API_URL': 'https://api.binance.com/api', 'MARGIN_API_URL': 'https://api.binance.com/sapi', 'WEBSITE_URL': 'https://www.binance.com', 'FUTURES_URL': 'https://fapi.binance.com/fapi', 'FUTURES_DATA_URL': 'https://fapi.binance.com/futures/data', 'FUTURES_COIN_URL': 'https://dapi.binance.com/dapi', 'FUTURES_COIN_DATA_URL': 'https://dapi.binance.com/futures/data', 'OPTIONS_URL': 'https://vapi.binance.com/vapi', 'OPTIONS_TESTNET_URL': 'https://testnet.binanceops.com/vapi', 'API_KEY': None, 'API_SECRET': None, 'session': <requests.sessions.Session object at 0xb79470e8>, '_requests_params': None, 'response': <Response [200]>, 'testnet': False, 'timestamp_offset': 0, 'crypto': 'BTC', 'api_url': 'https://testnet.binance.vision/api', 'api_key': None, 'api_secret': None, '': 'ETH', 'period_start': '1/09/2022', 'period_end': '1/10/2022', 'time_offset': 0, 'buy_price': None, 'sell_price': None, 'volume': None, 'adx': None, 'macd': None, 'ma': None, 'rsi': None, 'active_trades': {}, 'trades_to_report': {}, 'success_count': 0, 'failure_count': 0, 'recent_trades_cache': {}, 'account_cache': {}, 'coin_info_cache': {}, 'trade_fee_cache': {}}

#   >>> tmarket.get_avg_price(symbol='LTCBTC')
#   {'mins': 1, 'price': '0.00269300'}

#   >>> tmarket.get_deposit_address('BTC', recvWindow=60000)
#   {'coin': 'BTC', 'address': '13drrqoCBejjPjM6tgFbYEf11dUSToKqcP', 'tag': '', 'url': 'http://blockchain.coinmarketcap.com/address/bitcoin/13drrqoCBejjPjM6tgFbYEf11dUSToKqcP'}

#   >>> tmarket.get_orderbook_tickers()
#   [{'symbol': 'BNBBUSD', 'bidPrice': '328.50000000', 'bidQty': '2.08000000', 'askPrice': '328.60000000', 'askQty': '2.93000000'}, {'symbol': 'BTCBUSD', 'bidPrice': '20483.00000000', 'bidQty': '0.02733900', 'askPrice': '20483.08000000', 'askQty': '0.03222200'}, {'symbol': 'ETHBUSD', 'bidPrice': '1567.61000000', 'bidQty': '0.55499000', 'askPrice': '1567.80000000', 'askQty': '0.45287000'}, {'symbol': 'LTCBUSD', 'bidPrice': '55.13000000', 'bidQty': '17.95756000', 'askPrice': '55.14000000', 'askQty': '9.24919000'}, {'symbol': 'TRXBUSD', 'bidPrice': '0.06325000', 'bidQty': '4425.50000000', 'askPrice': '0.06326000', 'askQty': '11855.90000000'}, {'symbol': 'XRPBUSD', 'bidPrice': '0.46270000', 'bidQty': '367.50000000', 'askPrice': '0.46280000', 'askQty': '2009.60000000'}, {'symbol': 'BNBUSDT', 'bidPrice': '328.60000000', 'bidQty': '6.21000000', 'askPrice': '328.70000000', 'askQty': '8.22000000'}, {'symbol': 'BTCUSDT', 'bidPrice': '20484.79000000', 'bidQty': '0.13961600', 'askPrice': '20485.22000000', 'askQty': '0.08251000'}, {'symbol': 'ETHUSDT', 'bidPrice': '1567.86000000', 'bidQty': '0.01891000', 'askPrice': '1567.87000000', 'askQty': '0.32529000'}, {'symbol': 'LTCUSDT', 'bidPrice': '55.13000000', 'bidQty': '13.78560000', 'askPrice': '55.14000000', 'askQty': '9.24919000'}, {'symbol': 'TRXUSDT', 'bidPrice': '0.06325000', 'bidQty': '316.20000000', 'askPrice': '0.06326000', 'askQty': '15333.60000000'}, {'symbol': 'XRPUSDT', 'bidPrice': '0.46270000', 'bidQty': '1491.30000000', 'askPrice': '0.46290000', 'askQty': '1512.30000000'}, {'symbol': 'BNBBTC', 'bidPrice': '0.01604000', 'bidQty': '0.38000000', 'askPrice': '0.01604100', 'askQty': '0.50000000'}, {'symbol': 'ETHBTC', 'bidPrice': '0.07654100', 'bidQty': '0.08493000', 'askPrice': '0.07654200', 'askQty': '0.11367000'}, {'symbol': 'LTCBTC', 'bidPrice': '0.00269100', 'bidQty': '1.15199000', 'askPrice': '0.00269200', 'askQty': '3.67757000'}, {'symbol': 'TRXBTC', 'bidPrice': '0.00000308', 'bidQty': '714.30000000', 'askPrice': '0.00000309', 'askQty': '2880.30000000'}, {'symbol': 'XRPBTC', 'bidPrice': '0.00002258', 'bidQty': '84.10000000', 'askPrice': '0.00002260', 'askQty': '433.70000000'}, {'symbol': 'LTCBNB', 'bidPrice': '0.16770000', 'bidQty': '47.10794000', 'askPrice': '0.16790000', 'askQty': '33.35319000'}, {'symbol': 'TRXBNB', 'bidPrice': '0.00019240', 'bidQty': '30665.30000000', 'askPrice': '0.00019250', 'askQty': '35324.70000000'}, {'symbol': 'XRPBNB', 'bidPrice': '0.00140800', 'bidQty': '6605.20000000', 'askPrice': '0.00140900', 'askQty': '4755.20000000'}]

#   >>> tmarket.get_recent_trades(symbol='BTCBUSD')
#   [{'id': 2807808, 'price': '20480.61000000', 'qty': '0.00729900', 'quoteQty': '149.48797239', 'time': 1667258293022, 'isBuyerMaker': True, 'isBestMatch': True}, {'id': 2807809, 'price': '20480.27000000', 'qty': '0.01469400', 'quoteQty': '30 0.93708738', 'time': 1667258293022, 'isBuyerMaker': True, 'isBestMatch': True},

#   >>> tmarket.get_trade_fee(symbol='ETHBTC', recvWindow=60000)
#   [{'symbol': 'ETHBTC', 'makerCommission': '0.001', 'takerCommission': '0.001'}]

#   >>> tmarket.get_all_coins_info(recvWindow=60000)
#   [{'coin': 'XMR', 'depositAllEnable': True, 'withdrawAll
#    Enable': False, 'name': 'Monero', 'free': '0', 'locked': '0', 'freeze': '0', 'withdrawing': '0', 'ipoing': '0', 'ipoable': '0', 'storage': '0', 'isLegalMoney': False, 'trading': True, 'networkList': [{'network': 'XMR', 'coin': 'XMR', 'with
#    drawIntegerMultiple': '0.00000001', 'isDefault': True, 'depositEnable': True, 'withdrawEnable': False, 'depositDesc': '', 'withdrawDesc': 'Withdrawals are temporarily halted while Binance replenishes the hot wallet. Withdrawals for this as
#    set will be resumed shortly.', 'specialTips': '', 'name': 'Monero', 'resetAddressStatus': False, 'addressRegex': '^[48][a-zA-Z|\\d]{94}([a-zA-Z|\\d]{11})?$', 'addressRule': '', 'memoRegex': '', 'withdrawFee': '0.0001', 'withdrawMin': '0.00
#    02', 'withdrawMax': '10000000000', 'minConfirm': 3, 'unLockConfirm': 0,
#    'sameAddress': False, 'estimatedArrivalTime': 10, 'busy': False,
#    'country': 'BINANCE_BAHRAIN_BSC'}]}]

#   >>> tmarket.get_account_status(recvWindow=60000)
#   {'data': 'Normal'}

#   >>> tmarket.get_account_snapshot(type='SPOT', recvWindow=60000)
#   {'code': 200, 'msg': '', 'snapshotVos': []}

#   >>> tmarket.get_account_api_trading_status(recvWindow=60000)
#   {'data': {'isLocked': False, 'plannedRecoverTime': 0, 'triggerCondition': {'UFR': 300, 'IFER': 150, 'GCR': 150}, 'updateTime': 0}}

#   >>> tmarket.get_account_api_permissions(recvWindow=60000)
#   {'ipRestrict': False, 'createTime': 1667239846000, 'tradingAuthorityExpirationTime': 1674950400000, 'enableSpotAndMarginTrading': True, 'enableWithdrawals': False, 'enableReading': True, 'enableMargin': False, 'permitsUniversalTransfer': True, 'enableVanillaOptions': True, 'enableInternalTransfer': False, 'enableFutures': False}

#   >>> tmarket.get_exchange_info()
#   {'timezone': 'UTC', 'serverTime': 1667259716606, 'rateLimits': [{'rateLimitType': 'REQUEST_WEIGHT', 'interval': 'MINUTE', 'intervalNum': 1, 'limit': 1200}, {'rateLimitType': 'ORDERS', 'interval': 'SECOND', 'intervalNum': 10, 'limit': 50},
#   {'rateLimitType': 'ORDERS', 'interval': 'DAY', 'intervalNum': 1, 'limit': 160000}], 'exchangeFilters': [], 'symbols': [{'symbol': 'BNBBUSD', 'status': 'TRADING', 'baseAsset': 'BNB', 'baseAssetPrecision': 8, 'quoteAsset': 'BUSD', 'quotePrec
#   ision': 8, 'quoteAssetPrecision': 8, 'baseCommissionPrecision': 8, 'quoteCommissionPrecision': 8, 'orderTypes': ['LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'], 'icebergAllowed': True, 'ocoAllowed': True, 'quoteO
#   rderQtyMarketAllowed': True, 'allowTrailingStop': True, 'cancelReplaceAllowed': True, 'isSpotTradingAllowed': True, 'isMarginTradingAllowed': False, 'filters': [{'filterType': 'PRICE_FILTER', 'minPrice': '0.01000000', 'maxPrice': '10000.00
#   000000', 'tickSize': '0.01000000'}, {'filterType': 'PERCENT_PRICE', 'multiplierUp': '5', 'multiplierDown': '0.2', 'avgPriceMins': 1}, {'filterType': 'LOT_SIZE', 'minQty': '0.01000000', 'maxQty': '9000.00000000', 'stepSize': '0.01000000'},
#   {'filterType': 'MIN_NOTIONAL', 'minNotional': '10.00000000', 'applyToMarket': True, 'avgPriceMins': 1}, {'filterType': 'ICEBERG_PARTS', 'limit': 10}, {'filterType': 'MARKET_LOT_SIZE', 'minQty>>> tmarket.get_exchange_info()
#   {'timezone': 'UTC', 'serverTime': 1667259716606, 'rateLimits': [{'rateLimitType': 'REQUEST_WEIGHT', 'interval': 'MINUTE', 'intervalNum': 1, 'limit': 1200}, {'rateLimitType': 'ORDERS', 'interval': 'SECOND', 'intervalNum': 10, 'limit': 50},
#   {'rateLimitType': 'ORDERS', 'interval': 'DAY', 'intervalNum': 1, 'limit': 160000}], 'exchangeFilters': [], 'symbols': [{'symbol': 'BNBBUSD', 'status': 'TRADING', 'baseAsset': 'BNB', 'baseAssetPrecision': 8, 'quoteAsset': 'BUSD', 'quotePrec
#   ision': 8, 'quoteAssetPrecision': 8, 'baseCommissionPrecision': 8, 'quoteCommissionPrecision': 8, 'orderTypes': ['LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'], 'icebergAllowed': True, 'ocoAllowed': True, 'quoteO
#   rderQtyMarketAllowed': True, 'allowTrailingStop': True, 'cancelReplaceAllowed': True, 'isSpotTradingAllowed': True, 'isMarginTradingAllowed': False, 'filters': [{'filterType': 'PRICE_FILTER', 'minPrice': '0.01000000', 'maxPrice': '10000.00
#   000000', 'tickSize': '0.01000000'}, {'filterType': 'PERCENT_PRICE', 'multiplierUp': '5', 'multiplierDown': '0.2', 'avgPriceMins': 1}, {'filterType': 'LOT_SIZE', 'minQty': '0.01000000', 'maxQty': '9000.00000000', 'stepSize': '0.01000000'},
#   {'filterType': 'MIN_NOTIONAL', 'minNotional': '10.00000000', 'applyToMarket': True, 'avgPriceMins': 1}, {'filterType': 'ICEBERG_PARTS', 'limit': 10}, {'filterType': 'MARKET_LOT_SIZE', 'minQty




