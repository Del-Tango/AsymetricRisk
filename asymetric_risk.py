#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK - (A)Risk

import os
import btalib
import pandas as pd

from time import sleep
from binance.client import Client
from binance import ThreadedWebsocketManager


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
}

client = Client(AR_DEFAUL['api-key'], AR_DEFAULT['api-secret'])
client.API_URL = AR_DEFAULT['api-url']

# FETCHERS

# SETTERS

# CHECKERS

# GENERAL

# ACTIONS

# HANDLERS

# PARSERS

# TODO
def parse_command_line_arguments():
    pass

# INIT

# TODO
def init_asymetric_risk():
    pass

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
