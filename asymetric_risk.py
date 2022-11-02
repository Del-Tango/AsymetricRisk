#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK - (A)Risk

import os
import logging
import pysnooper

from time import sleep
from src.backpack.bp_log import log_init
from src.backpack.bp_ensurance import ensure_files_exist, ensure_directories_exist
from src.backpack.bp_shell import shell_cmd
from src.backpack.bp_checkers import check_file_exists
from src.backpack.bp_general import stdout_msg, clear_screen
from src.ar_market import TradingMarket
from src.ar_bot import TradingBot

AR_SCRIPT_NAME = "AsymetricRisk",
AR_SCRIPT_DESCRIPTION = "Crypto Trading Bot"
AR_VERSION = "AR15",
AR_VERSION_NO = "1.0",

# COLD ARGS

AR_PROJECT_DIR = os.path.dirname(__file__)

# HOT ARGS

AR_DEFAULT = {
    "log-dir": AR_PROJECT_DIR + " /log",
    "conf-dir": AR_PROJECT_DIR + " /conf",
    "lib-dir": AR_PROJECT_DIR + " /lib",
    "src-dir": AR_PROJECT_DIR + " /src",
    "dox-dir": AR_PROJECT_DIR + " /dox",
    "dta-dir": AR_PROJECT_DIR + " /data",
    "tmp-dir": "/tmp",
    "log-file": "asymetric_risk.log",
    "conf-file": "asymetric_risk.conf.json",
    "init-file": __file__,
    "log-format": "[ %(asctime)s ] %(name)s [ %(levelname)s ] %(thread)s - %(filename)s - %(lineno)d: %(funcName)s - %(message)s",
    "timestamp-format": "%d/%m/%Y-%H:%M:%S",
    "api-key": os.environ.get('binance_api'),
    "api-secret": os.environ.get('binance_secret'),
    "api-url": 'https://testnet.binance.vision/api',
    "base-currency": 'BTC',
    "quote-currency": 'ETH',
    "period-start": '01-10-2022',
    "period-end": '01-11-2022',
    "debug": False,
    "silence": False,
}

log = log_init(
    '/'.join([AR_DEFAULT['log-dir'], AR_DEFAULT['log-file']]),
    AR_DEFAULT['log-format'], AR_DEFAULT['timestamp-format'],
    AR_DEFAULT['debug'], log_name=str(AR_SCRIPT_NAME)
)
trading_market = TradingMarket(AR_DEFAULT['api-key'], AR_DEFAULT['api-secret'], sync=True, **AR_DEFAULT)
trading_bot = TradingBot(trading_market, **AR_DEFAULT)

# FETCHERS

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

# HANDLERS

# TODO
#@pysnooper.snoop()
def handle_actions(actions=[], *args, **kwargs):
    log.debug('')
    failure_count = 0
#   handlers = {
#       'open-gates': action_open_gates,
#   }
#   for action_label in actions:
#       stdout_msg('INFO: Processing action... ({})'.format(action_label))
#       if action_label not in handlers.keys():
#           stdout_msg(
#               'NOK: Invalid action label specified! ({})'.format(action_label)
#           )
#           continue
#       handle = handlers[action_label](*args, **kwargs)
#       if isinstance(handle, int) and handle != 0:
#           stdout_msg(
#               'NOK: Action ({}) failures detected! ({})'.format(action_label, handle)
#           )
#           failure_count += 1
#           continue
#       stdout_msg("OK: Action executed successfully! ({})".format(action_label))
#   return True if failure_count == 0 else failure_count

# CREATORS

# TODO
def create_command_line_parser():
    log.debug('')
#   help_msg = format_header_string() + '''
#   [ EXAMPLE ]: Setup FloodGate NODE unit -

#       ~$ %prog \\
#           -S  | --setup \\
#           -c  | --config-file /etc/conf/fg-node.conf.json \\
#           -l  | --log-file /etc/log/fg-node.log

#   [ EXAMPLE ]: Open flood gates 1, 2 and 3 with no STDOUT output -

#       ~$ %prog \\
#           -a  | --action open-gates \\
#           -g  | --gate 1,2,3 \\
#           -s  | --silence \\
#           -c  | --config-file /etc/conf/fg-node.conf.json \\
#           -l  | --log-file /etc/log/fg-node.log

#   [ EXAMPLE ]: Turn on ACT lights for gates 1, 2 and 3 in DEBUG mode -

#       ~$ %prog \\
#           -a  | --action lights-on \\
#           -L  | --light 1,2,3 \\
#           -D  | --debug \\
#           -c  | --config-file /etc/conf/fg-node.conf.json \\
#           -l  | --log-file /etc/log/fg-node.log'''
#   parser = optparse.OptionParser(help_msg)
#   return parser

# PROCESSORS

# TODO
def process_command_line_options(parser):
    '''
    [ NOTE ]: In order to avoid a bad time in STDOUT land, please process the
              silence flag before all others.
    '''
    log.debug('')
#   (options, args) = parser.parse_args()
#   processed = {
#       'silence_flag': process_silence_argument(parser, options),
#       'log_file': process_log_file_argument(parser, options),
#       'setup_flag': process_setup_argument(parser, options),
#       'action_csv': process_action_csv_argument(parser, options),
#       'light_csv': process_light_csv_argument(parser, options),
#       'gate_csv': process_gate_csv_argument(parser, options),
#       'flash_count': process_flash_count_argument(parser, options),
#       'identity': process_identity_argument(parser, options),
#       'config_file': process_config_file_argument(parser, options),
#       'debug_flag': process_debug_mode_argument(parser, options),
#   }
#   return processed

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

# TODO
def add_command_line_parser_options(parser):
    log.debug('')
    parser.add_option(
        '-s', '--silence', dest='silence', action='store_true',
        help='Eliminates all STDOUT messages.'
    )
#   parser.add_option(
#       '-a', '--action', dest='action_csv', type='string', metavar='ACTION-CSV',
#       help='Action to execute - valid values include one or more of the '
#            'following labels given as a CSV string: (open-gates | close-gates '
#            '| set-id | setup | lights-on | lights-off | spl-r2p | spl-mon)'
#   )
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

def parse_command_line_arguments():
    log.debug('')
    parser = create_command_line_parser()
    add_command_line_parser_options(parser)
    return process_command_line_options(parser)

# GENERAL

# TODO
def cleanup():
    pass

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
            content = json.load(conf_file_path)
            AR_DEFAULT.update(content['AR_DEFAULT'])
            AR_CARGO.update(content['AR_CARGO'])
            AR_SCRIPT_NAME = content['AR_SCRIPT_NAME']
            AR_SCRIPT_DESCRIPTION = content['AR_SCRIPT_DESCRIPTION']
            AR_VERSION = content['AR_VERSION']
            AR_VERSION_NO = content['AR_VERSION_NO']
        except Exception as e:
            log.error(e)
            stdout_msg('[ NOK ]: Could not load config file! ({})'.format(conf_file_path))
            return False
    stdout_msg('[ OK ]: Settings loaded from config file! ({})'.format(conf_file_path))
    return True

# SETUP

def setup_trading_market():
    global trading_market
    trading_market = TradingMarket(
        AR_DEFAULT['api-key'], AR_DEFAULT['api-secret'], sync=True, **AR_DEFAULT
    )
    trading_market.API_URL = AR_DEFAULT['api-url']
    return trading_market

def setup_trading_bot():
    global trading_bot
    trading_bot = TradingBot(trading_market, **AR_DEFAULT)
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

def init_asymetric_risk(*args, **kwargs):
    log.debug('')
    exit_code = 0
    display_header()
    config_setup = load_config_json()
    if not config_setup:
        stdout_msg('[ WARNING ]: Could not load config file!')
    market_setup = setup_trading_market()
    if not market_setup:
        stdout_msg('[ WARNING ]: Could not set up trading market!')
    bot_setup = setup_trading_bot()
    if not bot_setup:
        stdout_msg('[ WARNING ]: Could not set up trading bot!')
    stdout_msg('[ INFO ]: Verifying action preconditions...')
    check = check_preconditions()
    if not isinstance(check, int) or check != 0:
        stdout_msg('[ ERROR ]: Preconditions not met!')
        return check
    handle = handle_actions(*args, **kwargs)
    if not handle:
        stdout_msg('[ WARNING ]: Action not have been handled properly!')
    return 0 if handle is True else handle

# MISCELLANEOUS

if __name__ == '__main__':
    parse_command_line_arguments()
    clear_screen()
    EXIT_CODE = 1
    try:
        EXIT_CODE = init_asymetric_risk()
    finally:
        cleanup()
    stdout_msg('[ DONE ]: Terminating! ({})'.format(EXIT_CODE))
    exit(EXIT_CODE)











# CODE DUMP

# trading_bot = TradingBot(TradingMarket(**AR_DEFAULT), **AR_DEFAULT)
# trade = trading_bot.trade({
#   'crypto': 'ETH', 'buy-price': N, 'sell-price': N, 'take-profit': 30%,
#   'stop-loss': 10%, trailing-stop-loss: 10%,
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

