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

from time import sleep
from subprocess import Popen, PIPE
from src.backpack.bp_log import log_init
from src.backpack.bp_ensurance import ensure_files_exist, ensure_directories_exist
from src.backpack.bp_shell import shell_cmd
from src.backpack.bp_checkers import check_file_exists
from src.backpack.bp_general import stdout_msg, clear_screen, pretty_dict_print
from src.backpack.bp_convertors import dict2json
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
    "watchdog-anchor-file": "ar-bot.anchor",
    "log-format":           "[ %(asctime)s ] %(name)s [ %(levelname)s ] %(thread)s - %(filename)s - %(lineno)d: %(funcName)s - %(message)s",
    "timestamp-format":     "%d/%m/%Y-%H:%M:%S",
    "api-key":              os.environ.get('binance_api'),
    "api-secret":           os.environ.get('binance_secret'),
    "taapi-key":            os.environ.get('taapi_api'),
    "api-url":              'https://testnet.binance.vision/api',
    "taapi-url":            "https://api.taapi.io",
    "profit-baby":          10,
    "base-currency":        'BTC',
    "quote-currency":       'USDT',
    "period-start":         '01-10-2022',
    "period-end":           '01-11-2022',
    "risk-tolerance":       1,
    "test":                 False,
    "debug":                False,
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

def check_preconditions():
    log.debug('')
    checkers = {
        'preconditions-conf': check_config_file(),
        'preconditions-log': check_log_file(),
    }
    if False in checkers.values():
        return len([item for item in checkers.values() if item is False])
    return 0

def check_config_file():
    log.debug('')
    conf_file_path = AR_DEFAULT['conf-dir'] + "/" + AR_DEFAULT['conf-file']
    conf_dir = ensure_directories_exist(AR_DEFAULT['conf-dir'])
    exit_code = 0
    if not check_file_exists(conf_file_path):
        cmd_out, cmd_err, exit_code = shell_cmd(
            'touch ' + conf_file_path + ' &> /dev/null'
        )
    return False if exit_code != 0 else True

def check_log_file():
    log.debug('')
    log_file_path = AR_DEFAULT['log-dir'] + "/" + AR_DEFAULT['log-file']
    log_dir = ensure_directories_exist(AR_DEFAULT['log-dir'])
    exit_code = 0
    if not check_file_exists(log_file_path):
        cmd_out, cmd_err, exit_code = shell_cmd(
            'touch ' + log_file_path + ' &> /dev/null'
        )
    return False if exit_code != 0 else True

# ACTIONS

# TODO
def action_trade_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_withdrawal_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_deposit_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_single_trade(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_view_trade_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_view_withdrawal_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_view_deposit_report(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_account_details(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_market_details(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_supported_coins(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_supported_tickers(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
def action_stop_watchdog(*args, **kwargs):
    log.debug('TODO - Under construction, building...')
    if not os.path.exists(AR_DEFAULT['watchdog-anchor-file']):
        return False
    remove = os.path.remove(AR_DEFAULT['watchdog-anchor-file'])

def action_start_watchdog(*args, **kwargs):
    '''
    [ RETURN ]: Trading watchdog exit code - type int
    '''
    log.debug('')
    stdout_msg(
        '[ INFO ]: Starting {} trading bot in watchdog mode -'\
            .format(AR_SCRIPT_NAME)
    )
    stdout_msg(
        '[ WARNING ]: Consider terminating the watchdog on winning streaks '
        'to keep from loosing it again. The watchdog will not terminate itself, '
        'duhh.. Hmm, probably should automate that too.'
    )
    watchdog = trading_bot.trade_watchdog(
        *(kwargs.get('strategy', '').split(',')),
        **kwargs
    )
    return watchdog

# HANDLERS

#@pysnooper.snoop()
def handle_actions(actions=[], *args, **kwargs):
    log.debug('')
    failure_count = 0
    handlers = self.fetch_action_handlers()
    for action_label in actions:
        stdout_msg('[ INFO ]: Processing action... ({})'.format(action_label))
        if action_label not in handlers.keys():
            stdout_msg(
                '[ NOK ]: Invalid action label specified! ({})'.format(action_label)
            )
            continue
        handle = handlers[action_label](*args, **kwargs)
        if isinstance(handle, int) and handle != 0:
            stdout_msg(
                '[ NOK ]: Action ({}) failures detected! ({})'.format(action_label, handle)
            )
            failure_count += 1
            continue
        stdout_msg("[ OK ]: Action executed successfully! ({})".format(action_label))
    return True if failure_count == 0 else failure_count

# CREATORS

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

def process_profit_baby_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.profit_baby
    if value == None:
        log.warning('No Profit BABY!! provided.')
        return False
    AR_DEFAULT['profit-baby'] = value
    stdout_msg(
        '[ + ]: Profit BABY!! setup ({})'.format(AR_DEFAULT['profit-baby'])
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
        '[ + ]: Report ID setup ({})'.format(AR_DEFAULT['report-id'])
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
        '[ + ]: Silence flag setup ({})'.format(AR_DEFAULT['silence'])
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
        '[ + ]: Action setup ({})'.format(AR_DEFAULT['action'])
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
        '[ + ]: Base currency setup ({})'.format(AR_DEFAULT['base-currency'])
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
        '[ + ]: Quote currency setup ({})'.format(AR_DEFAULT['quote-currency'])
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
        '[ + ]: Ticker symbol setup ({})'.format(AR_DEFAULT['ticker-symbol'])
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
        '[ + ]: Risk tolerance setup ({})'.format(AR_DEFAULT['risk-tolerance'])
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
        '[ + ]: API key setup ({})'.format(AR_DEFAULT['api-key'])
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
        '[ + ]: API secret key setup ({})'.format(AR_DEFAULT['api-secret'])
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
        '[ + ]: Taapi key setup ({})'.format(AR_DEFAULT['taapi-key'])
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
        '[ + ]: API URL setup ({})'.format(AR_DEFAULT['api-url'])
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
        '[ + ]: Taapi URL setup ({})'.format(AR_DEFAULT['taapi-url'])
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
        '[ + ]: Strategy setup ({})'.format(AR_DEFAULT['strategy'])
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
        '[ + ]: Debug falg setup ({})'.format(AR_DEFAULT['debug'])
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
        '[ + ]: Risk Analysis flag setup ({})'.format(AR_DEFAULT['analyze-risk'])
    )
    return True

def process_side_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.sid
    if value == None:
        log.warning(
            'No Side provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['side'])
        )
        return False
    AR_DEFAULT['side'] = value
    stdout_msg(
        '[ + ]: Side setup ({})'.format(AR_DEFAULT['side'])
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
        '[ + ]: Interval setup ({})'.format(AR_DEFAULT['interval'])
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
        '[ + ]: Period setup ({})'.format(AR_DEFAULT['period'])
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
        '[ + ]: Stop loss setup ({}%)'.format(AR_DEFAULT['stop-loss'])
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
        '[ + ]: Take profit setup ({}%)'.format(AR_DEFAULT['take-profit'])
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
        '[ + ]: Trailing stop setup ({}%)'.format(AR_DEFAULT['trailing-stop'])
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
        '[ + ]: Test flag setup ({})'.format(AR_DEFAULT['test'])
    )
    return True

def process_price_movement_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.price_movement
    if value == None:
        log.warning(
            'No Price movement provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['price-interval'])
        )
        return False
    AR_DEFAULT['price-movement'] = value
    stdout_msg(
        '[ + ]: Price movement setup ({})'.format(AR_DEFAULT['price-movement'])
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
        '[ + ]: RSI top setup ({})'.format(AR_DEFAULT['rsi-top'])
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
        '[ + ]: RSI bottom setup ({})'.format(AR_DEFAULT['rsi-bottom'])
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
        '[ + ]: RSI period setup ({})'.format(AR_DEFAULT['rsi-period'])
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
        '[ + ]: RSI backtrack setup ({})'.format(AR_DEFAULT['rsi-backtrack'])
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
        '[ + ]: RSI backtracks setup ({})'.format(AR_DEFAULT['rsi-backtracks'])
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
        '[ + ]: RSI chart setup ({})'.format(AR_DEFAULT['rsi-chart'])
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
        '[ + ]: RSI interval setup ({})'.format(AR_DEFAULT['rsi-interval'])
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
        '[ + ]: Volume movement setup ({})'.format(AR_DEFAULT['volume-movement'])
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
        '[ + ]: Volume interval setup ({})'.format(AR_DEFAULT['volume-interval'])
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
        '[ + ]: MA period setup ({})'.format(AR_DEFAULT['ma-period'])
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
        '[ + ]: MA backtrack setup ({})'.format(AR_DEFAULT['ma-backtrack'])
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
        '[ + ]: MA backtracks setup ({})'.format(AR_DEFAULT['ma-backtracks'])
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
        '[ + ]: MA chart setup ({})'.format(AR_DEFAULT['ma-chart'])
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
        '[ + ]: MA interval setup ({})'.format(AR_DEFAULT['ma-interval'])
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
        '[ + ]: EMA period setup ({})'.format(AR_DEFAULT['ema-period'])
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
        '[ + ]: EMA backtrack setup ({})'.format(AR_DEFAULT['ema-backtrack'])
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
        '[ + ]: EMA backtracks setup ({})'.format(AR_DEFAULT['ema-backtracks'])
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
        '[ + ]: EMA chart setup ({})'.format(AR_DEFAULT['ema-chart'])
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
        '[ + ]: EMA interval setup ({})'.format(AR_DEFAULT['ema-interval'])
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
        '[ + ]: MACD backtrack setup ({})'.format(AR_DEFAULT['macd-backtrack'])
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
        '[ + ]: MACD backtracks setup ({})'.format(AR_DEFAULT['macd-backtracks'])
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
        '[ + ]: MACD chart setup ({})'.format(AR_DEFAULT['macd-chart'])
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
        '[ + ]: MACD fast period setup ({})'.format(AR_DEFAULT['macd-fast-period'])
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
        '[ + ]: MACD slow period setup ({})'.format(AR_DEFAULT['macd-slow-period'])
    )
    return True

def process_macd_signal_period_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    value = options.macd_signal
    if value == None:
        log.warning(
            'No MACD signal provided. Defaulting to ({}).'\
            .format(AR_DEFAULT['macd-signal'])
        )
        return False
    AR_DEFAULT['macd-signal'] = value
    stdout_msg(
        '[ + ]: MACD signal setup ({})'.format(AR_DEFAULT['macd-signal'])
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
        '[ + ]: MACD interval setup ({})'.format(AR_DEFAULT['macd-interval'])
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
        '[ + ]: ADX period setup ({})'.format(AR_DEFAULT['adx-period'])
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
        '[ + ]: ADX backtrack setup ({})'.format(AR_DEFAULT['adx-backtrack'])
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
        '[ + ]: ADX backtracks setup ({})'.format(AR_DEFAULT['adx-backtracks'])
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
        '[ + ]: ADX chart setup ({})'.format(AR_DEFAULT['adx-chart'])
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
        '[ + ]: ADX interval setup ({})'.format(AR_DEFAULT['adx-interval'])
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
        '[ + ]:  setup ({})'.format(AR_DEFAULT['vwap-period'])
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
        '[ + ]: VWAP backtrack setup ({})'.format(AR_DEFAULT['vwap-backtrack'])
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
        '[ + ]: VWAP backtracks setup ({})'.format(AR_DEFAULT['vwap-backtracks'])
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
        '[ + ]: VWAP chart setup ({})'.format(AR_DEFAULT['vwap-chart'])
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
        '[ + ]: VWAP interval setup ({})'.format(AR_DEFAULT['vwap-interval'])
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
    load_config_file()
    stdout_msg(
        '[ + ]: Config file setup ({})'.format(AR_DEFAULT['conf-file'])
    )
    return True

def process_debug_mode_argument(parser, options):
    global AR_DEFAULT
    log.debug('')
    debug_mode = options.debug_mode
    if debug_mode == None:
        log.warning(
            'Debug mode flag not specified. '
            'Defaulting to ({}).'.format(AR_DEFAULT['debug'])
        )
        return False
    AR_DEFAULT['debug'] = debug_mode
    stdout_msg(
        '[ + ]: Debug mode setup ({})'.format(AR_DEFAULT['debug'])
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
        '[ + ]: Log file setup ({})'.format(AR_DEFAULT['log-file'])
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
        '-D', '--debug-mode', dest='debug_mode', action='store_true',
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
        '-u', '--taapi-url', dest='taapi-url', type='string', metavar='URL',
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
        '-S', '--api-secret', dest='apy-secret', type='string', metavar='KEY',
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
        '-R', '--risk-tolerance', dest='api_key', type='string', metavar='LEVEL',
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
        '-a', '--action', dest='action', type='string', metavar='CSV',
        help='Action to execute - valid values include one or more of the '
             'following labels given as a CSV string: (start-watchdog | '
             'stop-watchdog | trade-report | withdrawal-report | deposit-report | '
             'single-trade | view-trade-report | view-withdrawal-report | '
             'view-deposit-report | account-details | market-details | '
             'supported-coins | supported-tickers)',
    )
    parser.add_option(
        '', '--stop-loss', dest='stop-loss', type='int', metavar='PERCENTAGE',
        help='Price percentage of when to cut your losses in a trade.',
    )
    parser.add_option(
        '', '--trailing-stop', dest='trailing-stop', type='int', metavar='PERCENTAGE',
        help='Percentage to continuously take profit from a trade before '
             'hitting the --take-profit value.',
    )
    parser.add_option(
        '', '--take-profit', dest='take-profit', type='int', metavar='PERCENTAGE',
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
        '', '--test', dest='test_flag', action='store_true',
        help='Run actions in test mode.',
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

#@pysnooper.snoop()
def load_config_json():
    log.debug('')
    global AR_DEFAULT
    global AR_SCRIPT_NAME
    global AR_SCRIPT_DESCRIPTION
    global AR_VERSION
    global AR_VERSION_NO
    stdout_msg('[ INFO ]: Loading config file...')
    conf_file_path = AR_DEFAULT['conf-dir'] + '/' + AR_DEFAULT['conf-file']
    if not os.path.isfile(conf_file_path):
        stdout_msg('[ NOK ]: File not found! ({})'.format(conf_file_path))
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
                '[ NOK ]: Could not load config file! ({})'.format(conf_file_path)
            )
            return False
    stdout_msg(
        '[ OK ]: Settings loaded from config file! ({})'.format(conf_file_path)
    )
    return True

# SETUP

def setup_trading_bot(**kwargs):
    log.debug('')
    global trading_bot
    if not kwargs:
        kwargs = AR_DEFAULT
    trading_bot = TradingBot(**kwargs)
    enter_market = trading_bot.enter_market(**kwargs)
    return trading_bot

# FORMATTERS

def format_header_string():
    header = '''
    ___________________________________________________________________________

     *                          *  Asymetric Risk  *                         *
    ___________________________________________________________________________
                     Regards, the Alveare Solutions #!/Society -x
    '''
    return header

# DISPLAY

def display_header():
    if AR_DEFAULT['silence']:
        return False
    print(format_header_string())
    return True

# INIT

@pysnooper.snoop()
def init_asymetric_risk(*args, **kwargs):
    log.debug('')
    exit_code = 0
    display_header()
    config_setup = load_config_json()
    if not config_setup:
        stdout_msg('[ WARNING ]: Could not load config file!')
    try:
        bot_setup = setup_trading_bot(**AR_DEFAULT)
    except Exception as w:
        log.warning(w)
        stdout_msg(
            '[ WARNING ]: Could not set up trading bot! Details: ({})'.format(w)
        )
    stdout_msg('[ INFO ]: Verifying action preconditions...')
    check = check_preconditions()
    if not isinstance(check, int) or check != 0:
        stdout_msg('[ ERROR ]: Preconditions not met!')
        return check
    handle = handle_actions(
        *args, actions=kwargs.get('action', str()).split(','), **kwargs
    )
    if not handle:
        stdout_msg('[ WARNING ]: Issues detected during action execution!')
    return 0 if handle is True else handle

# MISCELLANEOUS

if __name__ == '__main__':
    parse_command_line_arguments()
    clear_screen()
    EXIT_CODE = 1
    try:
        EXIT_CODE = init_asymetric_risk(**AR_DEFAULT)
    finally:
        cleanup()
    stdout_msg('[ DONE ]: Terminating! ({})'.format(EXIT_CODE))
    exit(EXIT_CODE)











# CODE DUMP

#           -b  | --base-currency BTC
#           -q  | --quote-currency USDT
#           -Z  | --ticker-symbol BTC/USDT \\
#           -R  | --risk-tolerance 5
#           -a  | --action "start-watchdog,trade-report" \\
#           -K  | --api-key "yxdLHNgKWzka2HjzR5jZF0ZXTCZaHp2V1X9EgXjKBxLsfKoClFvET1PqIUW9ctAw" \\
#           -S  | --api-secret "oPyuIoqWHBt5pvfCk1YLIslViuH87DJvRTgtOsLylGB58LRsEuHvu4KuZOv0DAv5" \\
#           -k  | --taapi-key "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM2MmRkNThmYzVhOGFkZmVjM2ZhMmEzIiwiaWF0IjoxNjY3NzAxNzg5LCJleHAiOjMzMTcyMTY1Nzg5fQ.33yXXi5RK1oupATjS-RFMLKfD7grZdJ2r7GT4gH-tAE" \\
#           -U  | --api-url "https://testnet.binance.vision/api" \\
#           -u  | --taapi-url "https://api.taapi.io" \\
#           -T  | --strategy "vwap,rsi,macd,adx,ma,ema,price,volume" \\
#           -D  | --debug \\
#           -s  | --silence \\
#           -A  | --analyze-risk \\
#           -t  | --side "auto" \\
#           -i  | --interval "5m" \\
#           -p  | --period 14 \\
#               | --stop-loss \\
#               | --take-profit \\
#               | --trailing-stop \\
#               | --test \\
#               | --price-movement 5 \\
#               | --rsi-top 70 \\
#               | --rsi-bottom 30 \\
#               | --rsi-period 14 \\
#               | --rsi-backtrack 5 \\
#               | --rsi-backtracks 12 \\
#               | --rsi-chart "candles" \\
#               | --rsi-interval "5m" \\
#               | --volume-movement 5 \\
#               | --volume-interval "5m" \\
#               | --ma-period 30 \\
#               | --ma-backtrack 5 \\
#               | --ma-backtracks 12 \\
#               | --ma-chart "candles" \\
#               | --ma-interval "5m" \\
#               | --ema-period 30 \\
#               | --ema-backtrack 5 \\
#               | --ema-backtracks 12 \\
#               | --ema-chart "candles" \\
#               | --ema-interval "5m" \\
#               | --macd-backtrack 5 \\
#               | --macd-backtracks 12 \\
#               | --macd-chart "candles" \\
#               | --macd-fast-period 12 \\
#               | --macd-slow-period 26 \\
#               | --macd-signal-period 9 \\
#               | --macd-interval "5m" \\
#               | --adx-period 14 \\
#               | --adx-backtrack 5 \\
#               | --adx-backtracks 12 \\
#               | --adx-chart "candles" \\
#               | --adx-interval "5m" \\
#               | --vwap-period 14 \\
#               | --vwap-backtrack 5 \\
#               | --vwap-backtracks 12 \\
#               | --vwap-chart "candles" \\
#               | --vwap-interval "5m"


#   market_setup = setup_trading_market()
#   if not market_setup:
#       stdout_msg('[ WARNING ]: Could not set up trading market!')

#from src.ar_market import TradingMarket

# trading_market = TradingMarket(AR_DEFAULT['api-key'], AR_DEFAULT['api-secret'], sync=True, **AR_DEFAULT)


# TODO - DEPRECATED
#   def setup_trading_market():
#       global trading_market
#       trading_market = TradingMarket(
#           AR_DEFAULT['api-key'], AR_DEFAULT['api-secret'], sync=True, **AR_DEFAULT
#       )
#       trading_market.API_URL = AR_DEFAULT['api-url']
#       return trading_market



# trading_bot = TradingBot(TradingMarket(**AR_DEFAULT), **AR_DEFAULT)
# trade = trading_bot.trade(*(vwap, rsi, macd, price, volume), **{
#   'take-profit': 30%,
#   'stop-loss': 10%,
#   'trailing-stop-loss': 10%,
#   'analyze-risk': True,
#   'strategy':
#   'side': buy,
#   'price-movement': 5%,
#   'rsi-top': 70%,
#   'rsi-bottom': 30%,
#   'interval': 5m,
#   'rsi-period': 14,
#   'rsi-backtrack': 5,
#   'rsi-backtracks': 12,
#   'rsi-chart': candles,
#   'rsi-interval': 5m,
#   'volume-movement': 5%,
#   'volume-interval': 5m,
#   'ma-period': 30,
#   'ma-backtrack': 5,
#   'ma-backtracks': 12,
#   'ma-chart': candles,
#   'ma-interval': 5m,
#   'ema-period': 30,
#   'ema-backtrack': 5,
#   'ema-backtracks': 12,
#   'ema-chart': candles,
#   'ema-interval': 5m,
#   'macd-backtrack': 5,
#   'macd-backtracks': 12,
#   'macd-chart': candles,
#   'macd-fast-period': 12,
#   'macd-slow-period': 26,
#   'macd-signal-period': 9,
#   'macd-interval': 5m,
#   'adx-period': 14,
#   'adx-backtrack': 5,
#   'adx-backtracks': 12,
#   'adx-chart': candles,
#   'adx-interval': 5m,
#   'vwap-period': 14,
#   'vwap-backtrack': 5,
#   'vwap-backtracks': 12,
#   'vwap-chart': candles,
#   'vwap-interval': 5m,
# })
# if not trade or isinstance(trade, dict) and trade['error']:
#   print('trade failed')


#   # get balances for all assets & some account information
#   print(client.get_account())

#   # get balance for a specific asset only (BTC)
#   print(client.get_asset_balance(asset='BTC'))

#   # get balances for futures account
#   print(client.futures_account_balance())

#   # get balances for margin account
#   print(client.get_margin_account())

#   # get latest price from Binance API
#   btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
#   # print full output (dictionary)
#   print(btc_price)

#   print(btc_price["price"])

#   def trading_bot(trading_dict):
#       holdings = r.build_holdings()
#       holdings_df = pd.DataFrame()
#       for i in range(len(holdings)):
#           ticker = list(holdings.items())[i][0]
#           holding_df = pd.DataFrame(list(holdings.items())[i][1], index = [i])
#           holding_df['ticker'] = ticker
#           holdings_df = pd.concat([holdings_df, holding_df])
#       holdings_df = holdings_df[['ticker', 'price', 'quantity', 'percent_change','average_buy_price', 'equity', 'equity_change','pe_ratio', 'type', 'name', 'id' ]]

#       for j in range(len(trading_dict)):
#           holding_df = holdings_df[holdings_df.ticker == list(trading_dict.keys())[j]]
#           if holding_df['percent_change'].astype('float32')[0] <= list(trading_dict.values())[j][0]:
#               buy_string = 'Buying ' + str(holding_df['ticker'][0]) + ' at ' + time.ctime()
#               print(buy_string)
#               r.orders.order_buy_market(holding_df['ticker'][0],1,timeInForce= 'gfd')
#           else:
#               print('Nothing to buy')

#           if holding_df['percent_change'].astype('float32')[0] >= list(trading_dict.values())[j][1]:
#               sell_string = 'Buying ' + str(holding_df['ticker'][0]) + ' at ' + time.ctime()
#               print(sell_string)
#               r.orders.order_sell_market(holding_df['ticker'][0],1,timeInForce= 'gfd')
#           else:
#               print('Nothing to sell')v


#   trading_dict = {'KMI': [-0.50, 0.50]}
#   holdings_df = trading_bot(trading_dict)


#   import os

#   from binance.client import Client

#   # init
#   api_key = os.environ.get('binance_api')
#   api_secret = os.environ.get('binance_secret')

#   client = Client(api_key, api_secret)

#   client.API_URL = 'https://testnet.binance.vision/api'

#   # get balances for all assets & some account information
#   print(client.get_account())

#   # get balance for a specific asset only (BTC)
#   print(client.get_asset_balance(asset='BTC'))

#   # get balances for futures account
#   print(client.futures_account_balance())

#   # get balances for margin account
#   print(client.get_margin_account())

#   # get latest price from Binance API
#   btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
#   # print full output (dictionary)
#   print(btc_price)

#   print(btc_price["price"])


#   from time import sleep

#   from binance import ThreadedWebsocketManager
#   btc_price = {'error':False}


#   def btc_trade_history(msg):
#       ''' define how to process incoming WebSocket messages '''
#       if msg['e'] != 'error':
#           print(msg['c'])
#           btc_price['last'] = msg['c']
#           btc_price['bid'] = msg['b']
#           btc_price['last'] = msg['a']
#           btc_price['error'] = False
#       else:
#           btc_price['error'] = True


#   # init and start the WebSocket
#   bsm = ThreadedWebsocketManager()
#   bsm.start()

#   # subscribe to a stream
#   bsm.start_symbol_ticker_socket(callback=btc_trade_history, symbol='BTCUSDT')

#   bsm.start_symbol_ticker_socket(callback=btc_trade_history, symbol='ETHUSDT')

#   # stop websocket
#   bsm.stop()

#   #help(ThreadedWebsocketManager)

#   #valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
#   # get timestamp of earliest date data is available
#   timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1d')
#   print(timestamp)


#   #request historical candle (or klines) data
#   bars = client.get_historical_klines('BTCUSDT', '1d', timestamp, limit=1000)

#   # option 1 - save to file using json method
#   with open('btc_bars.json', 'w') as e:
#           json.dump(bars, e)

#   # option 2 - save as CSV file using the csv writer library
#   with open('btc_bars.csv', 'w', newline='') as f:
#       wr = csv.writer(f)
#       for line in bars:
#           wr.writerow(line)


#   # option 3 - save as CSV file without using a library.
#   with open('btc_bars2.csv', 'w') as d:
#       for line in bars:
#           d.write(f'{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}\n')


#   # delete unwanted data - just keep date, open, high, low, close
#   for line in bars:
#           del line[5:]

#   # option 4 - create a Pandas DataFrame and export to CSV
#   btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
#   btc_df.set_index('date', inplace=True)
#   print(btc_df.head())

#   # export DataFrame to csv
#   btc_df.to_csv('btc_bars3.csv')


#   client.get_open_orders
#   client.futures_get_open_orders




#   import btalib
#   import pandas as pd

#   # load DataFrame
#   btc_df = pd.read_csv('btc_bars3.csv', index_col=0)
#   btc_df.set_index('date', inplace=True)
#   btc_df.index = pd.to_datetime(btc_df.index, unit='ms')

#   # calculate 20 moving average using Pandas
#   btc_df['20sma'] = btc_df.close.rolling(20).mean()
#   print(btc_df.tail(5))


#   # calculate just the last value for the 20 moving average
#   mean = btc_df.close.tail(20).mean()



#   # get the highest closing price in 2020
#   max_val = btc_df.close['2020'].max()


#   ma = btalib.sma(btc_df.close)
#   print(sma.df)



#   # create sma and attach as column to original df
#   btc_df['sma'] = btalib.sma(btc_df.close, period=20).df
#   print(btc_df.tail())


#   rsi = btalib.rsi(btc_df, period=14)


#   print(rsi.df.rsi[-1])



#   macd = btalib.macd(btc_df, pfast=20, pslow=50, psignal=13)


#   # join the rsi and macd calculations as columns in original df
#   btc_df = btc_df.join([rsi.df, macd.df])
#   print(btc_df.tail())


#   buy_order_limit = client.create_test_order(
#           symbol='ETHUSDT',
#           side='BUY',
#           type='LIMIT',
#           timeInForce='GTC',
#           quantity=100,
#           price=200)


#   buy_order = client.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)



#   import os

#   from binance.client import Client
#   from binance.enums import *
#   from binance.exceptions import BinanceAPIException, BinanceOrderException

#   # init
#   api_key = os.environ.get('binance_api')
#   api_secret = os.environ.get('binance_secret')

#   client = Client(api_key, api_secret)

#   # create a real order if the test orders did not raise an exception

#   try:
#           buy_limit = client.create_order(
#                       symbol='ETHUSDT',
#                       side='BUY',
#                       type='LIMIT',
#                       timeInForce='GTC',
#                       quantity=100,
#                       price=200)

#   except BinanceAPIException as e:
#           # error handling goes here
#               print(e)
#   except BinanceOrderException as e:
#           # error handling goes here
#               print(e)




#       # cancel previous orders
#           cancel = client.cancel_order(symbol='ETHUSDT', orderId=buy_limit['orderId'])
#       # same order but with helper function
#           buy_limit = client.order_limit_buy(symbol='ETHUSDT', quantity=100, price=200)
#               # market order using a helper function
#                   market_order = client.order_market_sell(symbol='ETHUSDT', quantity=100)

#   buy_order = client.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)
#   buy_order = client.create_test_order(symbol='ETHUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=100)


#   try:
#           order = client.create_oco_order(
#                       symbol='ETHUSDT',
#                       side='SELL',
#                       quantity=100,
#                       price=250,
#                       stopPrice=150,
#                       stopLimitPrice=150,
#                       stopLimitTimeInForce='GTC')

#   except BinanceAPIException as e:
#           # error handling goes here
#               print(e)
#   except BinanceOrderException as e:
#           # error handling goes here
#               print(e)

#   # use exchange info to confirm order types
#   info = client.get_symbol_info('ETHUSDT')
#   print(info['orderTypes'])


#   def topup_bnb(min_balance: float, topup: float):
#   ''' Top up BNB balance if it drops below minimum specified balance '''
#       bnb_balance = client.get_asset_balance(asset='BNB')
#       bnb_balance = float(bnb_balance['free'])
#       if bnb_balance < min_balance:
#           qty = round(topup - bnb_balance, 5)
#           print(qty)
#           order = client.order_market_buy(symbol='BNBUSDT', quantity=qty)
#           return order
#       return False

#   min_balance = 1.0
#   topup = 2.5
#   order = topup_bnb(min_balance, topup)




#   import os
#   from time import sleep

#   from binance.client import Client
#   from binance import ThreadedWebsocketManager

#   # init
#   api_key = os.environ.get('binance_api')
#   api_secret = os.environ.get('binance_secret')
#   client = Client(api_key, api_secret)
#   price = {'BTCUSDT': None, 'error': False}

#   def btc_pairs_trade(msg):
#       ''' define how to process incoming WebSocket messages '''
#       if msg['e'] != 'error':
#           price['BTCUSDT'] = float(msg['c'])
#       else:
#           price['error'] = True

#   bsm = ThreadedWebsocketManager()
#   bsm.start()
#   bsm.start_symbol_ticker_socket(symbol='BTCUSDT', callback=btc_pairs_trade)


#   while not price['BTCUSDT']:
#       # wait for WebSocket to start streaming data
#       sleep(0.1)

#   while True:
#       # error check to make sure WebSocket is working
#       if price['error']:
#           # stop and restart socket
#           bsm.stop()
#           sleep(2)
#           bsm.start()
#           price['error'] = False

#       else:
#           if price['BTCUSDT'] > 10000:
#               try:
#                   order = client.order_market_buy(symbol='ETHUSDT', quantity=100)
#                   break
#               except Exception as e:
#                   print(e)

#       sleep(0.1)


#   bsm.stop()




#   import os
#   from time import sleep

#   import pandas as pd
#   from binance import ThreadedWebsocketManager
#   from binance.client import Client

#   # init
#   api_key = os.environ.get('binance_api')
#   api_secret = os.environ.get('binance_secret')
#   client = Client(api_key, api_secret)
#   price = {'BTCUSDT': pd.DataFrame(columns=['date', 'price']), 'error': False}



#   def btc_pairs_trade(msg):
#       ''' define how to process incoming WebSocket messages '''
#       if msg['e'] != 'error':
#           price['BTCUSDT'].loc[len(price['BTCUSDT'])] = [pd.Timestamp.now(), float(msg['c'])]
#       else:
#           price['error'] = True


#   # init and start the WebSocket
#   bsm = ThreadedWebsocketManager()
#   bsm.start()
#   bsm.start_symbol_ticker_socket(symbol='BTCUSDT', callback=btc_pairs_trade)


#   ## main
#   while len(price['BTCUSDT']) == 0:
#       # wait for WebSocket to start streaming data
#       sleep(0.1)
#       sleep(300)


#   while True:
#       # error check to make sure WebSocket is working
#       if price['error']:
#           # stop and restart socket
#           bsm.stop()
#           sleep(2)
#           bsm.start()
#           price['error'] = False
#       else:
#           df = price['BTCUSDT']
#           start_time = df.date.iloc[-1] - pd.Timedelta(minutes=5)
#           df = df.loc[df.date >= start_time]
#           max_price = df.price.max()
#           min_price = df.price.min()


#   if df.price.iloc[-1] < max_price * 0.95:
#       try:
#           order = client.futures_create_order(symbol='ETHUSDT', side='SELL', type='MARKET', quantity=100)
#           break
#       except Exception as e:
#           print(e)
#   elif df.price.iloc[-1] > min_price * 1.05:
#       try:
#           order = client.futures_create_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)
#           break
#       except Exception as e:
#           print(e)

#   sleep(0.1)


#   # properly stop and terminate WebSocket
#   bsm.stop()


#   |
#   |  get_account(self, **params)
#   |      Get current account information.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#account-information-user_data
#   |
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "makerCommission": 15,
#   |              "takerCommission": 15,
#   |              "buyerCommission": 0,
#   |              "sellerCommission": 0,
#   |              "canTrade": true,
#   |              "canWithdraw": true,
#   |              "canDeposit": true,
#   |              "balances": [
#   |                  {
#   |                      "asset": "BTC",
#   |                      "free": "4723846.89208129",
#   |                      "locked": "0.00000000"
#   |                  },
#   |                  {
#   |                      "asset": "LTC",
#   |                      "free": "4763368.68006011",
#   |                      "locked": "0.00000000"
#   |                  }
#   |              ]
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException



#   |  get_account_api_permissions(self, **params)
#   |      Fetch api key permissions.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#get-api-key-permission-user_data
#   |
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |             "ipRestrict": false,
#   |             "createTime": 1623840271000,
#   |             "enableWithdrawals": false,   // This option allows you to withdraw via API. You must apply the IP Access Restriction filter in order to enable withdrawals
#   |             "enableInternalTransfer": true,  // This option authorizes this key to transfer funds between your master account and your sub account instantly
#   |             "permitsUniversalTransfer": true,  // Authorizes this key to be used for a dedicated universal transfer API to transfer multiple supported currencies. Each business's own transfer API rights are not affected by this authorization
#   |             "enableVanillaOptions": false,  //  Authorizes this key to Vanilla options trading
#   |             "enableReading": true,
#   |             "enableFutures": false,  //  API Key created before your futures account opened does not support futures API service
#   |             "enableMargin": false,   //  This option can be adjusted after the Cross Margin account transfer is completed
#   |             "enableSpotAndMarginTrading": false, // Spot and margin trading
#   |             "tradingAuthorityExpirationTime": 1628985600000  // Expiration time for spot and margin trading permission
#   |          }


#   |
#   |  get_account_api_trading_status(self, **params)
#   |      Fetch account api trading status detail.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#account-api-trading-status-sapi-user_data
#   |
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "data": {          // API trading status detail
#   |                  "isLocked": false,   // API trading function is locked or not
#   |                  "plannedRecoverTime": 0,  // If API trading function is locked, this is the planned recover time
#   |                  "triggerCondition": {
#   |                          "GCR": 150,  // Number of GTC orders
#   |                          "IFER": 150, // Number of FOK/IOC orders
#   |                          "UFR": 300   // Number of orders
#   |                  },
#   |                  "indicators": {  // The indicators updated every 30 seconds
#   |                       "BTCUSDT": [  // The symbol
#   |                          {
#   |                              "i": "UFR",  // Unfilled Ratio (UFR)
#   |                              "c": 20,     // Count of all orders
#   |                              "v": 0.05,   // Current UFR value
#   |                              "t": 0.995   // Trigger UFR value
#   |                          },
#   |                          {
#   |                              "i": "IFER", // IOC/FOK Expiration Ratio (IFER)
#   |                              "c": 20,     // Count of FOK/IOC orders
#   |                              "v": 0.99,   // Current IFER value
#   |                              "t": 0.99    // Trigger IFER value
#   |                          },
#   |                          {
#   |                              "i": "GCR",  // GTC Cancellation Ratio (GCR)
#   |                              "c": 20,     // Count of GTC orders
#   |                              "v": 0.99,   // Current GCR value
#   |                              "t": 0.99    // Trigger GCR value
#   |                          }
#   |                      ],
#   |                      "ETHUSDT": [
#   |                          {
#   |                              "i": "UFR",
#   |                              "c": 20,
#   |                              "v": 0.05,
#   |                              "t": 0.995
#   |                          },
#   |                          {
#   |                              "i": "IFER",
#   |                              "c": 20,
#   |                              "v": 0.99,
#   |                              "t": 0.99
#   |                          },
#   |                          {
#   |                              "c": 20,
#   |                              "v": 0.99,
#   |                              "t": 0.99
#   |                          }
#   |                      ]
#   |                  },
#   |                  "updateTime": 1547630471725
#   |              }
#   |          }


#   |  get_account_snapshot(self, **params)
#   |      Get daily account snapshot of specific type.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#daily-account-snapshot-user_data
#   |
#   |      :param type: required. Valid values are SPOT/MARGIN/FUTURES.
#   |      :type type: string
#   |      :param startTime: optional
#   |      :type startTime: int
#   |      :param endTime: optional
#   |      :type endTime: int
#   |      :param limit: optional
#   |      :type limit: int
#   |      :param recvWindow: optional
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |             "code":200, // 200 for success; others are error codes
#   |             "msg":"", // error message
#   |             "snapshotVos":[
#   |                {
#   |                   "data":{
#   |                      "balances":[
#   |                         {
#   |                            "asset":"BTC",
#   |                            "free":"0.09905021",
#   |                            "locked":"0.00000000"
#   |                         },
#   |                         {
#   |                            "asset":"USDT",
#   |                            "free":"1.89109409",
#   |                            "locked":"0.00000000"
#   |                         }
#   |                      ],
#   |                      "totalAssetOfBtc":"0.09942700"
#   |                   },
#   |                   "type":"spot",
#   |                   "updateTime":1576281599000
#   |                }
#   |             ]
#   |          }
#   |


#   |  get_account_status(self, **params)
#   |      Get account status detail.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#account-status-sapi-user_data
#   |
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "data": "Normal"
#   |          }
#   |

#   |  get_all_coins_info(self, **params)
#   |      Get information of coins (available for deposit and withdraw) for user.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data
#   |
#   |      :param recvWindow: optional
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "coin": "BTC",
#   |              "depositAllEnable": true,
#   |              "withdrawAllEnable": true,
#   |              "name": "Bitcoin",
#   |              "free": "0",
#   |              "locked": "0",
#   |              "freeze": "0",
#   |              "withdrawing": "0",
#   |              "ipoing": "0",
#   |              "ipoable": "0",
#   |              "storage": "0",
#   |              "isLegalMoney": false,
#   |              "trading": true,
#   |              "networkList": [
#   |                  {
#   |                      "network": "BNB",
#   |                      "coin": "BTC",
#   |                      "withdrawIntegerMultiple": "0.00000001",
#   |                      "isDefault": false,
#   |                      "depositEnable": true,
#   |                      "withdrawEnable": true,
#   |                      "depositDesc": "",
#   |                      "withdrawDesc": "",
#   |                      "specialTips": "Both a MEMO and an Address are required to successfully deposit your BEP2-BTCB tokens to Binance.",
#   |                      "name": "BEP2",
#   |                      "resetAddressStatus": false,
#   |                      "addressRegex": "^(bnb1)[0-9a-z]{38}$",
#   |                      "memoRegex": "^[0-9A-Za-z-_]{1,120}$",
#   |                      "withdrawFee": "0.0000026",
#   |                      "withdrawMin": "0.0000052",
#   |                      "withdrawMax": "0",
#   |                      "minConfirm": 1,
#   |                      "unLockConfirm": 0
#   |                  },
#   |                  {
#   |                      "network": "BTC",
#   |                      "coin": "BTC",
#   |                      "withdrawIntegerMultiple": "0.00000001",
#   |                      "isDefault": true,
#   |                      "depositEnable": true,
#   |                      "withdrawEnable": true,
#   |                      "depositDesc": "",
#   |                      "withdrawDesc": "",
#   |                      "specialTips": "",
#   |                      "name": "BTC",
#   |                      "resetAddressStatus": false,
#   |                      "addressRegex": "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^(bc1)[0-9A-Za-z]{39,59}$",

#   |                      "memoRegex": "",
#   |                      "withdrawFee": "0.0005",
#   |                      "withdrawMin": "0.001",
#   |                      "withdrawMax": "0",
#   |                      "minConfirm": 1,
#   |                      "unLockConfirm": 2
#   |                  }
#   |              ]
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException

#   |  withdraw(self, **params)
#   |      Submit a withdraw request.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#withdraw-sapi
#   |
#   |      Assumptions:
#   |
#   |      - You must have Withdraw permissions enabled on your API key
#   |      - You must have withdrawn to the address specified through the website and approved the transaction via email
#   |
#   |      :param coin: required
#   |      :type coin: str
#   |      :param withdrawOrderId: optional - client id for withdraw
#   |      :type withdrawOrderId: str
#   |      :param network: optional
#   |      :type network: str
#   |      :param address: optional
#   |      :type address: str
#   |      :type addressTag: optional - Secondary address identifier for coins like XRP,XMR etc.
#   |      :param amount: required
#   |      :type amount: decimal
#   |      :param transactionFeeFlag: required - When making internal transfer, true for returning the fee to the destination account; false for returning the fee back to the departure account. Default false.
#   |      :type transactionFeeFlag: bool
#   |      :param name: optional - Description of the address, default asset value passed will be used
#   |      :type name: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "id":"7213fea8e94b4a5593d507237e5a555b"
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException


#   |  order_market_buy(self, **params)
#   |      Send in a new market buy order
#   |
#   |      :param symbol: required
#   |      :type symbol: str
#   |      :param quantity: required
#   |      :type quantity: decimal
#   |      :param quoteOrderQty: the amount the user wants to spend of the quote asset
#   |      :type quoteOrderQty: decimal
#   |      :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
#   |      :type newClientOrderId: str
#   |      :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
#   |      :type newOrderRespType: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      See order endpoint for full response options
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSym
#   bolException
#   |
#   |  order_market_sell(self, **params)
#   |      Send in a new market sell order
#   |
#   |      :param symbol: required
#   |      :type symbol: str
#   |      :param quantity: required
#   |      :type quantity: decimal
#   |      :param quoteOrderQty: the amount the user wants to receive of the quote asset
#   |      :type quoteOrderQty: decimal
#   |      :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
#   |      :type newClientOrderId: str
#   |      :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
#   |      :type newOrderRespType: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      See order endpoint for full response options
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSym
#   bolException


#   |
#   |  get_trade_fee(self, **params)
#   |      Get trade fee.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#trade-fee-sapi-user_data
#   |
#   |      :param symbol: optional
#   |      :type symbol: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          [
#   |              {
#   |                  "symbol": "ADABNB",
#   |                  "makerCommission": "0.001",
#   |                  "takerCommission": "0.001"
#   |              },
#   |              {
#   |                  "symbol": "BNBBTC",
#   |                  "makerCommission": "0.001",
#   |                  "takerCommission": "0.001"
#   |              }
#   |          ]
#   |


#   |  get_ticker(self, **params)
#   |      24 hour price change statistics.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics
#   |
#   |      :param symbol:
#   |      :type symbol: str
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "priceChange": "-94.99999800",
#   |              "priceChangePercent": "-95.960",
#   |              "weightedAvgPrice": "0.29628482",
#   |              "prevClosePrice": "0.10002000",
#   |              "lastPrice": "4.00000200",
#   |              "bidPrice": "4.00000000",
#   |              "askPrice": "4.00000200",
#   |              "openPrice": "99.00000000",
#   |              "highPrice": "100.00000000",
#   |              "lowPrice": "0.10000000",
#   |              "volume": "8913.30000000",
#   |              "openTime": 1499783499040,
#   |              "closeTime": 1499869899040,
#   |              "fristId": 28385,   # First tradeId
#   |              "lastId": 28460,    # Last tradeId
#   |              "count": 76         # Trade count
#   |          }
#   |
#   |      OR
#   |
#   |      .. code-block:: python
#   |
#   |          [
#   |              {
#   |                  "priceChange": "-94.99999800",
#   |                  "priceChangePercent": "-95.960",
#   |                  "weightedAvgPrice": "0.29628482",
#   |                  "prevClosePrice": "0.10002000",
#   |                  "lastPrice": "4.00000200",
#   |                  "bidPrice": "4.00000000",
#   |                  "askPrice": "4.00000200",
#   |                  "openPrice": "99.00000000",
#   |                  "highPrice": "100.00000000",
#   |                  "lowPrice": "0.10000000",
#   |                  "volume": "8913.30000000",
#   |                  "openTime": 1499783499040,
#   |                  "closeTime": 1499869899040,
#   |                  "fristId": 28385,   # First tradeId
#   |                  "lastId": 28460,    # Last tradeId
#   |                  "count": 76         # Trade count
#   |              }
#   |          ]
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException




#   |
#   |  get_system_status(self)
#   |      Get system status detail.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#system-status-sapi-system
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "status": 0,        # 0: normal，1：system maintenance
#   |              "msg": "normal"     # normal or System maintenance.
#   |          }
#   |
#   |      :raises: BinanceAPIException


#   |
#   |  get_symbol_ticker(self, **params)
#   |      Latest price for a symbol or symbols.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker
#   |
#   |      :param symbol:
#   |      :type symbol: str
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "symbol": "LTCBTC",
#   |              "price": "4.00000200"
#   |          }
#   |
#   |      OR
#   |
#   |      .. code-block:: python
#   |
#   |          [
#   |              {
#   |                  "symbol": "LTCBTC",
#   |                  "price": "4.00000200"
#   |              },
#   |              {
#   |                  "symbol": "ETHBTC",
#   |                  "price": "0.07946600"
#   |              }
#   |          ]
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException




#   |
#   |  get_symbol_info(self, symbol) -> Optional[Dict]
#   |      Return information about a symbol
#   |
#   |      :param symbol: required e.g BNBBTC
#   |      :type symbol: str
#   |
#   |      :returns: Dict if found, None if not
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "symbol": "ETHBTC",
#   |              "status": "TRADING",
#   |              "baseAsset": "ETH",
#   |              "baseAssetPrecision": 8,
#   |              "quoteAsset": "BTC",
#   |              "quotePrecision": 8,
#   |              "orderTypes": ["LIMIT", "MARKET"],
#   |              "icebergAllowed": false,
#   |              "filters": [
#   |                  {
#   |                      "filterType": "PRICE_FILTER",
#   |                      "minPrice": "0.00000100",
#   |                      "maxPrice": "100000.00000000",
#   |                      "tickSize": "0.00000100"
#   |                  }, {
#   |                      "filterType": "LOT_SIZE",
#   |                      "minQty": "0.00100000",
#   |                      "maxQty": "100000.00000000",
#   |                      "stepSize": "0.00100000"
#   |                  }, {
#   |                      "filterType": "MIN_NOTIONAL",
#   |                      "minNotional": "0.00100000"
#   |                  }
#   |              ]
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException


#   |  get_recent_trades(self, **params) -> Dict
#   |      Get recent trades (up to last 500).
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#recent-trades-list
#   |
#   |      :param symbol: required
#   |      :type symbol: str
#   |      :param limit:  Default 500; max 1000.
#   |      :type limit: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          [
#   |              {
#   |                  "id": 28457,
#   |                  "price": "4.00000100",
#   |                  "qty": "12.00000000",
#   |                  "time": 1499865549590,
#   |                  "isBuyerMaker": true,
#   |                  "isBestMatch": true
#   |              }
#   |          ]
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException
#   |
#   |  get_server_time(self) -> Dict
#   |      Test connectivity to the Rest API and get the current server time.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#check-server-time
#   |
#   |      :returns: Current server time
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "serverTime": 1499827319559
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException





#   |  get_orderbook_tickers(self) -> Dict
#   |      Best price/qty on the order book for all symbols.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker
#   |
#   |      :param symbol: optional
#   |      :type symbol: str
#   |
#   |      :returns: List of order book market entries
#   |
#   |      .. code-block:: python
#   |
#   |          [
#   |              {
#   |                  "symbol": "LTCBTC",
#   |                  "bidPrice": "4.00000000",
#   |                  "bidQty": "431.00000000",
#   |                  "askPrice": "4.00000200",
#   |                  "askQty": "9.00000000"
#   |              },
#   |              {
#   |                  "symbol": "ETHBTC",
#   |                  "bidPrice": "0.07946700",
#   |                  "bidQty": "9.00000000",
#   |                  "askPrice": "100000.00000000",
#   |                  "askQty": "1000.00000000"
#   |              }
#   |          ]
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException


#   |  get_deposit_address(self, coin: str, network: Optional[str] = None, **params)
#   |      Fetch a deposit address for a symbol
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#deposit-address-supporting-network-user_data
#   |
#   |      :param coin: required
#   |      :type coin: str
#   |      :param network: optional
#   |      :type network: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "address": "1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv",
#   |              "coin": "BTC",
#   |              "tag": "",
#   |              "url": "https://btc.com/1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv"
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException
#   |

#   |  get_avg_price(self, **params)
#   |      Current average price for a symbol.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#current-average-price
#   |
#   |      :param symbol:
#   |      :type symbol: str
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "mins": 5,
#   |              "price": "9.35751834"
#   |          }
#   |


#   |  create_margin_oco_order(self, **params)
#   |      Post a new OCO trade for margin account.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-oco-trade
#   |
#   |
#   |      :param symbol: required
#   |      :type symbol: str
#   |      :param isIsolated: for isolated margin or not, "TRUE", "FALSE"，default "FALSE"
#   |      :type symbol: str
#   |      :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
#   |      :type listClientOrderId: str
#   |      :param side: required
#   |      :type side: str
#   |      :param quantity: required
#   |      :type quantity: decimal
#   |      :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
#   |      :type limitClientOrderId: str
#   |      :param price: required
#   |      :type price: str
#   |      :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
#   |      :type limitIcebergQty: decimal
#   |      :param stopClientOrderId: A unique Id for the stop loss/stop loss limit leg. Automatically generated if not sent.
#   |      :type stopClientOrderId: str
#   |      :param stopPrice: required
#   |      :type stopPrice: str
#   |      :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
#   |      :type stopLimitPrice: str
#   |      :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
#   |      :type stopIcebergQty: decimal
#   |      :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
#   |      :type stopLimitTimeInForce: str
#   |      :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
#   |      :type newOrderRespType: str
#   |      :param sideEffectType: NO_SIDE_EFFECT, MARGIN_BUY, AUTO_REPAY; default NO_SIDE_EFFECT.
#   |      :type sideEffectType: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "orderListId": 0,
#   |              "contingencyType": "OCO",
#   |              "listStatusType": "EXEC_STARTED",
#   |              "listOrderStatus": "EXECUTING",
#   |              "listClientOrderId": "JYVpp3F0f5CAG15DhtrqLp",
#   |              "transactionTime": 1563417480525,
#   |              "symbol": "LTCBTC",
#   |              "marginBuyBorrowAmount": "5",       // will not return if no margin trade happens
#   |              "marginBuyBorrowAsset": "BTC",    // will not return if no margin trade happens
#   |              "isIsolated": false,       // if isolated margin
#   |              "orders": [
#   |                  {
#   |                      "symbol": "LTCBTC",
#   |                      "orderId": 2,
#   |                      "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos"
#   |                  },
#   |                  {
#   |                      "symbol": "LTCBTC",
#   |                      "orderId": 3,
#   |                      "clientOrderId": "xTXKaGYd4bluPVp78IVRvl"
#   |                  }
#   |              ],
#   |              "orderReports": [
#   |                  {
#   |                      "symbol": "LTCBTC",
#   |                      "orderId": 2,
#   |                      "orderListId": 0,
#   |                      "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos",
#   |                      "transactTime": 1563417480525,
#   |                      "price": "0.000000",
#   |                      "origQty": "0.624363",
#   |                      "executedQty": "0.000000",
#   |                      "cummulativeQuoteQty": "0.000000",
#   |                      "status": "NEW",
#   |                      "timeInForce": "GTC",
#   |                      "type": "STOP_LOSS",
#   |                      "side": "BUY",
#   |                      "stopPrice": "0.960664"
#   |                  },
#   |                  {
#   |                      "symbol": "LTCBTC",
#   |                      "orderId": 3,
#   |                      "orderListId": 0,
#   |                      "clientOrderId": "xTXKaGYd4bluPVp78IVRvl",
#   |                      "transactTime": 1563417480525,
#   |                      "price": "0.036435",
#   |                      "origQty": "0.624363",
#   |                      "executedQty": "0.000000",
#   |                      "cummulativeQuoteQty": "0.000000",
#   |                      "status": "NEW",
#   |                      "timeInForce": "GTC",
#   |                      "type": "LIMIT_MAKER",
#   |                      "side": "BUY"
#   |                  }
#   |              ]
#   |          }


#   |  create_margin_order(self, **params)
#   |      Post a new order for margin account.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-order-trade
#   |
#   |      :param symbol: required
#   |      :type symbol: str
#   |      :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
#   |      :type isIsolated: str
#   |      :param side: required
#   |      :type side: str
#   |      :param type: required
#   |      :type type: str
#   |      :param quantity: required
#   |      :type quantity: decimal
#   |      :param price: required
#   |      :type price: str
#   |      :param stopPrice: Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
#   |      :type stopPrice: str
#   |      :param timeInForce: required if limit order GTC,IOC,FOK
#   |      :type timeInForce: str
#   |      :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
#   |      :type newClientOrderId: str
#   |      :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
#   |      :type icebergQty: str
#   |      :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default to
#   |          FULL, all other orders default to ACK.
#   |      :type newOrderRespType: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      Response ACK:
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "symbol": "BTCUSDT",
#   |              "orderId": 28,
#   |              "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   |              "transactTime": 1507725176595
#   |          }
#   |
#   |      Response RESULT:
#   |      Response RESULT:
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "symbol": "BTCUSDT",
#   |              "orderId": 28,
#   |              "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   |              "transactTime": 1507725176595,
#   |              "price": "1.00000000",
#   |              "origQty": "10.00000000",
#   |              "executedQty": "10.00000000",
#   |              "cummulativeQuoteQty": "10.00000000",
#   |              "status": "FILLED",
#   |              "timeInForce": "GTC",
#   |              "type": "MARKET",
#   |              "side": "SELL"
#   |          }
#   |
#   |      Response FULL:
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "symbol": "BTCUSDT",
#   |              "orderId": 28,
#   |              "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   |              "transactTime": 1507725176595,
#   |              "price": "1.00000000",
#   |              "origQty": "10.00000000",
#   |              "executedQty": "10.00000000",
#   |              "cummulativeQuoteQty": "10.00000000",
#   |              "status": "FILLED",
#   |              "timeInForce": "GTC",
#   |              "type": "MARKET",
#   |              "side": "SELL",
#   |              "fills": [
#   |                  {
#   |                      "price": "4000.00000000",
#   |                      "qty": "1.00000000",
#   |                      "commission": "4.00000000",
#   |                      "commissionAsset": "USDT"
#   |                  },
#   |                  {
#   |                      "price": "3999.00000000",
#   |                      "qty": "5.00000000",
#   |                      "commission": "19.99500000",
#   |                      "commissionAsset": "USDT"
#   |                  },
#   |                  {
#   |                      "price": "3998.00000000",
#   |                      "qty": "2.00000000",
#   |                      "commission": "7.99600000",
#   |                      "commissionAsset": "USDT"
#   |                  },
#   |                  {
#   |                      "price": "3997.00000000",
#   |                      "qty": "1.00000000",
#   |                      "commission": "3.99700000",
#   |                      "commissionAsset": "USDT"
#   |                  },
#   |                  {
#   |                      "price": "3995.00000000",
#   |                      "qty": "1.00000000",
#   |                      "commission": "3.99500000",
#   |                      "commissionAsset": "USDT"
#   |                  }
#   |              ]
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
#   |          BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
#   |          BinanceOrderInactiveSymbolException




#   |  create_oco_order(self, **params)
#   |      Send in a new OCO order
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#new-oco-trade
#   |
#   |      :param symbol: required
#   |      :type symbol: str
#   |      :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
#   |      :type listClientOrderId: str
#   |      :param side: required
#   |      :type side: str
#   |      :param quantity: required
#   |      :type quantity: decimal
#   |      :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
#   |      :type limitClientOrderId: str
#   |      :param price: required
#   |      :type price: str
#   |      :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
#   |      :type limitIcebergQty: decimal
#   |      :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
#   |      :type stopClientOrderId: str
#   |      :param stopPrice: required
#   |      :type stopPrice: str
#   |      :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
#   |      :type stopLimitPrice: str
#   |      :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
#   |      :type stopIcebergQty: decimal
#   |      :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
#   |      :type stopLimitTimeInForce: str
#   |      :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
#   |      :type newOrderRespType: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      Response ACK:
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |          }
#   |
#   |      Response RESULT:
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |          }
#   |
#   |      Response FULL:
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException


#   |  create_order(self, **params)
#   |      Send in a new order
#   |
#   |      Any order with an icebergQty MUST have timeInForce set to GTC.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#new-order-trade
#   |
#   |      :param symbol: required
#   |      :type symbol: str
#   |      :param side: required
#   |      :type side: str
#   |      :param type: required
#   |      :type type: str
#   |      :param timeInForce: required if limit order
#   |      :type timeInForce: str
#   |      :param quantity: required
#   |      :type quantity: decimal
#   |      :param quoteOrderQty: amount the user wants to spend (when buying) or receive (when selling)
#   |          of the quote asset, applicable to MARKET orders
#   |      :type quoteOrderQty: decimal
#   |      :param price: required
#   |      :type price: str
#   |      :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
#   |      :type newClientOrderId: str
#   |      :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
#   |      :type icebergQty: decimal
#   |      :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
#   |      :type newOrderRespType: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      Response ACK:
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "symbol":"LTCBTC",
#   |              "orderId": 1,
#   |              "clientOrderId": "myOrder1" # Will be newClientOrderId
#   |              "transactTime": 1499827319559
#   |          }
#   |
#   |      Response RESULT:
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "symbol": "BTCUSDT",
#   |              "orderId": 28,
#   |              "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   |              "transactTime": 1507725176595,
#   |              "price": "0.00000000",
#   |              "origQty": "10.00000000",
#   |              "executedQty": "10.00000000",
#   |              "cummulativeQuoteQty": "10.00000000",
#   |              "status": "FILLED",
#   |              "timeInForce": "GTC",
#   |              "type": "MARKET",
#   |              "side": "SELL"
#   |          }
#   |
#   |      Response FULL:
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "symbol": "BTCUSDT",
#   |              "orderId": 28,
#   |              "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   |              "transactTime": 1507725176595,
#   |              "price": "0.00000000",
#   |              "origQty": "10.00000000",
#   |              "executedQty": "10.00000000",
#   |              "cummulativeQuoteQty": "10.00000000",
#   |              "status": "FILLED",
#   |              "timeInForce": "GTC",
#   |              "type": "MARKET",
#   |              "side": "SELL",
#   |              "fills": [
#   |                  {
#   |                      "price": "4000.00000000",
#   |                      "qty": "1.00000000",
#   |                      "commission": "4.00000000",
#   |                      "commissionAsset": "USDT"
#   |                  },
#   |                  {
#   |                      "price": "3999.00000000",
#   |                      "qty": "5.00000000",
#   |                      "commission": "19.99500000",
#   |                      "commissionAsset": "USDT"
#   |                  },
#   |                  {
#   |                      "price": "3998.00000000",
#   |                      "qty": "2.00000000",
#   |                      "commission": "7.99600000",
#   |                      "commissionAsset": "USDT"
#   |                  },
#   |                  {
#   |                      "price": "3997.00000000",
#   |                      "qty": "1.00000000",
#   |                      "commission": "3.99700000",
#   |                      "commissionAsset": "USDT"
#   |                  },
#   |                  {
#   |                      "price": "3995.00000000",
#   |                      "qty": "1.00000000",
#   |                      "commission": "3.99500000",
#   |                      "commissionAsset": "USDT"
#   |                  }
#   |              ]
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException


#   |  get_all_orders(self, **params)
#   |      Get all account orders; active, canceled, or filled.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#all-orders-user_data
#   |
#   |      :param symbol: required
#   |      :type symbol: str
#   |      :param orderId: The unique order id
#   |      :type orderId: int
#   |      :param startTime: optional
#   |      :type startTime: int
#   |      :param endTime: optional
#   |      :type endTime: int
#   |      :param limit: Default 500; max 1000.
#   |      :type limit: int
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          [
#   |              {
#   |                  "symbol": "LTCBTC",
#   |                  "orderId": 1,
#   |                  "clientOrderId": "myOrder1",
#   |                  "price": "0.1",
#   |                  "origQty": "1.0",
#   |                  "executedQty": "0.0",
#   |                  "status": "NEW",
#   |                  "timeInForce": "GTC",
#   |                  "type": "LIMIT",
#   |                  "side": "BUY",
#   |                  "stopPrice": "0.0",
#   |                  "icebergQty": "0.0",
#   |                  "time": 1499827319559
#   |              }
#   |          ]
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException
#   |


#   |  get_all_tickers(self) -> List[Dict[str, str]]
#   |      Latest price for all symbols.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker
#   |
#   |      :returns: List of market tickers
#   |
#   |      .. code-block:: python
#   |
#   |          [
#   |              {
#   |                  "symbol": "LTCBTC",
#   |                  "price": "4.00000200"
#   |              },
#   |              {
#   |                  "symbol": "ETHBTC",
#   |                  "price": "0.07946600"
#   |              }
#   |          ]
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException
#   |


#   |  get_asset_balance(self, asset, **params)
#   |      Get current asset balance.
#   |
#   |      :param asset: required
#   |      :type asset: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: dictionary or None if not found
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "asset": "BTC",
#   |              "free": "4723846.89208129",
#   |              "locked": "0.00000000"
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException


#   |  get_asset_details(self, **params)
#   |      Fetch details on assets.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#asset-detail-sapi-user_data
#   |
#   |      :param asset: optional
#   |      :type asset: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |                  "CTR": {
#   |                      "minWithdrawAmount": "70.00000000", //min withdraw amount
#   |                      "depositStatus": false,//deposit status (false if ALL of networks' are false)
#   |                      "withdrawFee": 35, // withdraw fee
#   |                      "withdrawStatus": true, //withdraw status (false if ALL of networks' are false)
#   |                      "depositTip": "Delisted, Deposit Suspended" //reason
#   |                  },
#   |                  "SKY": {
#   |                      "minWithdrawAmount": "0.02000000",
#   |                      "depositStatus": true,
#   |                      "withdrawFee": 0.01,
#   |                      "withdrawStatus": true
#   |                  }
#   |          }


#   |  get_asset_dividend_history(self, **params)
#   |      Query asset dividend record.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#asset-dividend-record-user_data
#   |
#   |      :param asset: optional
#   |      :type asset: str
#   |      :param startTime: optional
#   |      :type startTime: long
#   |      :param endTime: optional
#   |      :type endTime: long
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      .. code:: python
#   |
#   |          result = client.get_asset_dividend_history()
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "rows":[
#   |                  {
#   |                      "amount":"10.00000000",
#   |                      "asset":"BHFT",
#   |                      "divTime":1563189166000,
#   |                      "enInfo":"BHFT distribution",
#   |                      "tranId":2968885920
#   |                  },
#   |                  {
#   |                      "amount":"10.00000000",
#   |                      "asset":"BHFT",
#   |                      "divTime":1563189165000,
#   |                      "enInfo":"BHFT distribution",
#   |                      "tranId":2968885920
#   |                  }
#   |              ],
#   |              "total":2
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException


#   |  get_deposit_history(self, **params)
#   |      Fetch deposit history.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#deposit-history-supporting-network-user_data
#   |
#   |      :param coin: optional
#   |      :type coin: str
#   |      :type status: optional - 0(0:pending,1:success) optional
#   |      :type status: int
#   |      :param startTime: optional
#   |      :type startTime: long
#   |      :param endTime: optional
#   |      :type endTime: long
#   |      :param offset: optional - default:0
#   |      :type offset: long
#   |      :param limit: optional
#   |      :type limit: long
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          [
#   |              {
#   |                  "amount":"0.00999800",
#   |                  "coin":"PAXG",
#   |                  "network":"ETH",
#   |                  "status":1,
#   |                  "address":"0x788cabe9236ce061e5a892e1a59395a81fc8d62c",
#   |                  "addressTag":"",
#   |                  "txId":"0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3",
#   |                  "insertTime":1599621997000,
#   |                  "transferType":0,
#   |                  "confirmTimes":"12/12"
#   |              },
#   |              {
#   |                  "amount":"0.50000000",
#   |                  "coin":"IOTA",
#   |                  "network":"IOTA",
#   |                  "status":1,
#   |                  "address":"SIZ9VLMHWATXKV99LH99CIGFJFUMLEHGWVZVNNZXRJJVWBPHYWPPBOSDORZ9EQSHCZAMPVAPGFYQAUUV9DROOXJLNW",
#   |                  "addressTag":"",
#   |                  "txId":"ESBFVQUTPIWQNJSPXFNHNYHSQNTGKRVKPRABQWTAXCDWOAKDKYWPTVG9BGXNVNKTLEJGESAVXIKIZ9999",
#   |                  "insertTime":1599620082000,
#   |                  "transferType":0,
#   |                  "confirmTimes":"1/1"
#   |              }
#   |          ]
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException


#   |
#   |  cancel_order(self, **params)
#   |      Cancel an active order. Either orderId or origClientOrderId must be sent.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#cancel-order-trade
#   |
#   |      :param symbol: required
#   |      :type symbol: str
#   |      :param orderId: The unique order id
#   |      :type orderId: int
#   |      :param origClientOrderId: optional
#   |      :type origClientOrderId: str
#   |      :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
#   |      :type newClientOrderId: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "symbol": "LTCBTC",
#   |              "origClientOrderId": "myOrder1",
#   |              "orderId": 1,
#   |              "clientOrderId": "cancelMyOrder1"
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException

#   |  get_account(self, **params)
#   |      Get current account information.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#account-information-user_data
#   |
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "makerCommission": 15,
#   |              "takerCommission": 15,
#   |              "buyerCommission": 0,
#   |              "sellerCommission": 0,
#   |              "canTrade": true,
#   |              "canWithdraw": true,
#   |              "canDeposit": true,
#   |              "balances": [
#   |                  {
#   |                      "asset": "BTC",
#   |                      "free": "4723846.89208129",
#   |                      "locked": "0.00000000"
#   |                  },
#   |                  {
#   |                      "asset": "LTC",
#   |                      "free": "4763368.68006011",
#   |                      "locked": "0.00000000"
#   |                  }
#   |              ]
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException


#   |  get_account_snapshot(self, **params)
#   |      Get daily account snapshot of specific type.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#daily-account-snapshot-user_data
#   |
#   |      :param type: required. Valid values are SPOT/MARGIN/FUTURES.
#   |      :type type: string
#   |      :param startTime: optional
#   |      :type startTime: int
#   |      :param endTime: optional
#   |      :type endTime: int
#   |      :param limit: optional
#   |      :type limit: int
#   |      :param recvWindow: optional
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |             "code":200, // 200 for success; others are error codes
#   |             "msg":"", // error message
#   |             "snapshotVos":[
#   |                {
#   |                   "data":{
#   |                      "balances":[
#   |                         {
#   |                            "asset":"BTC",
#   |                            "free":"0.09905021",
#   |                            "locked":"0.00000000"
#   |                         },
#   |                         {
#   |                            "asset":"USDT",
#   |                            "free":"1.89109409",
#   |                            "locked":"0.00000000"
#   |                         }
#   |                      ],
#   |                      "totalAssetOfBtc":"0.09942700"
#   |                   },
#   |                   "type":"spot",
#   |                   "updateTime":1576281599000
#   |                }
#   |             ]
#   |          }
#   |
#   |      OR
#   |      .. code-block:: python
#   |
#   |          {
#   |             "code":200, // 200 for success; others are error codes
#   |             "msg":"", // error message
#   |             "snapshotVos":[
#   |                {
#   |                   "data":{
#   |                      "marginLevel":"2748.02909813",
#   |                      "totalAssetOfBtc":"0.00274803",
#   |                      "totalLiabilityOfBtc":"0.00000100",
#   |                      "totalNetAssetOfBtc":"0.00274750",
#   |                      "userAssets":[
#   |                         {
#   |                            "asset":"XRP",
#   |                            "borrowed":"0.00000000",
#   |                            "free":"1.00000000",
#   |                            "interest":"0.00000000",
#   |                            "locked":"0.00000000",
#   |                            "netAsset":"1.00000000"
#   |                         }
#   |                      ]
#   |                   },
#   |                   "type":"margin",
#   |                   "updateTime":1576281599000
#   |                }
#   |             ]
#   |          }
#   |
#   |      OR
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |             "code":200, // 200 for success; others are error codes
#   |             "msg":"", // error message
#   |             "snapshotVos":[
#   |                {
#   |                   "data":{
#   |                      "assets":[
#   |                         {
#   |                            "asset":"USDT",
#   |                            "marginBalance":"118.99782335",
#   |                            "walletBalance":"120.23811389"
#   |                         }
#   |                      ],
#   |                      "position":[
#   |                         {
#   |                            "entryPrice":"7130.41000000",
#   |                            "markPrice":"7257.66239673",
#   |                            "positionAmt":"0.01000000",
#   |                            "symbol":"BTCUSDT",
#   |                            "unRealizedProfit":"1.24029054"
#   |                         }
#   |                      ]
#   |                   },
#   |                   "type":"futures",
#   |                   "updateTime":1576281599000
#   |                }


#   |
#   |  get_account_status(self, **params)
#   |      Get account status detail.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#account-status-sapi-user_data
#   |
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "data": "Normal"
#   |          }


#   |  get_all_orders(self, **params)
#   |      Get all account orders; active, canceled, or filled.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#all-orders-user_data
#   |
#   |      :param symbol: required
#   |      :type symbol: str
#   |      :param orderId: The unique order id
#   |      :type orderId: int
#   |      :param startTime: optional
#   |      :type startTime: int
#   |      :param endTime: optional
#   |      :type endTime: int
#   |      :param limit: Default 500; max 1000.
#   |      :type limit: int
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          [
#   |              {
#   |                  "symbol": "LTCBTC",
#   |                  "orderId": 1,
#   |                  "clientOrderId": "myOrder1",
#   |                  "price": "0.1",
#   |                  "origQty": "1.0",
#   |                  "executedQty": "0.0",
#   |                  "status": "NEW",
#   |                  "timeInForce": "GTC",
#   |                  "type": "LIMIT",
#   |                  "side": "BUY",
#   |                  "stopPrice": "0.0",
#   |                  "icebergQty": "0.0",
#   |                  "time": 1499827319559
#   |              }
#   |          ]
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException

#   |  get_all_tickers(self) -> List[Dict[str, str]]
#   |      Latest price for all symbols.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker
#   |
#   |      :returns: List of market tickers
#   |
#   |      .. code-block:: python
#   |
#   |          [
#   |              {
#   |                  "symbol": "LTCBTC",
#   |                  "price": "4.00000200"
#   |              },
#   |              {
#   |                  "symbol": "ETHBTC",
#   |                  "price": "0.07946600"
#   |              }
#   |          ]
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException


#   |  get_asset_balance(self, asset, **params)
#   |      Get current asset balance.
#   |
#   |      :param asset: required
#   |      :type asset: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: dictionary or None if not found
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |              "asset": "BTC",
#   |              "free": "4723846.89208129",
#   |              "locked": "0.00000000"
#   |          }
#   |
#   |      :raises: BinanceRequestException, BinanceAPIException
#   |


#   |  get_asset_details(self, **params)
#   |      Fetch details on assets.
#   |
#   |      https://binance-docs.github.io/apidocs/spot/en/#asset-detail-sapi-user_data
#   |
#   |      :param asset: optional
#   |      :type asset: str
#   |      :param recvWindow: the number of milliseconds the request is valid for
#   |      :type recvWindow: int
#   |
#   |      :returns: API response
#   |
#   |      .. code-block:: python
#   |
#   |          {
#   |                  "CTR": {
#   |                      "minWithdrawAmount": "70.00000000", //min withdraw amount
#   |                      "depositStatus": false,//deposit status (false if ALL of networks' are false)
#   |                      "withdrawFee": 35, // withdraw fee
#   |                      "withdrawStatus": true, //withdraw status (false if ALL of networks' are false)
#   |                      "depositTip": "Delisted, Deposit Suspended" //reason
#   |                  },
#   |                  "SKY": {
#   |                      "minWithdrawAmount": "0.02000000",
#   |                      "depositStatus": true,
#   |                      "withdrawFee": 0.01,
#   |                      "withdrawStatus": true
#   |                  }
#   |          }

