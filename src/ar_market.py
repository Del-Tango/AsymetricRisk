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
        # necessary data (depending on chosen taapi api plan specifications)
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

    # TODO
    def fetch_details(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')

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

    # UPDATERS

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


        # Get coin price
#       price = client.get_symbol_ticker(symbol=sanitized_ticker)
#       # Calculate how much coin specified amount can buy
#       buy_quantity = round(amount / float(price['price']))

#           quantity=buy_quantity,


#       self.order_market_buy(
#           symbol=self.ticker_symbol, quantity=amount, newOrderRespType='JSON',
#           recvWindow=60000
#       )


#       self.period_start = kwargs.get('period-start', '1/09/2022')
#       self.period_end = kwargs.get('period-end', '1/10/2022')

#           'caches': {
#               'coin-info': self.coin_info_cache,
#               'ticker-info': self.ticker_info_cache,
#               'trade-fee': self.trade_fee_cache
#           }

#       ticker_symbol = str(self.base_currency) \
#           + str(self.quote_currency)

#       for coin_dict in self.coin_info_cache[timestamp]:
#           if coin_dict['coin'] != self.base_currency:
#               continue
#           print('DEBUG: coin_dict', coin_dict)
#           self.buy_price = coin_dict.get('bidPrice')
#           self.sell_price = coin_dict.get('askPrice')
#           self.volume = coin_dict.get('volume')
#           break


# Coin Info Dict - {'coin': 'BTC', 'depositAllEnable': True,
# 'withdrawAllEnable': True, 'name': 'Bitcoin', 'free': '0', 'locked': '0',
# 'freeze': '0', 'withdrawing': '0', 'ipoing': '0', 'ipoable': '0', 'storage':
# '0', 'isLegalMoney': False, '
#   trading': True, 'networkList': [{'network': 'BSC', 'coin': 'BTC', 'withdrawIntegerMultiple': '0.00000001', 'isDefault': False, 'depositEnable': True, 'withdrawEnable': True, 'depositDesc': '', 'withdrawDesc': '', 'specialTips': '', 'specia
#   lWithdrawTips': 'The network you have selected is BSC. Please ensure that the withdrawal address supports the Binance Smart Chain network. You will lose your assets if the chosen platform does not support retrievals.', 'name': 'BNB Smart C
#   hain (BEP20)', 'resetAddressStatus': False, 'addressRegex': '^(0x)[0-9A-Fa-f]{40}$', 'addressRule': '', 'memoRegex': '', 'withdrawFee': '0.0000049', 'withdrawMin': '0.0000098', 'withdrawMax': '10000000000', 'minConfirm': 15, 'unLockConfirm
#   ': 0, 'sameAddress': False, 'estimatedArrivalTime': 5, 'busy': False, 'country': 'AE,BINANCE_BAHRAIN_BSC,custody'}, {'network': 'BTC', 'coin': 'BTC', 'withdrawIntegerMultiple': '0.00000001', 'isDefault': True, 'depositEnable': True, 'withd
#   rawEnable': True, 'depositDesc': '', 'withdrawDesc': '', 'specialTips': '', 'specialWithdrawTips': '', 'name': 'Bitcoin', 'resetAddressStatus': False, 'addressRegex': '^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^[(bc1q)|(bc1p)][0-9A-Za-z]{37,62}$',
#   'addressRule': '', 'memoRegex': '', 'withdrawFee': '0.0002', 'withdrawMin': '0.001', 'withdrawMax': '7500', 'minConfirm': 1, 'unLockConfirm': 2, 'sameAddress': False, 'estimatedArrivalTime': 60, 'busy': False, 'country': 'AE,BINANCE_BAHRA
#   IN_BSC,custody'}, {'network': 'BNB', 'coin': 'BTC', 'withdrawIntegerMultiple': '0.00000001', 'isDefault': False, 'depositEnable': True, 'withdrawEnable': True, 'depositDesc': '', 'withdrawDesc': '', 'specialTips': 'Please enter both MEMO a
#   nd Address data, which are required to deposit BEP2-BTCB tokens to your Binance account.', 'name': 'BNB Beacon Chain (BEP2)', 'resetAddressStatus': False, 'addressRegex': '^(bnb1)[0-9a-z]{38}$', 'addressRule': '', 'memoRegex': '^[0-9A-Za-z
#                                                                                                                                                                                                                                       \\-_]{1,120}$', 'withdrawFee': '0.0000082', 'withdrawMin': '0.000016', 'withdrawMax': '10000000000', 'depositDust': '0.00001', 'minConfirm': 1, 'unLockConfirm': 0, 'sameAddress': True, 'estimatedArrivalTime': 5, 'busy': False, 'country': '
#   AE,BINANCE_BAHRAIN_BSC'}, {'network': 'SEGWITBTC', 'coin': 'BTC', 'withdrawIntegerMultiple': '0.00000001', 'isDefault': False, 'depositEnable': True, 'withdrawEnable': False, 'depositDesc': '', 'withdrawDesc': 'The wallet is currently unde
#   rgoing maintenance. Withdrawals for this asset will be resumed shortly.', 'specialTips': '', 'specialWithdrawTips': '', 'name': 'BTC(SegWit)', 'resetAddressStatus': False, 'addressRegex': '', 'addressRule': '', 'memoRegex': '', 'withdrawFe
#   e': '0.0005', 'withdrawMin': '0.001', 'withdrawMax': '10000000000', 'minConfirm': 1, 'unLockConfirm': 2, 'sameAddress': False, 'estimatedArrivalTime': 5, 'busy': False}, {'network': 'ETH', 'coin': 'BTC', 'withdrawIntegerMultiple': '0.00000
#   001', 'isDefault': False, 'depositEnable': True, 'withdrawEnable': True, 'depositDesc': '', 'withdrawDesc': '', 'specialTips': 'This deposit address supports ERC20 BBTC tokens. Please ensure your destination address supports BBTC tokens un
#   der the contract address ending in 22541.', 'specialWithdrawTips': 'You are withdrawing Binance Wrapped BTC (BBTC). Please ensure that the receiving platform supports this token or you might potentially risk losing your asset.', 'name': 'E
#   thereum (ERC20)', 'resetAddressStatus': False, 'addressRegex': '^(0x)[0-9A-Fa-f]{40}$', 'addressRule': '', 'memoRegex': '', 'withdrawFee': '0.00018', 'withdrawMin': '0.00036', 'withdrawMax': '10000000000', 'minConfirm': 12, 'unLockConfirm'
#   : 0, 'sameAddress': False, 'estimatedArrivalTime': 5, 'busy': False, 'country': 'AE,BINANCE_BAHRAIN_BSC,custody'}]}


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





