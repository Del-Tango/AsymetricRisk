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

from binance.client import Client
from binance import ThreadedWebsocketManager
from src.ar_indicator import TradingIndicator

log = logging.getLogger('AsymetricRisk')


class TradingMarket(Client):

#   @pysnooper.snoop()
    def __init__(self, *args, sync=False, **kwargs):
        calling_all_ancestors_from_beyond_the_grave = super().__init__(*args)
        self.base_currency = kwargs.get('base-currency', 'BTC')
        self.API_URL = kwargs.get('api-url', 'https://testnet.binance.vision/api')      # Place trades at
        if not self.API_KEY:
            self.API_KEY = kwargs.get('api-key', os.environ.get('binance_api'))
        if not self.API_SECRET:
            self.API_SECRET = kwargs.get('api-secret', os.environ.get('binance_secret'))
        self.taapi_key = kwargs.get('taapi-key', os.environ.get('taapi_api'))
        self.quote_currency = kwargs.get('quote-currency', 'USDT')
        self.ticker_symbol = kwargs.get(
            'ticker-symbol', self.compute_ticker_symbol(
                base=self.base_currency, quote=self.quote_currency
            ) # 'BTC/USDT'
        )
        self.period_interval = kwargs.get('period-interval', '1h')
        self.cache_size_limit = kwargs.get('cache-size-limit', 20)
        self.indicator_update_delay = kwargs.get('indicator-update-delay', 18)  # seconds
        # WARNING: Longer delays between indicator api calls will result in
        # longer execution time. Delays that are too short may not retreive all
        # necessary data (depending on chosen Taapi API plan specifications)
        self.indicator = TradingIndicator(**kwargs)
        self.time_offset = 0
        self.buy_price = float()
        self.sell_price = float()
        self.volume = float()
        self.adx = float()
        self.macd = float()
        self.macd_signal = float()
        self.macd_hist = float()
        self.ma = float()
        self.ema = float()
        self.rsi = float()
        self.vwap = float()
        self.last_indicator_update_timestamp = None
        self.success_count = 0
        self.failure_count = 0
        self.active_trades = {} #{id: {<value-key>: <value>}} - {'id': 54569, 'price': '328.30000000', 'qty': '2.02000000', 'quoteQty': '663.16600000', 'time': 1667254909509, 'isBuyerMaker': False, 'isBestMatch': True}
        self.trades_to_report = {} # {id: {<value-key>: <value>}} - {'id': 54569, 'price': '328.30000000', 'qty': '2.02000000', 'quoteQty': '663.16600000', 'time': 1667254909509, 'isBuyerMaker': False, 'isBestMatch': True}
        self.supported_tickers_cache = {}
        self.supported_coins_cache = {}
        self.recent_trades_cache = {}
        self.account_cache = {}
        self.coin_info_cache = {}
        self.ticker_info_cache = {}
        self.trade_fee_cache = {}
        self.history_cache = {}
        if sync:
            self.time_offset = self._fetch_time_offset()
        self.update_details('all')
        return calling_all_ancestors_from_beyond_the_grave

    # FETCHERS

    def fetch_details(self, *args, **kwargs):
        '''
        [ NOTE ]: Fetch market details
        [ RETURN ]: {
            "ticker-symbol": "BTC/USDT",
            "interval": "5m",
            "history": {
                "buy-price": [{"value": 16634.68, "backtrack": 1}, ...],
                "sell-price": [{}, ],
                "volume": [{}, ],
                "adx": [{}, ],
                "macd": [{}, ],
                "macd-signal": [{}, ],
                "macd-hist": [{}, ],
                "ma": [{}, ],
                "ema": [{}, ],
                "rsi": [{}, ],
                "vwap": [{}, ]
            },
            "buy-price": 16634.68,
            "sell-price": 16634.79,
            "volume": 113695.42224,
            "indicators": {
                "adx": 15.579493600436063,
                "macd": -3.179918018162425,
                "macd-signal": -6.485571811770549,
                "macd-hist": 3.3056537936081236,
                "ma": 16634.81933333334,
                "ema": 16633.394949095054,
                "rsi": 53.52208448310394,
                "vwap": 16632.333673366094
                }
            }
        '''
        log.debug('')
        return self.update_details(*args, **kwargs)

    def fetch_account(self, *args, **kwargs):
        log.debug('')
        timestamp = str(time.time())
        self.update_cache(
            self.get_account(recvWindow=kwargs.get('recvWindow', 60000)),
            self.account_cache,
            label=timestamp
        )
        return self.account_cache[timestamp]

    def fetch_asset_balance(self, *args, **kwargs):
        log.debug('')
        account = self.fetch_account(**kwargs)
        return account.get('balances', False)

#   @pysnooper.snoop()
    def fetch_supported_coins(self, *args, **kwargs):
        log.debug('')
        merged = {}
        coins = self.get_all_coins_info(
            recvWindow=kwargs.get('recvWindow', 60000)
        )
        log.debug('Supported crypto coins: {}'.format(coins))
        for coin in coins:
            merged.update({coin.get('coin'): coin,})
        timestamp = str(time.time())
        self.update_cache(
            merged, self.supported_coins_cache, label=timestamp,
        )
        return merged

#   @pysnooper.snoop()
    def fetch_supported_tickers(self, *args, **kwargs):
        log.debug('')
        tickers, merged = self.get_all_tickers(), {}
        log.debug('Supported ticker symbols: {}'.format(tickers))
        for ticker_dict in tickers:
            merged.update({ticker_dict.get('symbol'): ticker_dict,})
        timestamp = str(time.time())
        self.update_cache(
            merged, self.supported_tickers_cache, label=timestamp,
        )
        return merged

    def fetch_active_trades(self, *args, **kwargs):
        log.debug('')
        all_trades = self.fetch_all_trades(*args, **kwargs)
        active_trades = {}
        for key in all_trades:
            active_trades[key] = [
                item for item in all_trades[key] if item.get('status') == 'NEW'
            ]
        log.debug('Active trades: {}'.format(active_trades))
        return active_trades

    def fetch_all_trades(self, *args, **kwargs):
        '''
        [ INPUT ]: *args - ticker symbols to get trades for
                   **kwargs - orderId (type int) - Unique order ID
                            - startTime (type int) - Optional
                            - endTime (type int) - Optional
                            - limit (type int) - Default 500, max 1000
        [ RETURN ]: Dict with all trades grouped by ticker symbol
        '''
        log.debug('')
        records = {}
        for ticker_symbol in args:
            timestamp = str(time.time())
            self.update_cache(
                self.get_all_orders(
                    symbol=ticker_symbol, recvWindow=60000, **kwargs
                ),
                self.recent_trades_cache, label=timestamp,
            )
            records.update(
                {ticker_symbol: self.recent_trades_cache[timestamp]}
            )
        log.debug('All trades: {}'.format(records))
        return records

    def fetch_macd_values(self, **kwargs):
        log.debug('')
        self.ensure_indicator_delay()
        raw_value = self.indicator.macd(**self.format_macd_indicator_kwargs(**kwargs))
        if not raw_value:
            return False
        self.update_indicator_timestamp()
        value_dict = self.raw_api_response_to_dict(raw_value)
        return value_dict.get('valueMACD', False), \
            value_dict.get('valueMACDSignal', False), \
            value_dict.get('valueMACDHist', False)

    def fetch_adx_value(self, **kwargs):
        log.debug('')
        self.ensure_indicator_delay()
        raw_value = self.indicator.adx(**self.format_adx_indicator_kwargs(**kwargs))
        if not raw_value:
            return False
        self.update_indicator_timestamp()
        return self.raw_api_response_to_dict(raw_value).get('value', False)

    def fetch_ma_value(self, **kwargs):
        log.debug('')
        self.ensure_indicator_delay()
        raw_value = self.indicator.ma(**self.format_ma_indicator_kwargs(**kwargs))
        if not raw_value:
            return False
        self.update_indicator_timestamp()
        return self.raw_api_response_to_dict(raw_value).get('value', False)

    def fetch_ema_value(self, **kwargs):
        log.debug('')
        self.ensure_indicator_delay()
        raw_value = self.indicator.ema(**self.format_ema_indicator_kwargs(**kwargs))
        if not raw_value:
            return False
        self.update_indicator_timestamp()
        return self.raw_api_response_to_dict(raw_value).get('value', False)

    def fetch_rsi_value(self, **kwargs):
        log.debug('')
        self.ensure_indicator_delay()
        raw_value = self.indicator.rsi(**self.format_rsi_indicator_kwargs(**kwargs))
        if not raw_value:
            return False
        self.update_indicator_timestamp()
        return self.raw_api_response_to_dict(raw_value).get('value', False)

    def fetch_vwap_value(self, **kwargs):
        log.debug('')
        self.ensure_indicator_delay()
        raw_value = self.indicator.vwap(**self.format_vwap_indicator_kwargs(**kwargs))
        if not raw_value:
            return False
        self.update_indicator_timestamp()
        return self.raw_api_response_to_dict(raw_value).get('value', False)

    def _fetch_time_offset(self):
        log.debug('')
        res = self.get_server_time()
        return res.get('serverTime') - int(time.time() * 1000)

    # FORMATTERS

    def format_general_indicator_kwargs(self, **kwargs):
        log.debug('')
        return {
            'exchange': kwargs.get('exchange', 'binance'),
            'symbol': kwargs.get('ticker-symbol', self.ticker_symbol),
            'interval': kwargs.get('interval', self.period_interval),
        }

    def format_macd_indicator_kwargs(self, **kwargs):
        log.debug('')
        return_dict = self.format_general_indicator_kwargs()
        return_dict.update({
            'interval': kwargs.get('macd-interval', kwargs.get('interval', self.period_interval)),
            'backtrack': kwargs.get('macd-backtrack', 5),
            'backtracks': kwargs.get('macd-backtracks', 12),
            'chart': kwargs.get('macd-chart', 'candles'),
            'optInFastPeriod': kwargs.get('macd-fast-period', 12),
            'optInSlowPeriod': kwargs.get('macd-slow-period', 26),
            'optInSignalPeriod': kwargs.get('macd-signal-period', 9),
        })
        return return_dict

    def format_adx_indicator_kwargs(self, **kwargs):
        log.debug('')
        return_dict = self.format_general_indicator_kwargs()
        return_dict.update({
            'interval': kwargs.get('adx-interval', kwargs.get('interval', self.period_interval)),
            'period': kwargs.get('adx-period', 14),
            'backtrack': kwargs.get('adx-backtrack', 5),
            'backtracks': kwargs.get('adx-backtracks', 12),
            'chart': kwargs.get('adx-chart', 'candles'),
        })
        return return_dict

    def format_ma_indicator_kwargs(self, **kwargs):
        log.debug('')
        return_dict = self.format_general_indicator_kwargs()
        return_dict.update({
            'interval': kwargs.get('ma-interval', kwargs.get('interval', self.period_interval)),
            'period': kwargs.get('ma-period', 30),
            'backtrack': kwargs.get('ma-backtrack', 5),
            'backtracks': kwargs.get('ma-backtracks', 12),
            'chart': kwargs.get('ma-chart', 'candles'),
        })
        return return_dict

    def format_ema_indicator_kwargs(self, **kwargs):
        log.debug('')
        return_dict = self.format_general_indicator_kwargs()
        return_dict.update({
            'interval': kwargs.get('ema-interval', kwargs.get('interval', self.period_interval)),
            'period': kwargs.get('ema-period', 30),
            'backtrack': kwargs.get('ema-backtrack', 5),
            'backtracks': kwargs.get('ema-backtracks', 12),
            'chart': kwargs.get('ema-chart', 'candles'),
        })
        return return_dict

    def format_rsi_indicator_kwargs(self, **kwargs):
        log.debug('')
        return_dict = self.format_general_indicator_kwargs()
        return_dict.update({
            'interval': kwargs.get('rsi-interval', kwargs.get('interval', self.period_interval)),
            'period': kwargs.get('rsi-period', 30),
            'backtrack': kwargs.get('rsi-backtrack', 5),
            'backtracks': kwargs.get('rsi-backtracks', 12),
            'chart': kwargs.get('rsi-chart', 'candles'),
        })
        return return_dict

    def format_vwap_indicator_kwargs(self, **kwargs):
        log.debug('')
        return_dict = self.format_general_indicator_kwargs()
        return_dict.update({
            'interval': kwargs.get('vwap-interval', kwargs.get('interval', self.period_interval)),
            'period': kwargs.get('vwap-period', 30),
            'backtrack': kwargs.get('vwap-backtrack', 5),
            'backtracks': kwargs.get('vwap-backtracks', 12),
            'chart': kwargs.get('vwap-chart', 'candles'),
        })
        return return_dict

    # GENERAL

    # TODO - add take profit and stop loss / trailing stop limits
    @pysnooper.snoop()
    def buy(self, amount, *args, take_profit=None, stop_loss=None,
            trailing_stop=None, **kwargs):
        log.debug('TODO - Under construction, building...')
        sanitized_ticker = self.ticker_symbol.replace('/', '')
        if kwargs.get('test'):
            stdout_msg('Creating test buy order...', info=True)
            order = self.create_test_order(
                symbol=sanitized_ticker,
                side=self.SIDE_BUY,
                type=self.ORDER_TYPE_MARKET,
                quoteOrderQty=amount,
                newOrderRespType=kwargs.get('newOrderRespType', 'JSON'),
                recvWindow=kwargs.get('recvWindow', 60000),
            )
        else:
            stdout_msg('Creating buy order...', info=True)
            order = self.create_order(
                symbol=sanitized_ticker,
                side=self.SIDE_BUY,
                type=self.ORDER_TYPE_MARKET,
                quoteOrderQty=amount,
                newOrderRespType=kwargs.get('newOrderRespType', 'JSON'),
                recvWindow=kwargs.get('recvWindow', 60000),
            )
        return order

    # TODO - add take profit and stop loss / trailing stop limits
    @pysnooper.snoop()
    def sell(self, amount, *args, take_profit=None, stop_loss=None,
             trailing_stop=None,  **kwargs):
        log.debug('TODO - Under construction, building...')
        sanitized_ticker = self.ticker_symbol.replace('/', '')
        if kwargs.get('test'):
            stdout_msg('Creating test sell order...', info=True)
            order = self.create_test_order(
                symbol=sanitized_ticker,
                side=self.SIDE_SELL,
                type=self.ORDER_TYPE_MARKET,
                quoteOrderQty=amount,
                newOrderRespType=kwargs.get('newOrderRespType', 'JSON'),
                recvWindow=kwargs.get('recvWindow', 60000),
            )
        else:
            stdout_msg('Creating sell order...', info=True)
            order = self.create_order(
                symbol=sanitized_ticker,
                side=self.SIDE_SELL,
                type=self.ORDER_TYPE_MARKET,
                quoteOrderQty=amount,
                newOrderRespType=kwargs.get('newOrderRespType', 'JSON'),
                recvWindow=kwargs.get('recvWindow', 60000),
            )
        return order

    def compute_ticker_symbol(self, base=None, quote=None):
        log.debug('')
        return str(base) + '/' + str(quote)

    def raw_api_response_to_dict(self, raw_value):
        log.debug('')
        sanitized = ''.join(list(raw_value)[1:]).replace("'", '')
        return json.loads(sanitized)

    def truncate_cache(cache_dict, size_limit):
        log.debug('')
        if not cache_dict or not isinstance(size_limit, int) \
                or size_limit > len(cache_dict):
            return False
        size_limit -= 1
        keys_to_remove = list(reversed(sorted(cache_dict)))[size_limit:]
        for key in keys_to_remove:
            del cache_dict[key]

    def synced(self, func_name, **args):
        log.debug('')
        args['timestamp'] = int(time.time() - self.time_offset)
        return getattr(self, func_name)(**args)

    def close_position(self, *args, **kwargs):
        '''
        [ INPUT ]: *args    - trade ID's (type int)
                   **kwargs - symbol (type str) - ticker symbol, default is
                              active market
                            - recvWindow (type int) - binance API response
                              window, default is 60000
        [ RETURN ]: Closed trades (type lst), failed closes (type lst)
        '''
        log.debug('')
        if not args:
            stdout_msg(
                'No trade ID\'s given to close positions for!', err=True
            )
            return False
        closed_trade, failed_close = [], []
        stdout_msg('Closing trades... {}'.format(args), info=True)
        for trade_id in args:
            close = cancel_order(**{
                'symbol': kwargs.get('symbol', self.ticker_symbol),
                'orderId': trade_id,
                'recvWindow': kwargs.get('recvWindow', 60000),
            })
            if not close:
                failed_close.append(trade_id)
                stdout_msg(
                    'Something went wrong! Could not close trade ({})'
                    .format(trade_id), nok=True
                )
                continue
            closed_trade.append(trade_id)
            stdout_msg(
                'Trade position closed! ({})'.format(trade_id), ok=True
            )
        return closed_trade, failed_close

    # ENSURANCE

    def ensure_indicator_delay(self):
        log.debug('')
        if not self.last_indicator_update_timestamp:
            return True
        while True:
            now = datetime.datetime.now()
            difference = now - self.last_indicator_update_timestamp
            if difference.seconds < self.indicator_update_delay:
                continue
            break
        return True

    # UPDATERS

    # TODO
    def update_indicator_history(self, *update_targets,
                                 timestamp=str(time.time()), **kwargs):
        log.debug('TODO - Under construction, building...')
        return_dict = {}
#       if 'all' in update_targets or 'indicators' in update_targets \
#               or 'adx' in update_targets:
#           return_dict['adx'] = [{}]
#       if 'all' in update_targets or 'indicators' in update_targets \
#               or 'macd' in update_targets:
#           return_dict['macd'] = [{}]
#           return_dict['macd-hist'] = [{}]
#           return_dict['macd-signal'] = [{}]
#       if 'all' in update_targets or 'indicators' in update_targets \
#               or 'ma' in update_targets:
#           return_dict['ma'] = [{}]
#       if 'all' in update_targets or 'indicators' in update_targets \
#               or 'ema' in update_targets:
#           return_dict['ema'] = [{}]
#       if 'all' in update_targets or 'indicators' in update_targets \
#               or 'rsi' in update_targets:
#           return_dict['rsi'] = [{}]
#       if 'all' in update_targets or 'indicators' in update_targets \
#               or 'vwap' in update_targets:
#           return_dict['vwap'] = [{}]
        return return_dict
    def update_price_volume_history(self, *update_targets,
                                    timestamp=str(time.time()), **kwargs):
        log.debug('TODO - Under construction, building...')
        return_dict = {'buy-price': [], 'sell-price': [], 'volume': []}
#       if 'all' in update_targets or 'price' in update_targets:
#           return_dict['buy-price'] = [{'value':, 'backtrack': ,}]
#           return_dict['sell-price'] = [{'value':, 'backtrack': ,}]
#       if 'all' in update_targets or 'volume' in update_targets:
#           return_dict['volume'] = [{'value':, 'backtrack': ,}]
        return return_dict

    def update_indicator_timestamp(self):
        log.debug('')
        self.last_indicator_update_timestamp = datetime.datetime.now()
        log.debug(
            'Last indicator update at ({})'.format(
                self.last_indicator_update_timestamp
            )
        )
        return self.last_indicator_update_timestamp

    def update_cache(self, element, cache_dict, **kwargs):
        log.debug('')
        size_limit = kwargs.get('size_limit', self.cache_size_limit)
        if len(cache_dict.keys()) > size_limit:
            truncate_cache = truncate_cache(cache_dict, size_limit - 1)
            if not truncate_cache:
                return 1
        label = kwargs.get('label', str(time.time()))
        cache_dict[label] = element
        log.debug('Updated cache - {}: {}'.format(cache_dict[label], element))
        return cache_dict

    def update_coin_details(self, timestamp=str(time.time()), **kwargs):
        log.debug('')
        self.update_cache(
            self.get_all_coins_info(recvWindow=60000),
            self.coin_info_cache, label=timestamp,
        )
        return {'coin-info-cache': self.coin_info_cache}

    def update_trade_fee_details(self, timestamp=str(time.time()), **kwargs):
        log.debug('')
        self.update_cache(
            self.get_trade_fee(symbol=self.ticker_symbol, recvWindow=60000),
            self.trade_fee_cache, label=timestamp,
        )
        return {'trade-fee-cache': self.trade_fee_cache}

#   @pysnooper.snoop()
    def update_price_volume_details(self, *update_targets,
                                    timestamp=str(time.time()), **kwargs):
        log.debug('')
        return_dict = {}
        self.update_cache(
            self.get_ticker(symbol=self.ticker_symbol.replace('/', '')),
            self.ticker_info_cache, label=timestamp,
        )
        if 'all' in update_targets or 'price' in update_targets:
            self.buy_price = float(
                self.ticker_info_cache[timestamp].get('bidPrice')
            )
            self.sell_price = float(
                self.ticker_info_cache[timestamp].get('askPrice')
            )
            return_dict.update(
                {'buy-price': self.buy_price, 'sell-price': self.sell_price}
            )
        if 'all' in update_targets or 'volume' in update_targets:
            self.volume = float(
                self.ticker_info_cache[timestamp].get('volume')
            )
            return_dict.update({'volume': self.volume})
        return return_dict

#   @pysnooper.snoop()
    def update_indicator_details(self, *update_targets,
                                 timestamp=str(time.time()), **kwargs):
        log.debug('')
        return_dict = {'indicators': {}}
        if 'all' in update_targets or 'indicators' in update_targets \
                or 'adx' in update_targets:
            self.adx = self.fetch_adx_value(**kwargs)
            return_dict['indicators'].update({'adx': self.adx})
        if 'all' in update_targets or 'indicators' in update_targets \
                or 'macd' in update_targets:
            self.macd, self.macd_signal, self.macd_hist = self.fetch_macd_values(
                **kwargs
            )
            return_dict['indicators'].update({
                'macd': self.macd, 'macd-signal': self.macd_signal,
                'macd-hist': self.macd_hist
            })
        if 'all' in update_targets or 'indicators' in update_targets \
                or 'ma' in update_targets:
            self.ma = self.fetch_ma_value(**kwargs)
            return_dict['indicators'].update({'ma': self.ma})
        if 'all' in update_targets or 'indicators' in update_targets \
                or 'ema' in update_targets:
            self.ema = self.fetch_ema_value(**kwargs)
            return_dict['indicators'].update({'ema': self.ema})
        if 'all' in update_targets or 'indicators' in update_targets \
                or 'rsi' in update_targets:
            self.rsi = self.fetch_rsi_value(**kwargs)
            return_dict['indicators'].update({'rsi': self.rsi})
        if 'all' in update_targets or 'indicators' in update_targets \
                or 'vwap' in update_targets:
            self.vwap = self.fetch_vwap_value(**kwargs)
            return_dict['indicators'].update({'vwap': self.vwap})
        return return_dict

#   @pysnooper.snoop()
    def update_details(self, *args, **kwargs):
        '''
        [ INPUT  ]: *(
                coin, price, volume, trade-fee, indicators, macd, adx, vwap, rsi,
                ma, ema, all, vwap
            )
            **{
                'interval': 5m,
                'rsi-period': 14,
                'rsi-backtrack': 5,
                'rsi-backtracks': 12,
                'rsi-chart': candles,
                'rsi-interval': 5m,
                'volume-movement': 5%,
                'volume-interval': 5m,
                'ma-period': 30,
                'ma-backtrack': 5,
                'ma-backtracks': 12,
                'ma-chart': candles,
                'ma-interval': 5m,
                'ema-period': 30,
                'ema-backtrack': 5,
                'ema-backtracks': 12,
                'ema-chart': candles,
                'ema-interval': 5m,
                'macd-backtrack': 5,
                'macd-backtracks': 12,
                'macd-chart': candles,
                'macd-fast-period': 12,
                'macd-slow-period': 26,
                'macd-signal-period': 9,
                'macd-interval': 5m,
                'adx-period': 14,
                'adx-backtrack': 5,
                'adx-backtracks': 12,
                'adx-chart': candles,
                'adx-interval': 5m,
                'vwap-period': 14,
                'vwap-backtrack': 5,
                'vwap-backtracks': 12,
                'vwap-chart': candles,
                'vwap-interval': 5m,
            }

        [ RETURN ]: Dict with updated values - {
            'ticker-symbol': 'BTC/USDT',
            'buy-price': 20903.77,
            'sell-price': 20904.5,
            'volume': 7270.56273,
            'interval': '1h'
            'indicators': {
                'adx': 25.79249660682844,
                'macd': -55.08962670456458,
                'macd-signal': -18.088430567653305,
                'macd-hist': -37.001196136911275,
                'ma': 21216.220666666643,
                'ema': 21216.220700066643,
                'rsi': 25.931456303405913,
                'vwap': 20592.650164735693
            },
            'history': {
                'adx': [{
                    'value': 25.79249660682844,
                    'backtrack': 1,
                }, ...]
                'macd': [{
                    'value': -55.08962670456458,
                    'backtrack': 1,
                }, ...]
                'macd-signal': [{
                    'value': -18.088430567653305,
                    'backtrack': 1,
                }, ...]
                'macd-hist': [{
                    'value': -37.001196136911275,
                    'backtrack': 1,
                }, ...]
                'ma': [{
                    'value': 21216.220666666643,
                    'backtrack': 1,
                }, ...]
                'ema': [{
                    'value': 21216.220700066643,
                    'backtrack': 1,
                }, ...]
                'rsi': [{
                    'value': 25.931456303405913,
                    'backtrack': 1,
                }, ...]
                'vwap': [{
                    'value': 20592.650164735693,
                    'backtrack': 1,
                }, ...]
                'buy-price': [{
                    'value': 20903.77,
                    'backtrack': 1,
                }, ...]
                'sell-price': [{
                    'value': 20904.5,
                    'backtrack': 1,
                }, ...],
                'volume': [{
                    'value': 7270.56273,
                    'backtrack': 1,
                }, ...],
            }
        }
        '''
        log.debug('')
        timestamp, return_dict = str(time.time()), {
            'ticker-symbol': self.ticker_symbol,
            'interval': kwargs.get('interval', self.period_interval),
            'history': {}
        }
        update_targets = args or ('price', 'volume', 'trade-fee')
        if 'all' in update_targets or 'coin' in update_targets:
            self.update_coin_details(timestamp=timestamp, **kwargs)
        if 'all' in update_targets or 'price' in update_targets or 'volume' in update_targets:
            return_dict.update(
                self.update_price_volume_details(*args, timestamp=timestamp, **kwargs)
            )
            return_dict['history'].update(
                self.update_price_volume_history(*args, timestamp=timestamp, **kwargs)
            )
        if 'all' in update_targets or 'trade-fee' in update_targets:
            self.update_trade_fee_details(timestamp=timestamp, **kwargs)
        if 'all' in update_targets or 'indicators' in update_targets:
            return_dict.update(
                self.update_indicator_details(*args, timestamp=timestamp, **kwargs)
            )
            return_dict['history'].update(
                self.update_indicator_history(*args, timestamp=timestamp, **kwargs)
            )
        return return_dict

# CODE DUMP

#       timestamp = str(time.time())
#       self.update_cache(
#           self.get_account(recvWindow=60000), self.account_cache,
#           label=timestamp
#       )



#       return {}
#       self.update_cache(
#           return_dict, self.history_cache[timestamp], label=timestamp,
#       )

#           self.buy_price = float(
#               self.ticker_info_cache[timestamp].get('bidPrice')
#           )
#           self.sell_price = float(
#               self.ticker_info_cache[timestamp].get('askPrice')
#           )
#           return_dict.update(
#               {'buy-price': self.buy_price, 'sell-price': self.sell_price}
#           )

#           self.volume = float(
#               self.ticker_info_cache[timestamp].get('volume')
#           )
#           return_dict.update({'volume': self.volume})





