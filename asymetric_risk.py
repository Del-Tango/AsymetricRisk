#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK - (A)Risk

import os
import logging
import pysnooper
import optparse
import json
import time

#from time import sleep
from subprocess import Popen, PIPE

from src.backpack.bp_log import log_init
from src.backpack.bp_ensurance import ensure_files_exist, ensure_directories_exist
from src.backpack.bp_shell import shell_cmd
from src.backpack.bp_checkers import check_file_exists, check_pid_running
from src.backpack.bp_general import stdout_msg, clear_screen, pretty_dict_print
from src.backpack.bp_convertors import dict2json
from src.backpack.bp_filters import filter_file_name_from_path, filter_directory_from_path
from src.ar_bot import TradingBot

AR_SCRIPT_NAME = "AsymetricRisk"
AR_SCRIPT_DESCRIPTION = "Crypto Trading Bot"
AR_VERSION = "AR15"
AR_VERSION_NO = "1.0"

# COLD ARGS

AR_PROJECT_DIR = os.path.dirname(__file__)

# HOT ARGS

AR_DEFAULT = {
    "log-dir":              AR_PROJECT_DIR + "/log",
    "conf-dir":             AR_PROJECT_DIR + "/conf",
    "lib-dir":              AR_PROJECT_DIR + "/lib",
    "src-dir":              AR_PROJECT_DIR + "/src",
    "dox-dir":              AR_PROJECT_DIR + "/dox",
    "dta-dir":              AR_PROJECT_DIR + "/data",
    "tmp-dir":              "/tmp",
    "log-file":             "asymetric_risk.log",
    "conf-file":            "asymetric_risk.conf.json",
    "init-file":            __file__,
    "watchdog-pid-file":    "ar-bot.pid",
    "watchdog-anchor-file": "ar-bot.anchor",
    "log-format":           "[ %(asctime)s ] %(name)s [ %(levelname)s ] %(thread)s - %(filename)s - %(lineno)d: %(funcName)s - %(message)s",
    "timestamp-format":     "%d/%m/%Y-%H:%M:%S",
    "api-key":              os.environ.get('binance_api'),
    "api-secret":           os.environ.get('binance_secret'),
    "taapi-key":            os.environ.get('taapi_api'),
    "api-url":              'https://testnet.binance.vision/api',
    "taapi-url":            "https://api.taapi.io",
    "trade-amount":         1,
    "profit-baby":          10,
    "base-currency":        'BTC',
    "quote-currency":       'USDT',
    "period-start":         '01-10-2022',
    "period-end":           '01-11-2022',
    "risk-tolerance":       1,
    "test":                 False,
    "debug":                True,
    "silence":              False,
    "action":               '', #(start-watchdog | trade-report | withdrawal-report | deposit-report | stop-watchdog | single-trade | view-report)
    "report-id":            '0',
    "analyze-risk":         True,
    "strategy":             "vwap,rsi,macd,adx,ma,ema,price,volume",
    "side":                 "auto",
    "interval":             "5m",
    "period":               14,
    "stop-loss":            10,
    "take-profit":          30,
    "trailing-stop":        10,
    "price-movement":       5,
    "rsi-top":              70,
    "rsi-bottom":           30,
    "rsi-period":           14,
    "rsi-backtrack":        5,
    "rsi-backtracks":       12,
    "rsi-chart":            "candles",
    "rsi-interval":         "5m",
    "volume-movement":      5,
    "volume-interval":      "5m",
    "ma-period":            30,
    "ma-backtrack":         5,
    "ma-backtracks":        12,
    "ma-chart":             "candles",
    "ma-interval":          "5m",
    "ema-period":           30,
    "ema-backtrack":        5,
    "ema-backtracks":       12,
    "ema-chart":            "candles",
    "ema-interval":         "5m",
    "macd-backtrack":       5,
    "macd-backtracks":      12,
    "macd-chart":           "candles",
    "macd-fast-period":     12,
    "macd-slow-period":     26,
    "macd-signal-period":   9,
    "macd-interval":        "5m",
    "adx-period":           14,
    "adx-backtrack":        5,
    "adx-backtracks":       12,
    "adx-chart":            "candles",
    "adx-interval":         "5m",
    "vwap-period":          14,
    "vwap-backtrack":       5,
    "vwap-backtracks":      12,
    "vwap-chart":           "candles",
    "vwap-interval":        "5m"
}

log = log_init(
    '/'.join([AR_DEFAULT['log-dir'], AR_DEFAULT['log-file']]),
    AR_DEFAULT['log-format'], AR_DEFAULT['timestamp-format'],
    AR_DEFAULT['debug'], log_name=AR_SCRIPT_NAME
)
trading_bot = None #TradingBot(**AR_DEFAULT)

# FETCHERS

def fetch_watchdog_pid():
    log.debug('')
    if not os.path.exists(AR_DEFAULT['watchdog-pid-file']):
        return False
    return file2list(AR_DEFAULT['watchdog-pid-file'])[0]

def fetch_action_handlers():
    log.debug('')
    return {
        'start-watchdog': action_start_watchdog,
        'stop-watchdog': action_stop_watchdog,
        'trade-report': action_trade_report,
        'withdrawal-report': action_withdrawal_report,
        'deposit-report': action_deposit_report,
        'single-trade': action_single_trade,
        'view-trade-report': action_view_trade_report,
        'view-withdrawal-report': action_view_withdrawal_report,
        'view-deposit-report': action_view_deposit_report,
        'account-details': action_account_details,
        'market-details': action_market_details,
        'supported-coins': action_supported_coins,
        'supported-tickers': action_supported_tickers,
    }

# SETTERS

# CHECKERS

def check_preconditions(**kwargs):
    log.debug('')
    stdout_msg('Verifying action preconditions...', info=True)
    checkers = {
        'preconditions-conf': check_config_file(**kwargs),
        'preconditions-log': check_log_file(**kwargs),
        'trading-bot': check_trading_bot(**kwargs),
    }
    log.debug('checkers: {}'.format(checkers))
    if False in checkers.values():
        return len([item for item in checkers.values() if not item])
    return 0

def check_trading_bot(**kwargs):
    log.debug('')
    if str(kwargs.get('action')) == 'stop-watchdog':
        return
    stdout_msg('Checking trading bot setup properly...', info=True)
    if trading_bot and isinstance(trading_bot, TradingBot):
        stdout_msg('Trading bot!', ok=True)
        return trading_bot
    stdout_msg('No trading bot found!', nok=True)
    stdout_msg('Creating new trading bot...', info=True)
    return create_trading_bot(**AR_DEFAULT)

def check_config_file(**kwargs):
    log.debug('')
    stdout_msg('Check config file...', info=True)
    conf_file_path = AR_DEFAULT['conf-dir'] + "/" + AR_DEFAULT['conf-file']
    conf_dir = ensure_directories_exist(AR_DEFAULT['conf-dir'])
    exit_code = 0
    if not check_file_exists(conf_file_path):
        cmd_out, cmd_err, exit_code = shell_cmd(
            'touch ' + conf_file_path + ' &> /dev/null'
        )
    return_flag = False if exit_code != 0 else True
    if return_flag:
        stdout_msg('Config file!', ok=True)
    else:
        stdout_msg(
            'Could not make sure config file exists and is writable!', nok=True
        )
    return return_flag

def check_log_file(**kwargs):
    log.debug('')
    stdout_msg('Checking log file...', info=True)
    log_file_path = AR_DEFAULT['log-dir'] + "/" + AR_DEFAULT['log-file']
    log_dir = ensure_directories_exist(AR_DEFAULT['log-dir'])
    exit_code = 0
    if not check_file_exists(log_file_path):
        cmd_out, cmd_err, exit_code = shell_cmd(
            'touch ' + log_file_path + ' &> /dev/null'
        )
    return_flag = False if exit_code != 0 else True
    if return_flag:
        stdout_msg('Log file!', ok=True)
    else:
        stdout_msg(
            'Could not make sure log file exists and is writable!', nok=True
        )
    return return_flag

# ACTIONS

# TODO
def action_trade_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
    stdout_msg('[ ACTION ]: Trade Report', bold=True)
def action_withdrawal_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
    stdout_msg('[ ACTION ]: Withdrawal Report', bold=True)
def action_deposit_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
    stdout_msg('[ ACTION ]: Deposit Report', bold=True)
def action_view_trade_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
    stdout_msg('[ ACTION ]: View Trade Report', bold=True)
def action_view_withdrawal_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
    stdout_msg('[ ACTION ]: View Withdrawal Report', bold=True)
def action_view_deposit_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
    stdout_msg('[ ACTION ]: View Deposit Report', bold=True)
def action_account_details(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
    stdout_msg('[ ACTION ]: View Account Details', bold=True)
def action_market_details(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
    stdout_msg('[ ACTION ]: View Market Details', bold=True)
def action_supported_coins(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
    stdout_msg('[ ACTION ]: View Supported Coins', bold=True)

def action_supported_tickers(*args, **kwargs):
    log.debug('')
    stdout_msg('[ ACTION ]: View Supported Ticker Symbols...', bold=True)
    stdout_msg('Fetching supported ticker symbols...', info=True)
    tickers = trading_bot.view_supported_tickers(*args, **kwargs)
    if not tickers:
        stdout_msg(
            'Could not fetch supported ticker symbols! Details: ({})'.format(
                tickers
            ), nok=True
        )
        return 1
    print(dict2json(tickers))
    stdout_msg('Available ticker symbols ({})'.format(len(tickers)), ok=True)
    return 0

def action_single_trade(*args, **kwargs):
    log.debug('')
    stdout_msg('[ ACTION ]: Single Trade', bold=True)
    stdout_msg('Starting {} trading bot in single trade mode...'
        .format(AR_SCRIPT_NAME), info=True
    )
    ensure_market = trading_bot.ensure_trading_market_setup(**kwargs)
    try:
        watchdog = trading_bot.trade(
            *(kwargs.get('strategy', AR_DEFAULT['strategy']).split(',')),
            **kwargs
        )
        if watchdog == 0:
            stdout_msg('Trading bot!', ok=True)
        return watchdog
    except KeyboardInterrupt as e:
        log.debug(e)
    except Exception as e:
        log.error(e)
    return 1

def action_stop_watchdog(*args, **kwargs):
    log.debug('')
    stdout_msg('[ ACTION ]: Stop Trading Bot', bold=True)
    if not os.path.exists(AR_DEFAULT['watchdog-anchor-file']):
        stdout_msg(
            '{} trading bot not running! No process anchor file found.'
            .format(AR_SCRIPT_NAME), err=True
        )
        return False
    remove = os.remove(AR_DEFAULT['watchdog-anchor-file'])
    pid = fetch_watchdog_pid()
    stdout_msg('Process anchor file removed.', ok=True)
    time.sleep(1)
    if check_pid_running(pid):
        stdout(
            'Could not stop trading bot! Process ({}) still running.'
            .format(pid), nok=True
        )
        return False
    stdout_msg('Trading bot process ({}) terminated!'.format(pid), ok=True)
    return True

#@pysnooper.snoop()
def action_start_watchdog(*args, **kwargs):
    '''
    [ RETURN ]: Trading watchdog exit code - type int
    '''
    log.debug('')
    stdout_msg('[ ACTION ]: Start Trading Bot', bold=True)
    stdout_msg('Starting {} trading bot in watchdog mode...'
        .format(AR_SCRIPT_NAME), info=True
    )
    ensure_market = trading_bot.ensure_trading_market_setup(**kwargs)
    try:
        watchdog = trading_bot.trade_watchdog(
            *(kwargs.get('strategy', AR_DEFAULT['strategy']).split(',')),
            **kwargs
        )
        if watchdog == 0:
            stdout_msg('Trading bot!', ok=True)
        return watchdog
    except KeyboardInterrupt as e:
        log.debug(e)
    except Exception as e:
        log.error(e)
    return 1

# HANDLERS

#@pysnooper.snoop()
def handle_actions(actions=[], *args, **kwargs):
    log.debug('')
    failure_count = 0
    handlers = fetch_action_handlers()
    for action_label in actions:
        stdout_msg('Processing action... ({})'.format(action_label), info=True)
        if action_label not in handlers.keys():
            stdout_msg(
                'Invalid action label specified! ({})'
                .format(action_label), nok=True
            )
            continue
        try:
            handle = handlers[action_label](*args, **kwargs)
            if not handle or (isinstance(handle, int) and handle != 0):
                stdout_msg(
                    'Action ({}) failures detected! ({})'
                    .format(action_label, handle), nok=True
                )
                failure_count += 1
                continue
        except Exception as e:
            log.error(e)
            stdout_msg('Action ({}) terminated abnormaly! Details: {}'.format(
                action_label, e
            ), err=True)
            return failure_count + 1
        stdout_msg(
            "Action executed successfully! ({})".format(action_label), ok=True
        )
    return True if failure_count == 0 else failure_count

# CREATORS

#@pysnooper.snoop()
def create_trading_bot(**kwargs):
    global trading_bot
    log.debug('')
    log.debug('Creating trading bot with kwargs: {}'.format(kwargs))
    try:
        trading_bot = TradingBot(**kwargs)
    except Exception as w:
        log.warning(w)
        stdout_msg(
            'Could not set up trading bot! Details: ({})'.format(w), warn=True
        )
        return False
    return trading_bot

def create_command_line_parser():
    log.debug('')
    help_msg = format_header_string() + '''
    [ EXAMPLE ]: View reports -

        ~$ %prog \\
            -a  | --action "view-trade-report" \\
            -r  | --report-id '0,1,2,3,4,5'

    [ EXAMPLE ]: Stop (A)Risk trading bot -

        ~$ %prog \\
            -a  | --action "stop-watchdog"

    [ EXAMPLE ]: Start (A)Risk trading bot -

        ~$ %prog \\
            -a  | --action "start-watchdog,trade-report" \\
            -c  | --config-file /etc/conf/asymetric_risk.conf.json \\
            -l  | --log-file /etc/log/asymetric_risk.log \\
            -K  | --api-key "yxdLHNgKWzka2HjzR5jZF0ZXTCZaHp2V1X9EgXjKBxLsfKoClFvET1PqIUW9ctAw" \\
            -S  | --api-secret "oPyuIoqWHBt5pvfCk1YLIslViuH87DJvRTgtOsLylGB58LRsEuHvu4KuZOv0DAv5" \\
            -k  | --taapi-key "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM2MmRkNThmYzVhOGFkZmVjM2ZhMmEzIiwiaWF0IjoxNjY3NzAxNzg5LCJleHAiOjMzMTcyMTY1Nzg5fQ.33yXXi5RK1oupATjS-RFMLKfD7grZdJ2r7GT4gH-tAE" \\
            -U  | --api-url "https://testnet.binance.vision/api" \\
            -u  | --taapi-url "https://api.taapi.io" \\
            -T  | --strategy "vwap,rsi,macd,adx,ma,ema,price,volume" \\
            -D  | --debug \\
            -s  | --silence \\
            -A  | --analyze-risk \\
            -t  | --side "auto" \\
            -i  | --interval "5m" \\
            -p  | --period 14 \\
            -R  | --risk-tolerance High \\
            -b  | --base-currency BTC \\
            -q  | --quote-currency USDT \\
            -Z  | --ticker-symbol BTC/USDT \\
            -P  | --profit-baby 10 \\
                | --stop-loss 10 \\
                | --take-profit 30 \\
                | --trailing-stop 10 \\
                | --price-movement 5 \\
                | --rsi-top 70 \\
                | --rsi-bottom 30 \\
                | --rsi-period 14 \\
                | --rsi-backtrack 5 \\
                | --rsi-backtracks 12 \\
                | --rsi-chart "candles" \\
                | --rsi-interval "5m" \\
                | --volume-movement 5 \\
                | --volume-interval "5m" \\
                | --ma-period 30 \\
                | --ma-backtrack 5 \\
                | --ma-backtracks 12 \\
                | --ma-chart "candles" \\
                | --ma-interval "5m" \\
                | --ema-period 30 \\
                | --ema-backtrack 5 \\
                | --ema-backtracks 12 \\
                | --ema-chart "candles" \\
                | --ema-interval "5m" \\
                | --macd-backtrack 5 \\
                | --macd-backtracks 12 \\
                | --macd-chart "candles" \\
                | --macd-fast-period 12 \\
                | --macd-slow-period 26 \\
                | --macd-signal-period 9 \\
                | --macd-interval "5m" \\
                | --adx-period 14 \\
                | --adx-backtrack 5 \\
                | --adx-backtracks 12 \\
                | --adx-chart "candles" \\
                | --adx-interval "5m" \\
                | --vwap-period 14 \\
                | --vwap-backtrack 5 \\
                | --vwap-backtracks 12 \\
                | --vwap-chart "candles" \\
                | --vwap-interval "5m"'''
    parser = optparse.OptionParser(help_msg)
    return parser

# PROCESSORS

def process_command_line_options(parser):
    '''
    [ NOTE ]: In order to avoid a bad time in STDOUT land, please process the
              silence flag before all others.
    '''
    log.debug('')
    (options, args) = parser.parse_args()
    processed = {
        'silence_flag': process_silence_argument(parser, options),
        'debug_flag': process_debug_mode_argument(parser, options),
        'config_file': process_config_file_argument(parser, options),
        'log_file': process_log_file_argument(parser, options),
        'action_csv': process_action_csv_argument(parser, options),
        'base_currency': process_base_currency_argument(parser, options),
        'quote_currency': process_quote_currency_argument(parser, options),
        'ticker_symbol': process_ticker_symbol_argument(parser, options),
        'risk_tolerance': process_risk_tolerance_argument(parser, options),
        'report_id': process_report_id_argument(parser, options),
        'api_key': process_api_key_argument(parser, options),
        'api_secret': process_api_secret_argument(parser, options),
        'taapi_key': process_taapi_key_argument(parser, options),
        'api_url': process_api_url_argument(parser, options),
        'taapi_url': process_taapi_url_argument(parser, options),
        'strategy': process_strategy_argument(parser, options),
        'debug': process_debug_argument(parser, options),
        'analyze_risk': process_analyze_risk_argument(parser, options),
        'side': process_side_argument(parser, options),
        'profit_baby': process_profit_baby_argument(parser, options),
        'interval': process_interval_argument(parser, options),
        'period 14': process_period_argument(parser, options),
        'stop_loss': process_stop_loss_argument(parser, options),
        'take_profit': process_take_profit_argument(parser, options),
        'trailing_stop': process_trailing_stop_argument(parser, options),
        'test': process_test_argument(parser, options),
        'price_movement': process_price_movement_argument(parser, options),
        'rsi_top': process_rsi_top_argument(parser, options),
        'rsi_bottom': process_rsi_bottom_argument(parser, options),
        'rsi_period': process_rsi_period_argument(parser, options),
        'rsi_backtrack': process_rsi_backtrack_argument(parser, options),
        'rsi_backtracks': process_rsi_backtracks_argument(parser, options),
        'rsi_chart': process_rsi_chart_argument(parser, options),
        'rsi_interval': process_rsi_interval_argument(parser, options),
        'volume_movement': process_volume_movement_argument(parser, options),
        'volume_interval': process_volume_interval_argument(parser, options),
        'ma_period': process_ma_period_argument(parser, options),
        'ma_backtrack': process_ma_backtrack_argument(parser, options),
        'ma_backtracks': process_ma_backtracks_argument(parser, options),
        'ma_chart': process_ma_chart_argument(parser, options),
        'ma_interval': process_ma_interval_argument(parser, options),
        'ema_period': process_ema_period_argument(parser, options),
        'ema_backtrack': process_ema_backtrack_argument(parser, options),
        'ema_backtracks': process_ema_backtracks_argument(parser, options),
        'ema_chart': process_ema_chart_argument(parser, options),
        'ema_interval': process_ema_interval_argument(parser, options),
        'macd_backtrack': process_macd_backtrack_argument(parser, options),
        'macd_backtracks': process_macd_backtracks_argument(parser, options),
        'macd_chart': process_macd_chart_argument(parser, options),
        'macd_fast_period': process_macd_fast_period_argument(parser, options),
        'macd_slow_period': process_macd_slow_period_argument(parser, options),
        'macd_signal_period': process_macd_signal_period_argument(parser, options),
        'macd_interval': process_macd_interval_argument(parser, options),
        'adx_period': process_adx_period_argument(parser, options),
        'adx_backtrack': process_adx_backtrack_argument(parser, options),
        'adx_backtracks': process_adx_backtracks_argument(parser, options),
        'adx_chart': process_adx_chart_argument(parser, options),
        'adx_interval': process_adx_interval_argument(parser, options),
        'vwap_period': process_vwap_period_argument(parser, options),
        'vwap_backtrack': process_vwap_backtrack_argument(parser, options),
        'vwap_backtracks': process_vwap_backtracks_argument(parser, options),
        'vwap_chart': process_vwap_chart_argument(parser, options),
        'vwap_interval': process_vwap_interval_argument(parser, options),
    }
    return processed

def process_price_movement_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.price_movement
    if value == None:
        log.warning(
            'No Price movement provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['price-movement'])
        )
        return False
    AR_DEFAULT['price-movement'] = value
    stdout_msg(
        'Price movement setup ({})'.format(AR_DEFAULT['price-movement']), ok=True
    )
    return True

def process_profit_baby_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.profit_baby
    if value == None:
        log.warning('No Profit BABY!! provided.')
        return False
    AR_DEFAULT['profit-baby'] = value
    stdout_msg(
        'Profit BABY!! setup ({})'.format(AR_DEFAULT['profit-baby']), ok=True
    )
    return True

def process_report_id_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.report_id
    if value == None:
        log.warning('No Report ID provided.')
        return False
    AR_DEFAULT['report-id'] = value
    stdout_msg(
        'Report ID setup ({})'.format(AR_DEFAULT['report-id']), ok=True
    )
    return True

def process_silence_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.silence
    if value == None:
        log.warning(
            'No Silence flag provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['silence'])
        )
        return False
    AR_DEFAULT['silence'] = value
    stdout_msg(
        'Silence flag setup ({})'.format(AR_DEFAULT['silence']), ok=True
    )
    return True

def process_action_csv_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.action_csv
    if value == None:
        log.warning(
            'No Action provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['action'])
        )
        return False
    AR_DEFAULT['action'] = value
    stdout_msg(
        'Action setup ({})'.format(AR_DEFAULT['action']), ok=True
    )
    return True

def process_base_currency_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.base_currency
    if value == None:
        log.warning(
            'No Base currency provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['base-currency'])
        )
        return False
    AR_DEFAULT['base-currency'] = value
    stdout_msg(
        'Base currency setup ({})'.format(AR_DEFAULT['base-currency']), ok=True
    )
    return True

def process_quote_currency_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.quote_currency
    if value == None:
        log.warning(
            'No Quote currency provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['quote-currency'])
        )
        return False
    AR_DEFAULT['quote-currency'] = value
    stdout_msg(
        'Quote currency setup ({})'.format(AR_DEFAULT['quote-currency']), ok=True
    )
    return True

def process_ticker_symbol_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ticker_symbol
    if value == None:
        log.warning(
            'No Ticker symbol provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ticker-symbol'])
        )
        return False
    AR_DEFAULT['ticker-symbol'] = value
    stdout_msg(
        'Ticker symbol setup ({})'.format(AR_DEFAULT['ticker-symbol']), ok=True
    )
    return True

def process_risk_tolerance_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.risk_tolerance
    if value == None:
        log.warning(
            'No Risk tolerance provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['risk-tolerance'])
        )
        return False
    valid_labels = {
        'high': 5,
        'mid-high': 4,
        'mid': 3,
        'low-mid': 2,
        'low': 1,
    }
    if isinstance(value, int):
        AR_DEFAULT['risk-tolerance'] = value
    elif isinstance(value, str):
        if value.lower() not in valid_labels.keys():
            log.error(
                'Invalid risk tolerance label! ({}) Defaulting to ({}).'\
                .format(value, AR_DEFAULT['risk-tolerance'])
            )
            return False
        AR_DEFAULT['risk-tolerance'] = valid_labels[value.lower()]
    stdout_msg(
        'Risk tolerance setup ({})'.format(AR_DEFAULT['risk-tolerance']), ok=True
    )
    return True

def process_api_key_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.api_key
    if value == None:
        log.warning(
            'No API key provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['api-key'])
        )
        return False
    AR_DEFAULT['api-key'] = value
    stdout_msg(
        'API key setup ({})'.format(AR_DEFAULT['api-key']), ok=True
    )
    return True

def process_api_secret_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.api_secret
    if value == None:
        log.warning(
            'No API secret key provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['api-secret'])
        )
        return False
    AR_DEFAULT['api-secret'] = value
    stdout_msg(
        'API secret key setup ({})'.format(AR_DEFAULT['api-secret']), ok=True
    )
    return True

def process_taapi_key_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.taapi_key
    if value == None:
        log.warning(
            'No Taapi key provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['taapi-key'])
        )
        return False
    AR_DEFAULT['taapi-key'] = value
    stdout_msg(
        'Taapi key setup ({})'.format(AR_DEFAULT['taapi-key']), ok=True
    )
    return True

def process_api_url_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.api_url
    if value == None:
        log.warning(
            'No API URL provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['api-url'])
        )
        return False
    AR_DEFAULT['api-url'] = value
    stdout_msg(
        'API URL setup ({})'.format(AR_DEFAULT['api-url']), ok=True
    )
    return True

def process_taapi_url_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.taapi_url
    if value == None:
        log.warning(
            'No Taapi URL provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['taapi-url'])
        )
        return False
    AR_DEFAULT['taapi-url'] = value
    stdout_msg(
        'Taapi URL setup ({})'.format(AR_DEFAULT['taapi-url']), ok=True
    )
    return True

def process_strategy_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.strategy
    if value == None:
        log.warning(
            'No Strategy provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['strategy'])
        )
        return False
    AR_DEFAULT['strategy'] = value
    stdout_msg(
        'Strategy setup ({})'.format(AR_DEFAULT['strategy']), ok=True
    )
    return True

def process_debug_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.debug
    if value == None:
        log.warning(
            'No Debug flag provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['debug'])
        )
        return False
    AR_DEFAULT['debug'] = value
    stdout_msg(
        'Debug falg setup ({})'.format(AR_DEFAULT['debug']), ok=True
    )
    return True

def process_analyze_risk_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.analyze_risk
    if value == None:
        log.warning(
            'No Risk Analysis flag provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['analyze-risk'])
        )
        return False
    AR_DEFAULT['analyze-risk'] = value
    stdout_msg(
        'Risk Analysis flag setup ({})'.format(AR_DEFAULT['analyze-risk']), ok=True
    )
    return True

def process_side_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.side
    if value == None:
        log.warning(
            'No Side provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['side'])
        )
        return False
    AR_DEFAULT['side'] = value
    stdout_msg(
        'Side setup ({})'.format(AR_DEFAULT['side']), ok=True
    )
    return True

def process_interval_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.interval
    if value == None:
        log.warning(
            'No Interval provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['interval'])
        )
        return False
    AR_DEFAULT['interval'] = value
    stdout_msg(
        'Interval setup ({})'.format(AR_DEFAULT['interval']), ok=True
    )
    return True

def process_period_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.period
    if value == None:
        log.warning(
            'No Period provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['period'])
        )
        return False
    AR_DEFAULT['period'] = value
    stdout_msg(
        'Period setup ({})'.format(AR_DEFAULT['period']), ok=True
    )
    return True

def process_stop_loss_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.stop_loss
    if value == None:
        log.warning(
            'No Stop loss provided. Defaulting to ({}%).'\
            .format(AR_DEFAULT['stop-loss'])
        )
        return False
    AR_DEFAULT['stop-loss'] = value
    stdout_msg(
        'Stop loss setup ({}%)'.format(AR_DEFAULT['stop-loss']), ok=True
    )
    return True

def process_take_profit_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.take_profit
    if value == None:
        log.warning(
            'No Take profit provided. Defaulting to ({}%).'\
            .format(AR_DEFAULT['take-profit'])
        )
        return False
    AR_DEFAULT['take-profit'] = value
    stdout_msg(
        'Take profit setup ({}%)'.format(AR_DEFAULT['take-profit']), ok=True
    )
    return True

def process_trailing_stop_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.trailing_stop
    if value == None:
        log.warning(
            'No Trailing stop provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['trailing-stop'])
        )
        return False
    AR_DEFAULT['trailing-stop'] = value
    stdout_msg(
        'Trailing stop setup ({}%)'.format(AR_DEFAULT['trailing-stop']), ok=True
    )
    return True

def process_test_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.test
    if value == None:
        log.warning(
            'No Test flag provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['test'])
        )
        return False
    AR_DEFAULT['test'] = value
    stdout_msg(
        'Test flag setup ({})'.format(AR_DEFAULT['test']), ok=True
    )
    return True

def process_rsi_top_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.rsi_top
    if value == None:
        log.warning(
            'No RSI top provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['rsi-top'])
        )
        return False
    AR_DEFAULT['rsi-top'] = value
    stdout_msg(
        'RSI top setup ({})'.format(AR_DEFAULT['rsi-top']), ok=True
    )
    return True

def process_rsi_bottom_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.rsi_bottom
    if value == None:
        log.warning(
            'No RSI bottom provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['rsi-bottom'])
        )
        return False
    AR_DEFAULT['rsi-bottom'] = value
    stdout_msg(
        'RSI bottom setup ({})'.format(AR_DEFAULT['rsi-bottom']), ok=True
    )
    return True

def process_rsi_period_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.rsi_period
    if value == None:
        log.warning(
            'No RSI period provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['rsi-period'])
        )
        return False
    AR_DEFAULT['rsi-period'] = value
    stdout_msg(
        'RSI period setup ({})'.format(AR_DEFAULT['rsi-period']), ok=True
    )
    return True

def process_rsi_backtrack_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.rsi_backtrack
    if value == None:
        log.warning(
            'No RSI backtrack provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['rsi-backtrack'])
        )
        return False
    AR_DEFAULT['rsi-backtrack'] = value
    stdout_msg(
        'RSI backtrack setup ({})'.format(AR_DEFAULT['rsi-backtrack']), ok=True
    )
    return True

def process_rsi_backtracks_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.rsi_backtracks
    if value == None:
        log.warning(
            'No RSI backtracks provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['rsi-backtracks'])
        )
        return False
    AR_DEFAULT['rsi-backtracks'] = value
    stdout_msg(
        'RSI backtracks setup ({})'.format(AR_DEFAULT['rsi-backtracks']), ok=True
    )
    return True

def process_rsi_chart_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.rsi_chart
    if value == None:
        log.warning(
            'No RSI chart provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['rsi-chart'])
        )
        return False
    AR_DEFAULT['rsi-chart'] = value
    stdout_msg(
        'RSI chart setup ({})'.format(AR_DEFAULT['rsi-chart']), ok=True
    )
    return True

def process_rsi_interval_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.rsi_interval
    if value == None:
        log.warning(
            'No RSI interval provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['rsi-interval'])
        )
        return False
    AR_DEFAULT['rsi-interval'] = value
    stdout_msg(
        'RSI interval setup ({})'.format(AR_DEFAULT['rsi-interval']), ok=True
    )
    return True

def process_volume_movement_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.volume_movement
    if value == None:
        log.warning(
            'No Volume movement provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['volume-interval'])
        )
        return False
    AR_DEFAULT['volume-movement'] = value
    stdout_msg(
        'Volume movement setup ({})'.format(AR_DEFAULT['volume-movement']), ok=True
    )
    return True

def process_volume_interval_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.volume_interval
    if value == None:
        log.warning(
            'No Volume interval provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['volume-interval'])
        )
        return False
    AR_DEFAULT['volume-interval'] = value
    stdout_msg(
        'Volume interval setup ({})'.format(AR_DEFAULT['volume-interval']), ok=True
    )
    return True

def process_ma_period_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ma_period
    if value == None:
        log.warning(
            'No MA period provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ma-period'])
        )
        return False
    AR_DEFAULT['ma-period'] = value
    stdout_msg(
        'MA period setup ({})'.format(AR_DEFAULT['ma-period']), ok=True
    )
    return True

def process_ma_backtrack_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ma_backtracks
    if value == None:
        log.warning(
            'No MA backtrack provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ma-backtrack'])
        )
        return False
    AR_DEFAULT['ma-backtrack'] = value
    stdout_msg(
        'MA backtrack setup ({})'.format(AR_DEFAULT['ma-backtrack']), ok=True
    )
    return True

def process_ma_backtracks_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ma_backtracks
    if value == None:
        log.warning(
            'No MA backtracks provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ma-backtracks'])
        )
        return False
    AR_DEFAULT['ma-backtracks'] = value
    stdout_msg(
        'MA backtracks setup ({})'.format(AR_DEFAULT['ma-backtracks']), ok=True
    )
    return True

def process_ma_chart_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ma_chart
    if value == None:
        log.warning(
            'No MA chart provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ma-chart'])
        )
        return False
    AR_DEFAULT['ma-chart'] = value
    stdout_msg(
        'MA chart setup ({})'.format(AR_DEFAULT['ma-chart']), ok=True
    )
    return True

def process_ma_interval_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ma_interval
    if value == None:
        log.warning(
            'No MA interval provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ma-interval'])
        )
        return False
    AR_DEFAULT['ma-interval'] = value
    stdout_msg(
        'MA interval setup ({})'.format(AR_DEFAULT['ma-interval']), ok=True
    )
    return True

def process_ema_period_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ema_period
    if value == None:
        log.warning(
            'No EMA period provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ema-period'])
        )
        return False
    AR_DEFAULT['ema-period'] = value
    stdout_msg(
        'EMA period setup ({})'.format(AR_DEFAULT['ema-period']), ok=True
    )
    return True

def process_ema_backtrack_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ema_backtrack
    if value == None:
        log.warning(
            'No EMA backtrack provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ema-backtrack'])
        )
        return False
    AR_DEFAULT['ema-backtrack'] = value
    stdout_msg(
        'EMA backtrack setup ({})'.format(AR_DEFAULT['ema-backtrack']), ok=True
    )
    return True

def process_ema_backtracks_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ema_backtracks
    if value == None:
        log.warning(
            'No EMA backtracks provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ema-backtracks'])
        )
        return False
    AR_DEFAULT['ema-backtracks'] = value
    stdout_msg(
        'EMA backtracks setup ({})'.format(AR_DEFAULT['ema-backtracks']), ok=True
    )
    return True

def process_ema_chart_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ema_chart
    if value == None:
        log.warning(
            'No EMA chart provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ema-chart'])
        )
        return False
    AR_DEFAULT['ema-chart'] = value
    stdout_msg(
        'EMA chart setup ({})'.format(AR_DEFAULT['ema-chart']), ok=True
    )
    return True

def process_ema_interval_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.ema_interval
    if value == None:
        log.warning(
            'No EMA interval provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['ema-interval'])
        )
        return False
    AR_DEFAULT['ema-interval'] = value
    stdout_msg(
        'EMA interval setup ({})'.format(AR_DEFAULT['ema-interval']), ok=True
    )
    return True

def process_macd_backtrack_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.macd_backtrack
    if value == None:
        log.warning(
            'No MACD backtrack provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['macd-backtrack'])
        )
        return False
    AR_DEFAULT['macd-backtrack'] = value
    stdout_msg(
        'MACD backtrack setup ({})'.format(AR_DEFAULT['macd-backtrack']), ok=True
    )
    return True

def process_macd_backtracks_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.macd_backtracks
    if value == None:
        log.warning(
            'No MACD backtracks provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['macd-backtracks'])
        )
        return False
    AR_DEFAULT['macd-backtracks'] = value
    stdout_msg(
        'MACD backtracks setup ({})'.format(AR_DEFAULT['macd-backtracks']), ok=True
    )
    return True

def process_macd_chart_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.macd_chart
    if value == None:
        log.warning(
            'No MACD chart provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['macd-chart'])
        )
        return False
    AR_DEFAULT['macd-chart'] = value
    stdout_msg(
        'MACD chart setup ({})'.format(AR_DEFAULT['macd-chart']), ok=True
    )
    return True

def process_macd_fast_period_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.macd_fast_period
    if value == None:
        log.warning(
            'No MACD fast period provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['macd-fast-period'])
        )
        return False
    AR_DEFAULT['macd-fast-period'] = value
    stdout_msg(
        'MACD fast period setup ({})'.format(AR_DEFAULT['macd-fast-period']), ok=True
    )
    return True

def process_macd_slow_period_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.macd_slow_period
    if value == None:
        log.warning(
            'No MACD slow period provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['macd-slow-period'])
        )
        return False
    AR_DEFAULT['macd-slow-period'] = value
    stdout_msg(
        'MACD slow period setup ({})'.format(AR_DEFAULT['macd-slow-period']), ok=True
    )
    return True

def process_macd_signal_period_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.macd_signal_period
    if value == None:
        log.warning(
            'No MACD signal provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['macd-signal-period'])
        )
        return False
    AR_DEFAULT['macd-signal-period'] = value
    stdout_msg(
        'MACD signal setup ({})'.format(AR_DEFAULT['macd-signal-period']), ok=True
    )
    return True

def process_macd_interval_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.macd_interval
    if value == None:
        log.warning(
            'No MACD interval provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['macd-interval'])
        )
        return False
    AR_DEFAULT['macd-interval'] = value
    stdout_msg(
        'MACD interval setup ({})'.format(AR_DEFAULT['macd-interval']), ok=True
    )
    return True

def process_adx_period_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.adx_period
    if value == None:
        log.warning(
            'No ADX period provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['adx-period'])
        )
        return False
    AR_DEFAULT['adx-period'] = value
    stdout_msg(
        'ADX period setup ({})'.format(AR_DEFAULT['adx-period']), ok=True
    )
    return True

def process_adx_backtrack_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.adx_backtrack
    if value == None:
        log.warning(
            'No ADX backtrack provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['adx-backtrack'])
        )
        return False
    AR_DEFAULT['adx-backtrack'] = value
    stdout_msg(
        'ADX backtrack setup ({})'.format(AR_DEFAULT['adx-backtrack']), ok=True
    )
    return True

def process_adx_backtracks_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.adx_backtracks
    if value == None:
        log.warning(
            'No ADX backtracks provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['adx-backtracks'])
        )
        return False
    AR_DEFAULT['adx-backtracks'] = value
    stdout_msg(
        'ADX backtracks setup ({})'.format(AR_DEFAULT['adx-backtracks']), ok=True
    )
    return True

def process_adx_chart_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.adx_chart
    if value == None:
        log.warning(
            'No ADX chart provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['adx-chart'])
        )
        return False
    AR_DEFAULT['adx-chart'] = value
    stdout_msg(
        'ADX chart setup ({})'.format(AR_DEFAULT['adx-chart']), ok=True
    )
    return True

def process_adx_interval_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.adx_interval
    if value == None:
        log.warning(
            'No ADX interval provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['adx-interval'])
        )
        return False
    AR_DEFAULT['adx-interval'] = value
    stdout_msg(
        'ADX interval setup ({})'.format(AR_DEFAULT['adx-interval']), ok=True
    )
    return True

def process_vwap_period_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.vwap_period
    if value == None:
        log.warning(
            'No VWAP period provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['vwap-period'])
        )
        return False
    AR_DEFAULT['vwap-period'] = value
    stdout_msg(
        'VWAP period setup ({})'.format(AR_DEFAULT['vwap-period']), ok=True
    )
    return True

def process_vwap_backtrack_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.vwap_backtrack
    if value == None:
        log.warning(
            'No VWAP backtrack provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['vwap-backtrack'])
        )
        return False
    AR_DEFAULT['vwap-backtrack'] = value
    stdout_msg(
        'VWAP backtrack setup ({})'.format(AR_DEFAULT['vwap-backtrack']), ok=True
    )
    return True

def process_vwap_backtracks_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.vwap_backtracks
    if value == None:
        log.warning(
            'No VWAP backtracks provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['vwap-backtracks'])
        )
        return False
    AR_DEFAULT['vwap-backtracks'] = value
    stdout_msg(
        'VWAP backtracks setup ({})'.format(AR_DEFAULT['vwap-backtracks']), ok=True
    )
    return True

def process_vwap_chart_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.vwap_chart
    if value == None:
        log.warning(
            'No VWAP chart provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['vwap-chart'])
        )
        return False
    AR_DEFAULT['vwap-chart'] = value
    stdout_msg(
        'VWAP chart setup ({})'.format(AR_DEFAULT['vwap-chart']), ok=True
    )
    return True

def process_vwap_interval_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.vwap_interval
    if value == None:
        log.warning(
            'No VWAP interval provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['vwap-interval'])
        )
        return False
    AR_DEFAULT['vwap-interval'] = value
    stdout_msg(
        'VWAP interval setup ({})'.format(AR_DEFAULT['vwap-interval']), ok=True
    )
    return True

def process_config_file_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    file_path = options.config_file_path
    if file_path == None:
        log.warning(
            'No config file provided. Defaulting to ({}/{}).'\
            .format(AR_DEFAULT['conf-dir'], AR_DEFAULT['conf-file'])
        )
        return False
    AR_DEFAULT['conf-dir'] = filter_directory_from_path(file_path)
    AR_DEFAULT['conf-file'] = filter_file_name_from_path(file_path)
    load_config_json()
    stdout_msg(
        'Config file setup ({})'.format(AR_DEFAULT['conf-file']), ok=True
    )
    return True

def process_debug_mode_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    debug_mode = options.debug
    if debug_mode == None:
        log.warning(
            'Debug mode flag not specified. '
            'Defaulting to ({}).'.format(AR_DEFAULT['debug'])
        )
        return False
    AR_DEFAULT['debug'] = debug_mode
    stdout_msg(
        'Debug mode setup ({})'.format(AR_DEFAULT['debug']), ok=True
    )
    return True

def process_log_file_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    file_path = options.log_file_path
    if file_path == None:
        log.warning(
            'No log file provided. Defaulting to ({}/{}).'\
            .format(AR_DEFAULT['log-dir'], AR_DEFAULT['log-file'])
        )
        return False
    AR_DEFAULT['log-dir'] = filter_directory_from_path(file_path)
    AR_DEFAULT['log-file'] = filter_file_name_from_path(file_path)
    stdout_msg(
        'Log file setup ({})'.format(AR_DEFAULT['log-file']), ok=True
    )
    return True

def process_warning(warning):
    log.warning(warning['msg'])
    print('[ WARNING ]:', warning['msg'], 'Details:', warning['details'])
    return warning

def process_error(error):
    log.error(error['msg'])
    print('[ ERROR ]:', error['msg'], 'Details:', error['details'])
    return error

# PARSERS

def add_command_line_parser_options(parser):
    log.debug('')
    parser.add_option(
        '-c', '--config-file', dest='config_file_path', type='string',
        help='Configuration file to load default values from.', metavar='FILE_PATH'
    )
    parser.add_option(
        '-D', '--debug', dest='debug', action='store_true',
        help='Display more verbose output and log messages.'
    )
    parser.add_option(
        '-l', '--log-file', dest='log_file_path', type='string',
        help='Path to the log file.', metavar='FILE_PATH'
    )
    parser.add_option(
        '-Z', '--ticker-symbol', dest='ticker_symbol', type='string',
        help='Ticker symbol to use for action. Symbol names are always uppercase, '
             'with the coin separated by a forward slash and the market: COIN/MARKET. '
             'For example: BTC/USDT Bitcoin to Tether, or LTC/BTC '
             'Litecoin to Bitcoin... ', metavar='SYMBOL'
    )
    parser.add_option(
        '-q', '--quote-currency', dest='quote_currency', type='string',
        help='Quote currency to use for action.', metavar='SYMBOL'
    )
    parser.add_option(
        '-b', '--base-currency', dest='base_currency', type='string',
        help='Base currency to use for action.', metavar='SYMBOL'
    )
    parser.add_option(
        '-p', '--period', dest='period', type='string',
        help='Period/Number of candles to use when calculating indicators for '
             'action (trading or reporting).', metavar='PERIOD'
    )
    parser.add_option(
        '-i', '--interval', dest='interval', type='string',
        help='General interval or time frame for action. Supported time frames: '
             '1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w. So if you re interested '
             'in values on hourly candles, use interval=1h, for daily values use '
             'interval=1d, etc..', metavar='INTERVAL'
    )
    parser.add_option(
        '-t', '--side', dest='side', type='string', metavar='SIDE',
        help='Trading side to be used for action - valid values include '
        '(buy, sell, auto). Default is {}'.format(AR_DEFAULT['side']),
    )
    parser.add_option(
        '-A', '--analyze-risk', dest='analyze_risk', action='store_true',
        help='Flag to enable risk analysis with the specified risk tolerance '
             'before commiting to a trade, either manual or automatic.',
    )
    parser.add_option(
        '-s', '--silence', dest='silence', action='store_true',
        help='Flag to enable suppression of STDOUT messages.',
    )
    parser.add_option(
        '-T', '--strategy', dest='strategy', type='string', metavar='CSV',
        help='Strategies to apply when taking into consideration the generation '
             'of buy and sell signals. Default is {}'.format(AR_DEFAULT['strategy']),
    )
    parser.add_option(
        '-u', '--taapi-url', dest='taapi_url', type='string', metavar='URL',
        help='Taapi API URL target. Default is {}'.format(AR_DEFAULT['taapi-url']),
    )
    parser.add_option(
        '-U', '--api-url', dest='api_url', type='string', metavar='URL',
        help='Binance API URL target. Default is {}'.format(AR_DEFAULT['api-url']),
    )
    parser.add_option(
        '-k', '--taapi-key', dest='taapi_key', type='string',metavar='KEY',
        help='Taapi API Key - trading indicators wont work without it..',
    )
    parser.add_option(
        '-S', '--api-secret', dest='api_secret', type='string', metavar='KEY',
        help='Binance API Secret Key - nothing works without it.',
    )
    parser.add_option(
        '-K', '--api-key', dest='api_key', type='string', metavar='KEY',
        help='Binance API Key - nothing works without it.',
    )
    parser.add_option(
        '-r', '--report-id', dest='report_id', type='string', metavar='CSV',
        help='Report IDs given as a CSV string to use for action.',
    )
    parser.add_option(
        '-R', '--risk-tolerance', dest='risk_tolerance', type='string', metavar='LEVEL',
        help='Risk tolerance taken into account during the risk analysis process. '
             'Valid values include (low or 1 | low-mid or 2 | mid or 3 | mid-high '
             'or 4 | high or 5). Default is {}'.format(AR_DEFAULT['risk-tolerance']),
    )
    parser.add_option(
        '-P', '--profit-baby', dest='profit_baby', type='string', metavar='PERCENTAGE',
        help='Stop trading when hitting this profit target, relative to the '
             'account value when the bot was initialized. '
             'Default is {}%'.format(AR_DEFAULT['risk-tolerance']),
    )
    parser.add_option(
        '-a', '--action', dest='action_csv', type='string', metavar='CSV',
        help='Action to execute - valid values include one or more of the '
             'following labels given as a CSV string: (start-watchdog | '
             'stop-watchdog | trade-report | withdrawal-report | deposit-report | '
             'single-trade | view-trade-report | view-withdrawal-report | '
             'view-deposit-report | account-details | market-details | '
             'supported-coins | supported-tickers)',
    )
    parser.add_option(
        '', '--stop-loss', dest='stop_loss', type='int', metavar='PERCENTAGE',
        help='Price percentage of when to cut your losses in a trade.',
    )
    parser.add_option(
        '', '--trailing-stop', dest='trailing_stop', type='int', metavar='PERCENTAGE',
        help='Percentage to continuously take profit from a trade before '
             'hitting the --take-profit value.',
    )
    parser.add_option(
        '', '--take-profit', dest='take_profit', type='int', metavar='PERCENTAGE',
        help='Price percentage of when to cash in on a trade.',
    )
    parser.add_option(
        '', '--vwap-interval', dest='vwap_interval', type='string', metavar='INTERVAL',
        help='Time interval used when computing the Volume-Weighted Average Price. '
             'Supported time frames: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w.',
    )
    parser.add_option(
        '', '--vwap-chart', dest='vwap_chart', type='string', metavar='TYPE',
        help='Type of chart used when computing the Relative Strength Index. '
             'The chart parameter accepts one of two values: candles or heikinashi. '
             'Candles is the default, but if you set this to heikinashi, the '
             'indicator values will be calculated using Heikin Ashi candles. ',
    )
    parser.add_option(
        '', '--vwap-period', dest='vwap_period', type='int', metavar='PERIOD',
        help='Period/Number of candles used when computing the Volume-Weighted '
             'Average Price.',
    )
    parser.add_option(
        '', '--vwap-backtracks', dest='vwap_backtracks', type='int',
        help='Number of candles/periods to backtrack when computing '
             'Volume-Weighted Average Price history. The backtracks parameter returns '
             'the indicator value calculated on every candle for the past X candles. '
             'For example, if you want to know what the indicator was every hour for '
             'the past 12 hours, you use backtracks=12. As a result, you will '
             'get 12 values back.', metavar='PERIOD'
    )
    parser.add_option(
        '', '--vwap-backtrack', dest='vwap_backtrack', type='int',
        help='Number of candles/periods to backtrack when computing '
             'Volume-Weighted Average Price history. The backtrack parameter removes '
             'candles from the data set and calculates the indicator value X amount of '
             'candles back. So, if you’re fetching the indicator on the hourly and you '
             'want to know what the indicator was 5 hours ago, set backtrack=5. '
             'The default is 0 and a maximum is 50.', metavar='PERIOD'
    )
    parser.add_option(
        '', '--adx-chart', dest='adx_chart', type='string', metavar='TYPE',
        help='Type of chart used when computing the Relative Strength Index. '
             'The chart parameter accepts one of two values: candles or heikinashi. '
             'Candles is the default, but if you set this to heikinashi, the '
             'indicator values will be calculated using Heikin Ashi candles. ',
    )
    parser.add_option(
        '', '--adx-interval', dest='adx_interval', type='string', metavar='INTERVAL',
        help='Time interval used when computing the Average Directional IndeX. '
             'Supported time frames: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w.',
    )
    parser.add_option(
        '', '--adx-period', dest='adx_period', type='int', metavar='PERIOD',
        help='Period/Number of candles used when computing the '
             'Average Directional IndeX.',
    )
    parser.add_option(
        '', '--adx-backtrack', dest='adx_backtrack', type='int',
        help='Number of candles/periods to backtrack when computing '
             'Average Directional IndeX history. The backtrack parameter removes '
             'candles from the data set and calculates the indicator value X amount of '
             'candles back. So, if you’re fetching the indicator on the hourly and you '
             'want to know what the indicator was 5 hours ago, set backtrack=5. '
             'The default is 0 and a maximum is 50.', metavar='PERIOD'
    )
    parser.add_option(
        '', '--adx-backtracks', dest='adx_backtracks', type='int',
        help='Number of candles/periods to backtrack when computing '
             'Average Directional IndeX history. The backtracks parameter returns '
             'the indicator value calculated on every candle for the past X candles. '
             'For example, if you want to know what the indicator was every hour for '
             'the past 12 hours, you use backtracks=12. As a result, you will '
             'get 12 values back.', metavar='PERIOD'
    )
    parser.add_option(
        '', '--macd-interval', dest='macd_interval', type='string', metavar='INTERVAL',
        help='Time interval used when computing the Moving Average Divergence Convergence. '
             'Supported time frames: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w.',
    )
    parser.add_option(
        '', '--macd-signal-period', dest='macd_signal_period', type='int', metavar='PERIOD',
        help='Period/Number of candles used when computing the Moving Average Divergence Convergence signal.',
    )
    parser.add_option(
        '', '--macd-slow-period', dest='macd_slow_period', type='int', metavar='PERIOD',
        help='Slow Period used when computing the Moving Average Divergence Convergence.',
    )
    parser.add_option(
        '', '--macd-fast-period', dest='macd_fast_period', type='int', metavar='PERIOD',
        help='Fast Period used when computing the Moving Average Divergence Convergence.',
    )
    parser.add_option(
        '', '--macd-chart', dest='macd_chart', type='string', metavar='TYPE',
        help='Type of chart used when computing the Relative Strength Index. '
             'The chart parameter accepts one of two values: candles or heikinashi. '
             'Candles is the default, but if you set this to heikinashi, the '
             'indicator values will be calculated using Heikin Ashi candles. ',
    )
    parser.add_option(
        '', '--macd-backtracks', dest='macd_backtracks', type='int',
        help='Number of candles/periods to backtrack when computing '
             'Moving Average Divergence Convergence history. The backtracks parameter returns '
             'the indicator value calculated on every candle for the past X candles. '
             'For example, if you want to know what the indicator was every hour for '
             'the past 12 hours, you use backtracks=12. As a result, you will '
             'get 12 values back.', metavar='PERIOD'
    )
    parser.add_option(
        '', '--macd-backtrack', dest='macd_backtrack', type='int',
        help='Number of candles/periods to backtrack when computing '
             'Moving Average Divergence Convergence history. The backtrack parameter removes '
             'candles from the data set and calculates the indicator value X amount of '
             'candles back. So, if you’re fetching the indicator on the hourly and you '
             'want to know what the indicator was 5 hours ago, set backtrack=5. '
             'The default is 0 and a maximum is 50.', metavar='PERIOD'
    )
    parser.add_option(
        '', '--ema-interval', dest='ema_interval', type='string', metavar='INTERVAL',
        help='Time interval used when computing the Estimated Moving Average. '
             'Supported time frames: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w.',
    )
    parser.add_option(
        '', '--ema-chart', dest='ema_chart', type='string', metavar='TYPE',
        help='Type of chart used when computing the Estimated Moving Average. '
             'The chart parameter accepts one of two values: candles or heikinashi. '
             'Candles is the default, but if you set this to heikinashi, the '
             'indicator values will be calculated using Heikin Ashi candles. ',
    )
    parser.add_option(
        '', '--ema-period', dest='ema_period', type='int', metavar='PERIOD',
        help='Period/Number of candles used when computing the Estimated Moving Average.',
    )
    parser.add_option(
        '', '--ema-backtracks', dest='ema_backtracks', type='int', metavar='PERIOD',
        help='Number of candles/periods to backtrack when computing '
             'Estimated Moving Average history. The backtracks parameter returns '
             'the indicator value calculated on every candle for the past X candles. '
             'For example, if you want to know what the indicator was every hour for '
             'the past 12 hours, you use backtracks=12. As a result, you will '
             'get 12 values back.',
    )
    parser.add_option(
        '', '--ema-backtrack', dest='ema_backtrack', type='int', metavar='PERIOD',
        help='Number of candles/periods to backtrack when computing '
             'Estimated Moving Average history. The backtrack parameter removes '
             'candles from the data set and calculates the indicator value X amount of '
             'candles back. So, if you’re fetching the indicator on the hourly and you '
             'want to know what the indicator was 5 hours ago, set backtrack=5. '
             'The default is 0 and a maximum is 50.',
    )
    parser.add_option(
        '', '--ma-interval', dest='ma_interval', type='string', metavar='INTERVAL',
        help='Time interval used when computing the Moving Average. '
             'Supported time frames: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w.',
    )
    parser.add_option(
        '', '--ma-chart', dest='ma_chart', type='string', metavar='TYPE',
        help='Type of chart used when computing the Moving Average. '
             'The chart parameter accepts one of two values: candles or heikinashi. '
             'Candles is the default, but if you set this to heikinashi, the '
             'indicator values will be calculated using Heikin Ashi candles. ',
    )
    parser.add_option(
        '', '--ma-period', dest='ma_period', type='int', metavar='PERIOD',
        help='Period/Number of candles used when computing the Moving Average.',
    )
    parser.add_option(
        '', '--ma-backtracks', dest='ma_backtracks', type='int',
        help='Number of candles/periods to backtrack when computing '
             'Moving Average history. The backtracks parameter returns '
             'the indicator value calculated on every candle for the past X candles. '
             'For example, if you want to know what the indicator was every hour for '
             'the past 12 hours, you use backtracks=12. As a result, you will '
             'get 12 values back.', metavar='PERIOD'
    )
    parser.add_option(
        '', '--ma-backtrack', dest='ma_backtrack', type='int',
        help='Number of candles/periods to backtrack when computing '
             'Moving Average history. The backtrack parameter removes '
             'candles from the data set and calculates the indicator value X amount of '
             'candles back. So, if you’re fetching the indicator on the hourly and you '
             'want to know what the indicator was 5 hours ago, set backtrack=5. '
             'The default is 0 and a maximum is 50.', metavar='PERIOD'
    )
    parser.add_option(
        '', '--volume-interval', dest='volume_interval', type='string',
        help='Time interval used when looking for volume movements.'
             'Supported time frames: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w.',
        metavar='INTERVAL'
    )
    parser.add_option(
        '', '--volume-movement', dest='volume_movement', type='int',
        help='Volume percentage that triggers a large volume movement for '
             'specified interval.', metavar='PERCENTAGE'
    )
    parser.add_option(
        '', '--rsi-interval', dest='rsi_interval', type='string', metavar='INTERVAL',
        help='Time interval used when computing the Relative Strength Index.'
             'Supported time frames: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w.',
    )
    parser.add_option(
        '', '--rsi-chart', dest='rsi_chart', type='string', metavar='TYPE',
        help='Type of chart used when computing the Relative Strength Index. '
             'The chart parameter accepts one of two values: candles or heikinashi. '
             'Candles is the default, but if you set this to heikinashi, the '
             'indicator values will be calculated using Heikin Ashi candles. ',
    )
    parser.add_option(
        '', '--rsi-period', dest='rsi_period', type='int', metavar='PERIOD',
        help='Period/Number of candles used when computing the Relative Strength Index.',
    )
    parser.add_option(
        '', '--rsi-bottom', dest='rsi_bottom', type='int', metavar='PERCENTAGE',
        help='Relative Strength Index percentage value considered to be low.',
    )
    parser.add_option(
        '', '--rsi-top', dest='rsi_top', type='int', metavar='PERCENTAGE',
        help='Relative Strength Index percentage value considered to be high.',
    )
    parser.add_option(
        '', '--rsi-backtracks', dest='rsi_backtracks', type='int',
        help='Number of candles/periods to backtrack. The backtracks parameter returns '
             'the indicator value calculated on every candle for the past X candles. '
             'For example, if you want to know what the indicator was every hour for '
             'the past 12 hours, you use backtracks=12. As a result, you will '
             'get 12 values back.', metavar='PERIOD'
    )
    parser.add_option(
        '', '--rsi-backtrack', dest='rsi_backtrack', type='int',
        help='Number of candles/periods to backtrack. The backtrack parameter removes '
             'candles from the data set and calculates the indicator value X amount of '
             'candles back. So, if you’re fetching the indicator on the hourly and you '
             'want to know what the indicator was 5 hours ago, set backtrack=5. '
             'The default is 0 and a maximum is 50.', metavar='PERIOD'
    )
    parser.add_option(
        '', '--price-movement', dest='price_movement', type='int',
        help='Price percentage that triggers a large price movement for '
             'specified interval.', metavar='PERCENTAGE'
    )
    parser.add_option(
        '', '--test', dest='test', action='store_true',
        help='Run actions in test mode. When creating a new order, creation and '
             'signature/recvWindow long is tested. Creates and validates a new '
             'order but does not send it into the matching engine..',
    )

def parse_command_line_arguments():
    log.debug('')
    parser = create_command_line_parser()
    add_command_line_parser_options(parser)
    return process_command_line_options(parser)

# GENERAL

# TODO
def cleanup():
    log.debug('TODO - Under construction, building...')

def update_log():
    global log
    del log
    log = log_init(
        '/'.join([AR_DEFAULT['log-dir'], AR_DEFAULT['log-file']]),
        AR_DEFAULT['log-format'], AR_DEFAULT['timestamp-format'],
        AR_DEFAULT['debug'], log_name=AR_SCRIPT_NAME
    )
    return log

#@pysnooper.snoop()
def load_config_json():
    global AR_DEFAULT
    global AR_SCRIPT_NAME
    global AR_SCRIPT_DESCRIPTION
    global AR_VERSION
    global AR_VERSION_NO
    log.debug('')
    stdout_msg('Loading config file...', info=True)
    conf_file_path = AR_DEFAULT['conf-dir'] + '/' + AR_DEFAULT['conf-file']
    if not os.path.isfile(conf_file_path):
        stdout_msg('File not found! ({})'.format(conf_file_path), nok=True)
        return False
    with open(conf_file_path, 'r', encoding='utf-8', errors='ignore') as conf_file:
        try:
            with open(conf_file_path) as fl:
                content = json.load(fl)
            AR_DEFAULT.update(content['AR_DEFAULT'])
            AR_SCRIPT_NAME = content['AR_SCRIPT_NAME']
            AR_SCRIPT_DESCRIPTION = content['AR_SCRIPT_DESCRIPTION']
            AR_VERSION = content['AR_VERSION']
            AR_VERSION_NO = content['AR_VERSION_NO']
        except Exception as e:
            log.error(e)
            stdout_msg(
                'Could not load config file! ({})'.format(conf_file_path), nok=True
            )
            return False
    stdout_msg(
        'Settings loaded from config file! ({})'.format(conf_file_path), ok=True
    )
    return True

# SETUP

#@pysnooper.snoop()
def setup_trading_bot(**kwargs):
    log.debug('')
    if not kwargs:
        kwargs = AR_DEFAULT
    bot = create_trading_bot(**kwargs)
    if not trading_bot or not isinstance(trading_bot, TradingBot):
        stdout_msg('Trading Bot setup failure!', err=True)
        return False
    enter_market = trading_bot.enter_market(**kwargs)
    if not enter_market:
        stdout_msg('Trading Bot could not enter trading market!', warn=True)
    return trading_bot

# FORMATTERS

def format_header_string():
    header = '''
    ___________________________________________________________________________

     *                          *  Asymetric Risk  *                         *
    ___________________________________________________________________________
                Excellent Regards, the Alveare Solutions #!/Society -x
    '''
    return header

# DISPLAY

def display_header():
    if AR_DEFAULT['silence']:
        return False
    stdout_msg(format_header_string(), bold=True)
    return True

# INIT

# @pysnooper.snoop()
def init_asymetric_risk(*args, **kwargs):
    log.debug('')
    display_header()
    check = check_preconditions(**kwargs)
    if not isinstance(check, int) or check != 0:
        stdout_msg('Preconditions not met!', err=True)
        return check
    handle = handle_actions(
        *args, actions=kwargs.get('action', str()).split(','), **kwargs
    )
    if not handle:
        stdout_msg('Issues detected during action execution!', warn=True)
    return 0 if not isinstance(handle, int) else handle

# MISCELLANEOUS

if __name__ == '__main__':
    config_setup = load_config_json()
    if not config_setup:
        stdout_msg('Could not load config file!', warn=True)
    parse_command_line_arguments()
    if not update_log():
        stdout_msg('Could not properly set up logger!', warn=True)
    clear_screen()
    EXIT_CODE = 1
    try:
        EXIT_CODE = init_asymetric_risk(**AR_DEFAULT)
    finally:
        cleanup()
    stdout_msg('Terminating! ({})\n'.format(EXIT_CODE), done=True)
    exit(EXIT_CODE)

# CODE DUMP

#   print(format_header_string())

#       stdout_msg(
#           '[ NOK ]: Trading bot failures detected! Exit code ({})'
#           .format(watchdog)
#       )
#   else:

#   return False if os.path.exists(AR_DEFAULT['watchdog-anchor-file']) else True

#       {
#           'error': True, 'exit': 1,
#           'description': 'Could not stop trading bot!'
#       }

#   {
#       'error': True, 'exit': 1,
#       'description': 'Trading bot watchdog terminated abruptly!',
#   }

