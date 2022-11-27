#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADING BOT

import os
import time
import logging
import pysnooper

from .ar_reporter import TradingReporter
from .ar_market import TradingMarket
from .ar_strategy import TradingStrategy

from src.backpack.bp_ensurance import ensure_files_exist
from src.backpack.bp_computers import compute_percentage
from src.backpack.bp_general import stdout_msg

log = logging.getLogger('AsymetricRisk')


class TradingBot():

#   @pysnooper.snoop()
    def __init__(self, *args, **kwargs):
        log.debug('')
        self.trading_stragies = kwargs.get('trading-strategies', 'vwap') # vwap,rsi,macd,adx
        self.market = {}
        self.start_account_value = float()
        self.current_account_value = float()
        self.profit_baby = float(10)
        self.trade_amount = float(1)
        self.profit_target = float()
        if kwargs.get('api-key') and kwargs.get('api-secret'):
            try:
                self.market = self.setup_market(**kwargs) # {'BTC/USDT': TradingMarket()}
                self.compute_profit_baby(
                    kwargs.get('profit-baby', self.profit_baby), **kwargs
                )
                self.compute_trade_amount(
                    kwargs.get('trade-amount', self.trade_amount), **kwargs
                )
            except Exception as w:
                stdout_msg(
                    'Could not setup trading bot market! '
                    'Details: ({})'.format(w), warn=True
                )
        self.markets = {arg.ticker_symbol: arg for arg in args} # {'BTC/USDT': TradingMarket(), ...}
        self.markets.update(self.market)
        self.reporter = self.setup_reporter(**kwargs)
        self.analyzer = self.setup_analyzer(**kwargs)

    # FETCHERS

#   @pysnooper.snoop()
    def fetch_account_value(self, **kwargs):
        log.debug('')
        market = self.fetch_active_market()
        if not market:
            log.error(
                'Could not fetch active market! Details: ({})'.format(market)
            )
            return False
        base, quote = self.fetch_market_currency()
        response = market.get_asset_balance(
            base, recvWindow=kwargs.get('recvWindow', 60000)
        )
        if kwargs.get('free') or kwargs.get('locked'):
            total_value = float(response['free']) if kwargs.get('free') \
                else float(response['locked'])
        else:
            total_value = (float(response['free']) + float(response['locked']))
        return total_value

    def fetch_market_currency(self):
        log.debug('')
        market = self.fetch_active_market()
        if not market:
            log.error(
                'Could not fetch active market! Details: ({})'.format(market)
            )
            return False, False
        return market.base_currency, market.quote_currency

    def fetch_supported_trading_strategies(self):
        log.debug('')
        return ['vwap', 'rsi', 'macd', 'ma', 'ema', 'adx', 'volume', 'price']

    def fetch_active_market(self):
        log.debug('')
        if not self.market or not isinstance(self.market, dict):
            log.error(
                'Active market not set up! Details: ({})'.format(self.market)
            )
            return False
        market = list(self.market.values())[0]
        if not market:
            log.error(
                'Could not fetch active market! Details: ({})'.format(market)
            )
            return False
        return market

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

    # UPDATERS

    def update_current_account_value(self, **kwargs):
        log.debug('')
        value = self.fetch_account_value(**kwargs)
        if not value:
            return False
        self.current_account_value = value
        return self.current_account_value

    # ENSURANCE

#   @pysnooper.snoop()
    def ensure_trading_market_setup(self, **kwargs):
        log.debug('')
        if not self.market:
            self.market = self.setup_market(**kwargs)
        return self.market

    # ACTIONS

#   @pysnooper.snoop()
    def trade_watchdog(self, *args, **kwargs):
        log.debug('')
        failures, anchor_file = 0, kwargs.get(
            'watchdog-anchor-file', '.ar-bot.anch'
        )
        ensure_files_exist(anchor_file)
        while True:
            if anchor_file and not os.path.exists(anchor_file):
                break
            trade = self.trade(*args, **kwargs)
            if not trade:
                if isinstance(trade, dict) and trade.get('error'):
                    failures += 1
            self.update_current_account_value(**kwargs)
            if self.profit_target \
                    and self.current_account_value >= self.profit_target:
                self.mission_accomplished()
                break
            cool_down_seconds = kwargs.get('watchdog-interval', 60)
            stdout_msg(
                'Bot cool down: {} seconds'.format(cool_down_seconds), red=True
            )
            time.sleep(cool_down_seconds)
        return failures

#   @pysnooper.snoop()
    def trade(self, *args, **kwargs):
        '''
        [ INPUT ]: *(vwap, rsi, macd, ma, ema, adx, price, volume)
            **{
                'analyze-risk': True,                     (type bool) - default True
                'strategy': vwap,rsi,macd,price,volume,   (type str) - default vwap
                'side': buy,                              (type str) - <buy, sell, auto> default auto
                'period': 14,
                'backtrack': 5,
                'backtracks': 14,
                'chart': candles,
                'price-movement': 5%,
                'interval': 5m,
                'rsi-top': 70%,
                'rsi-bottom': 30%,
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
                'price-period': 14,
                'price-backtrack': 5,
                'price-backtracks': 12,
                'price-chart': candles,
                'price-interval': 5m,
            }
        [ RETURN ]: {
            'trade-id': 142324,
        }
        '''
        log.debug('')
        market, details = self.fetch_active_market(), kwargs.copy()
        log.debug('Trade kwargs - {}'.format(details))
        if not market:
            stdout_msg('Trading market not set up!', err=True)
            return False
        stdout_msg(
            'Looking for trades... ({})'.format(market.ticker_symbol), info=True
        )
        trading_strategy = ','.join(args) if args \
                else details.get('strategy', '')
        stdout_msg(
            'Updating market details applicable to strategy... ({})'
            .format(trading_strategy), info=True
        )
        market_update_args = trading_strategy.split(',')
        if 'indicators' not in market_update_args:
            market_update_args.append('indicators')
        market_details = market.update_details(*market_update_args, **details)
        trade_flag, risk_index, trade = False, 0, None
        trade_amount = self.compute_trade_amount(
            details.get('trade-amount', 1), **details
        )
        if details.get('analyze-risk'):
            details.update({
                'details': market_details,
                'strategy': trading_strategy,
                'amount': trade_amount,
                'side': kwargs.get('side', 'auto'),
            })
            stdout_msg('Analyzing trading risk', info=True)
            trade_flag, risk_index, trade_side, failures = self.analyzer.analyze_risk(
                **details
            )
        if risk_index == 0:
            # [ NOTE ]: Trading cycle should stop here according to specified
            #           risk tolerance. Do nothing, try again later.
            stdout_msg('[ N/A ]: Skipping trade, not a good ideea right now.')
            return False
        if trade_flag:
            if trade_side == 'buy':
                trade = market.buy(trade_amount, **details)
            elif trade_side == 'sell':
                trade = market.sell(trade_amount, **details)
        else:
            return False
        return False if (not trade or trade.get('error')) else trade

    def close_trade(self, *args, **kwargs):
        '''
        [ NOTE ]: When in a long-trade (buy) exit at the next price resistance
                  level.

        [ NOTE ]: When in a short-trade (sell) exit at the next price support
                  level.

        [ INPUT ]: *args    - trade ID's (type str)
                   **kwargs - symbol (type str) - ticker symbol, default is
                              active market
                            - recvWindow (type int) - binance API response
                              window, default is 60000

        [ RETURN ]: closed trades (type lst), failed closes (type lst)
        '''
        log.debug('')
        market = self.fetch_active_market()
        return market.close_position(*args, **kwargs)

    # COMPUTERS

    def compute_trade_amount(self, percentage, **kwargs):
        log.debug('')
        self.trade_amount = 1 if not self.current_account_value \
            else compute_percentage(
                percentage, self.current_account_value
            )
        return self.trade_amount

    def compute_profit_baby(self, percentage, **kwargs):
        log.debug('')
        account_value = self.fetch_account_value(**kwargs)
        self.start_account_value = account_value
        self.current_account_value = account_value
        self.profit_baby = 0 if not self.start_account_value \
            else compute_percentage(
                percentage, self.start_account_value
            )
        self.profit_target = (self.start_account_value + self.profit_baby)
        return self.profit_baby

    # GENERAL

    def mission_accomplished(self):
        log.debug('HELL YES!')
        message = 'Target acquired! PROFIT BABY!! - Started from ({}) '\
            'now we here ({}) :>'.format(
                self.start_account_value, self.current_account_value
            )
        log.info(message)
        stdout_msg('[ DONE ]: ' + message)
        return message

    # VIEWERS

    def view_report(self, *args, **kwargs):
        log.debug('')
        if not self.reporter:
            log.error('No trading reporter set up!')
            return False
        return self.reporter.read(*args, **kwargs)

    def view_market_details(self, *args, **kwargs):
        log.debug('')
        market = self.fetch_active_market()
        if not market:
            return False
        if not args:
            args = ('all', )
        return market.fetch_details(*args, **kwargs)

    def view_account_details(self, *args, **kwargs):
        log.debug('')
        market = self.fetch_active_market()
        if not market:
            return False
        return market.fetch_account(**kwargs)

    def view_asset_balance(self, *args, **kwargs):
        '''
        [ NOTE ]: View balance of specified or all coins in market account.
        '''
        log.debug('')
        market = self.fetch_active_market()
        if not market:
            return False
        return market.fetch_asset_balance(*args, **kwargs)

    def view_trades(self, *args, **kwargs):
        '''
        [ NOTE ]: View active trades.
        '''
        log.debug('')
        market = self.fetch_active_market()
        if not market:
            return False
        return market.fetch_active_trades(*args, **kwargs)

    def view_trade_history(self, *args, **kwargs):
        '''
        [ NOTE ]: View all trades.
        '''
        log.debug('')
        market = self.fetch_active_market()
        if not market:
            return False
        return market.fetch_all_trades(*args, **kwargs)

    def view_supported_tickers(self, *args, **kwargs):
        '''
        [ NOTE ]: View all supported ticker symbols
        [ RETURN ]: {symbol: {'symbol': str, 'price': str}}
        '''
        log.debug('')
        market = self.fetch_active_market()
        if not market:
            return False
        return market.fetch_supported_tickers()

    def view_supported_coins(self, *args, **kwargs):
        '''
        [ NOTE ]: View all supported crypto coins
        '''
        log.debug('')
        market = self.fetch_active_market()
        if not market:
            return False
        return market.fetch_supported_coins(**kwargs)

    # REPORT MANAGEMENT

    def generate_report(self, *args, **kwargs):
        log.debug('')
        if not self.reporter:
            log.error('No trading reporter set up!')
            return False
        return self.reporter.generate(*args, **kwargs)

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

#   @pysnooper.snoop()
    def setup_market(self, **kwargs):
        log.debug('')
        market = TradingMarket(
            kwargs.get('api-key', str()),
            kwargs.get('api-secret', str()),
            testnet=kwargs.get('test'),
            **kwargs
        )
        return {kwargs['ticker-symbol']: market}


# CODE DUMP

#       strategy = ['all'] if not kwargs.get('strategy') else kwargs['strategy'].split(',')
#           trading_strategy = (arg[-1] if len(args) == 1 else ','.join(args)) \
#               if args else kwargs.get('strategy', 'vwap')

#               account_value = self.fetch_account_value(**kwargs)
#               self.start_account_value = account_value
#               self.current_account_value = account_value
#               self.profit_baby = 0 if not self.start_account_value \
#                   else compute_percentage(
#                       kwargs.get('profit-baby', 10), self.start_account_value
#                   )
#               self.profit_target = (self.start_account_value + self.profit_baby)

