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
        log.debug('')
        target_url = '{}/{}?'.format(self.api_url, indicator_label)
        action_data = {
            'secret': kwargs.get('secret', self.api_key),
            'exchange': kwargs.get('exchange', 'binance'),
            'symbol': kwargs.get('symbol', 'BTC/USDT'),
            'interval': kwargs.get('interval', '1h'),
        }
        action_variables = [
            (str(item) + '=' + str(action_data[item])) for item in action_data
            if action_data[item] != None
        ]
        target_url = target_url + str('&'.join(action_variables))
        return target_url

    # GENERAL

    def api_call(self, url_target, **kwargs):
        log.debug('')
        out, err, exit = shell_cmd("curl '{}' 2> /dev/null".format(url_target))
        if exit != 0:
            return False
        return out

    # ACTIONS

    def ping(self, **kwargs):
        log.debug('')
        out, err, exit = shell_cmd("ping -c 1 '{}' 2> /dev/null".format(self.api_url))
        if exit != 0:
            return False
        return True

    def adx(self, **kwargs):
        log.debug('')
        return self.api_call(self.format_target_url('adx', **kwargs))

    def macd(self, **kwargs):
        log.debug('')
        return self.api_call(self.format_target_url('macd', **kwargs))

    def ma(self, **kwargs):
        log.debug('')
        return self.api_call(self.format_target_url('ma', **kwargs))

    def rsi(self, **kwargs):
        log.debug('')
        return self.api_call(self.format_target_url('rsi', **kwargs))

    def vwap(self, **kwargs):
        log.debug('')
        return self.api_call(self.format_target_url('vwap', **kwargs))


