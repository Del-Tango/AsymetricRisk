#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADING BOT

import os
import time
import logging

from .ar_reporter import TradingReporter
from .ar_market import TradingMarket
from .ar_strategy import TradingStrategy

log = logging.getLogger('AsymetricRisk')


class TradingBot():

    def __init__(self, *args, **kwargs):
        log.debug('')
        self.trading_stragies = kwargs.get('trading-strategies', 'vwap') # vwap,rsi,macd,adx
        self.market = self.setup_market(**kwargs) # {'BTC/USDT': TradingMarket()}
        self.markets = {
            args[arg_index].ticker_symbol: args[arg_index] for arg_index in args
        }                                         # {'BTC/USDT': TradingMarket(), ...}
        self.markets.update(self.market)
        self.reporter = self.setup_reporter(**kwargs)
        self.analyzer = self.setup_analyzer(**kwargs)

    # FETCHERS

    def fetch_supported_trading_strategies(self):
        log.debug('')
        return ['vwap', 'rsi', 'macd', 'ma', 'ema', 'adx', 'volume', 'price']

    def fetch_active_market(self):
        log.debug('')
        if not self.market or not isinstance(self.market, dict):
            return False
        return list(self.market.values())[0]

    # SETTERS

    def set_market(self, ticker_symbol, market_obj):
        log.debug('')
        if not ticker_symbol or not market_obj:
            return False
        self.market = {ticker_symbol: market_obj}
        return self.market

    def set_trading_strategy(self, strategy):
        log.debug('')
        supported = self.fetch_supported_trading_strategies()
        for item in strategy.split(','):
            if item not in supported:
                return False
        self.trading_strategy = strategy
        return self.trading_strategy

    # ACTIONS

    def trade_watchdog(self, *args, **kwargs):
        log.debug('')
        failures, anchor_file = 0, kwargs.get('anchor-file', '')
        while True:
            if anchor_file and not os.path.exists(anchor_file):
                break
            trade = self.trade(*args, **kwargs)
            if not trade:
                failures += 1
            time.sleep(kwargs.get('watchdog-interval', 60))
        return failures

    def trade(self, *args, **kwargs):
        '''
        [ INPUT ]: *(vwap, rsi, macd, ma, ema, adx, price, volume)
            **{
                'analyze-risk': True,                     (type bool) - default True
                'strategy': vwap,rsi,macd,price,volume,   (type str) - default vwap
                'side': buy,                              (type str) - <buy, sell, auto> default auto
                'price-movement': 5%,
                'rsi-top': 70%,
                'rsi-bottom': 30%,
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
        [ RETURN ]: {
            'trade-id': 142324,
        }
        '''
        log.debug('')
        market = self.fetch_active_market()
        details = market.update_details('all', **kwargs)
        trade_flag, risk_index, trade_amount, trade = False, 0, kwargs.get('amount', 0), None
        if kwargs.get('analyze-risk'):
            trading_strategy = (arg[0] if len(args) == 1 else ','.join(args)) \
                if args else kwargs.get('strategy', 'vwap')
            kwargs.update({
                'details': details,
                'strategy': trading_strategy,
                'side': kwargs.get('side', 'auto'),
            })
            trade_flag, risk_index, trade_side = self.analyzer.analyze_risk(
                **kwargs
            )
        if risk_index == 0:
            # [ NOTE ]: Trading cycle should stop here according to specified
            #           risk tolerance. Do nothing, try again later.
            return False
        if trade_flag:
            if trade_side == 'buy':
                trade = market.buy(trade_amount, **kwargs)
            elif trade_side == 'sell':
                trade = market.sell(trade_amount, **kwargs)
        else:
            return False
        return False if (not trade or trade.get('error')) else trade

    def close_trade(self, *args, **kwargs):
        '''
        [ INPUT ]: *args    - trade ID's (type str)
                   **kwargs - symbol (type str) - ticker symbol, default is active market
                            - recvWindow (type int) - binance API response window, default is 60000
        [ RETURN ]: closed trades (type lst), failed closes (type lst)
        '''
        log.debug('')
        market = self.fetch_active_market()
        return market.close_position(*args, **kwargs)

    # VIEWERS

    def view_asset_balance(self, *args, **kwargs):
        '''
        [ NOTE ]: View balance of specified or all coins in market account.
        '''
        log.debug('')
        market = self.fetch_active_market()
        return market.fetch_asset_balance(*args, **kwargs)

    def view_trades(self, *args, **kwargs):
        '''
        [ NOTE ]: View active trades.
        '''
        log.debug('')
        market = self.fetch_active_market()
        return market.fetch_active_trades(*args, **kwargs)

    def view_trade_history(self, *args, **kwargs):
        '''
        [ NOTE ]: View all trades.
        '''
        log.debug('')
        market = self.fetch_active_market()
        return market.fetch_all_trades(*args, **kwargs)

    # REPORT MANAGEMENT

    # TODO
    def generate_report(self):
        log.debug('TODO - Under construction, building...')

    # MARKET MANAGEMENT

    def select_market(self, ticker_symbol, **kwargs):
        '''
        [ NOTE ]: Select one of the previously entered trading markets as the
                  target for bot actions.
        '''
        log.debug('')
        if ticker_symbol not in self.markets.keys():
            return False
        return self.set_market(ticker_symbol, self.markets[ticker_symbol])

    def enter_market(self, **kwargs):
        '''
        [ NOTE ]: Add new TradingMarket object to markets
        '''
        log.debug('')
        market = TradingMarket(
            kwargs.get('api-key'), kwargs.get('api-secret'), **kwargs
        )
        if not market:
            return False
        ticker_symbol = kwargs.get('ticker-symbol') \
            or (kwargs.get('base-currency', str()) + '/' \
            + kwargs.get('quote-currency', str()))
        new_entry = {ticker_symbol: market}
        self.markets.update(new_entry)
        return {
            'error': False if market else True,
            'market': market,
        }

    def exit_market(self, *args, **kwargs):
        '''
        [ NOTE ]: Remove TradingMarket object from markets
        '''
        log.debug('')
        failures, failed_tickers = 0, []
        if not args:
            failures += 1
        for ticker_symbol in args:
            if ticker_symbol not in self.market.keys():
                failures += 1
                failed_tickers.append(ticker_symbol)
                continue
            del self.market[ticker_symbol]
        return {
            'error': False if not failures else True,
            'failures': failures,
            'failed-tickers': failed_tickers,
        }

    # SETUP

    def setup_analyzer(self, **kwargs):
        log.debug('')
        analyzer = TradingStrategy(**kwargs)
        return analyzer

    def setup_reporter(self, **kwargs):
        log.debug('')
        reporter = TradingReporter(**kwargs)
        return reporter

    def setup_market(self, **kwargs):
        log.debug('')
        market = TradingMarket(
            kwargs.get('api-key', str()),
            kwargs.get('api-secret', str()),
            **kwargs
        )
        return {kwargs['ticker-symbol']: market}

