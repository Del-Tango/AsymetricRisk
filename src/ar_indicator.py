#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADING INDICATORS

import logging
import pysnooper

from src.backpack.bp_shell import shell_cmd

log = logging.getLogger('AsymetricRisk')


class TradingIndicator():

    def __init__(self, *args, **kwargs):
        self.api_url = kwargs.get('taapi-url', 'https://api.taapi.io')
        self.api_key = kwargs.get('taapi-key', str())

    # SETTERS

    def set_api_url(self, api_url):
        log.debug('')
        self.api_url = api_url
        return self.api_url

    def set_api_secret_key(self, api_key):
        log.debug('')
        self.api_key = api_key
        return self.api_key

    # FORMATTERS

    def format_target_url(self, indicator_label, *args, **kwargs):
        '''
        [ RETURN ]: Obviously... right?
        '''
        log.debug('')
        target_url = '{}/{}?'.format(self.api_url, indicator_label)
        action_data = {
            'secret': kwargs.get('secret', self.api_key),
            'exchange': kwargs.get('exchange', 'binance'),
            'symbol': kwargs.get('symbol', 'BTC/USDT'),
            'interval': kwargs.get('interval', '1h'),
            'period': kwargs.get('period'),
            'backtrack': kwargs.get('backtrack'),
            'backtracks': kwargs.get('backtracks'),
            'chart': kwargs.get('chart'),
            'optInFastPeriod': kwargs.get('macd-fast-period'),
            'optInSlowPeriod': kwargs.get('macd-slow-period'),
            'optInSignalPeriod': kwargs.get('macd-signal-period'),
        }
        action_variables = [
            (str(item) + '=' + str(action_data[item])) for item in action_data
            if action_data[item] != None
        ]
        target_url = target_url + str('&'.join(action_variables))
        return target_url

    # GENERAL

    def api_call(self, url_target, **kwargs):
        '''
        [ RETURN ]: Command STDOUT or False
        '''
        log.debug('')
        out, err, exit = shell_cmd("curl '{}' 2> /dev/null".format(url_target))
        if exit != 0:
            return False
        return out

    # ACTIONS

    def ping(self, **kwargs):
        '''
        [ RETURN ]: True or False
        '''
        log.debug('')
        out, err, exit = shell_cmd(
            "ping -c 1 '{}' 2> /dev/null".format(
                self.api_url.replace('https://', '').replace('http://', '')
            )
        )
        if exit != 0:
            return False
        return True

    def adx(self, **kwargs):
        '''
        [ RETURN ]: Example - 'b\'{"value":27.163106189421097}\''
        '''
        log.debug('')
        return self.api_call(self.format_target_url('adx', **{
            'period': kwargs.get('adx-period', kwargs.get('period')),
            'backtrack': kwargs.get('adx-backtrack'),
            'backtracks': kwargs.get('adx-backtracks'),
            'chart': kwargs.get('adx-chart'),
            'interval': kwargs.get('adx-interval', kwargs.get('interval'))
        }))

    def macd(self, **kwargs):
        '''
        [ RETURN ]: Example - 'b\'{"valueMACD":47.481220348032366,"valueMACDSignal":78.66025805066222,"valueMACDHist":-31.179037702629856}\''
        '''
        log.debug('')
        return self.api_call(self.format_target_url('macd',  **{
            'backtrack': kwargs.get('macd-backtrack'),
            'backtracks': kwargs.get('macd-backtracks'),
            'chart': kwargs.get('macd-chart'),
            'interval': kwargs.get('macd-interval', kwargs.get('interval')),
            'macd-fast-period': kwargs.get('macd-fast-period'),
            'macd-slow-period': kwargs.get('macd-slow-period'),
            'macd-signal-period': kwargs.get('macd-signal-period'),
        }))

    def ma(self, **kwargs):
        '''
        [ RETURN ]: Example - 'b\'{"value":21315.933999999987}\''
        '''
        log.debug('')
        return self.api_call(self.format_target_url('ma', **{
            'period': kwargs.get('ma-period', kwargs.get('period')),
            'backtrack': kwargs.get('ma-backtrack'),
            'backtracks': kwargs.get('ma-backtracks'),
            'chart': kwargs.get('ma-chart'),
            'interval': kwargs.get('ma-interval', kwargs.get('interval'))
        }))

    def ema(self, **kwargs):
        '''
        [ RETURN ]: Example - 'b\'{"value":20884.645666666664}\''
        '''
        log.debug('')
        return self.api_call(self.format_target_url('ema', **{
            'period': kwargs.get('ema-period', kwargs.get('period')),
            'backtrack': kwargs.get('ema-backtrack'),
            'backtracks': kwargs.get('ema-backtracks'),
            'chart': kwargs.get('ema-chart'),
            'interval': kwargs.get('ema-interval', kwargs.get('interval'))
        }))

    def rsi(self, **kwargs):
        '''
        [ RETURN ]: Example - 'b\'{"value":50.978938548271955}\''
        '''
        log.debug('')
        return self.api_call(self.format_target_url('rsi', **{
            'period': kwargs.get('rsi-period', kwargs.get('period')),
            'backtrack': kwargs.get('rsi-backtrack'),
            'backtracks': kwargs.get('rsi-backtracks'),
            'chart': kwargs.get('rsi-chart'),
            'interval': kwargs.get('rsi-interval', kwargs.get('interval'))
        }))

    def vwap(self, **kwargs):
        '''
        [ RETURN ]: Example - "b\"{"value":20513.436047490202}\""
        '''
        log.debug('')
        return self.api_call(self.format_target_url('vwap', **{
            'period': kwargs.get('vwap-period', kwargs.get('period')),
            'backtrack': kwargs.get('vwap-backtrack'),
            'backtracks': kwargs.get('vwap-backtracks'),
            'chart': kwargs.get('vwap-chart'),
            'interval': kwargs.get('vwap-interval', kwargs.get('interval'))
        }))

# CODE DUMP

