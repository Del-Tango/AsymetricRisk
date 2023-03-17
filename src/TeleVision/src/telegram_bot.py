#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# Telegram Messaging Bot

import logging
import asyncio
import requests

from telegram.ext import *
from src.tv_bot_ctrls import *
from src.backpack.bp_general import write2file, read_file

log = logging.getLogger('TeleVision')


class TelegramBot():

    _target_url = 'https://api.telegram.org'

    def __init__(self, *args, **kwargs):
        log.debug('')
        self._bot_token = kwargs.get('bot-token', str())
        self._chat_id = kwargs.get('chat-id', str())
        self._use_context = kwargs.get('context', True)
        self._update_queue = asyncio.queues.Queue
        self._poll_interval = kwargs.get('poll-interval', 0.0)
        self._timeout = kwargs.get('timeout', 10)
        self._target_url = kwargs.get('target-url', 'https://api.telegram.org')
        self._message = kwargs.get('message', 'Welcome to TeleVision!')
        self._url_cache = {}
        self._last_response = None
        self.updater = None
        self.setup()

    # DUNDERS

    def __str__(self):
        return ''.join(list(self._bot_token)[0:5]) + '...'

    # CREATORS

    def create_updater(self, **kwargs):
        log.debug('')
        obj = Application.builder()\
            .token(kwargs.get('bot-token', self._bot_token)).build()
        return obj

    # FORMATTERS

    def format_url_for_action_send_message(self, *args, **kwargs):
        log.debug('')
        url = '{}/bot{}/sendMessage?chat_id={}&text={}'.format(
            self._target_url, self._bot_token, self._chat_id, self._message
        )
        self._url_cache.update({'send-msg': url})
        return url

    def format_url_for_action_get_updates(self, *args, **kwargs):
        log.debug('')
        url = '{}/bot{}/getUpdates'.format(self._target_url, self._bot_token)
        if not self._url_cache.get('get-updates'):
            self._url_cache.update({'get-updates': url})
            return url
        return self._url_cache.get('get-updates')

    # GENERAL

    def add_bot_ctrl_handlers(self, dispatcher):
        log.debug('')
        if not BOT_CTRL_INDEX:
            log.error('No BOT_CTRL_INDEX found after importing tv_bot_ctrls!')
            return False
        dispatcher.add_error_handler(BOT_CTRL_INDEX['error'])
        for key in BOT_CTRL_INDEX:
            if key == 'error':
                continue
            dispatcher.add_handler(CommandHandler(key, BOT_CTRL_INDEX[key]))
        return dispatcher

    # ACTIONS

    def run_single_message(self, message, **kwargs):
        '''
        [ RETURN ]: {
            'ok': True,
            'result': {
                'message_id': 9,
                'from': {
                    'id': xxxxxxxxxx,
                    'is_bot': True,
                    'first_name': 'TeleVision',
                    'username': 'xXxBot'
                },
                'chat': {
                    'id': xxxxxxxxx,
                    'first_name': 'YoName',
                    'username': 'YoName',
                    'type': 'private'
                },
                'date': 1674364048,
                'text': 'Yo'
            }
        }
        '''
        log.debug('')
        self._message = message
        url = self.format_url_for_action_send_message()
        response = requests.get(url).json()
        self._last_response = response
        return response

    def run_bot_ctrls(self, updater):
        log.debug('')
        updater.run_polling(self._poll_interval, timeout=self._timeout or 10)
        updater.idle()
        return True

    # CLEANERS

    # TODO - To be continued...
    def cleanup_chat_data(self, **kwargs):
        log.debug('TODO - Under construction, building...')
        # drop_chat_data
    def cleanup_user_data(self, **kwargs):
        log.debug('TODO - Under construction, building...')
        # drop_user_data

    def cleanup(self, *args, **kwargs):
        log.debug('')
        handlers = {
            'chat-data': cleanup_chat_data,
            'user-data': cleanup_user_data,
        }
        targets = handlers.keys() if not args or 'all' in args else args
        failures = 0
        for target in targets:
            clean = handlers[target](**kwargs)
            if not clean:
                failures += 1
        return failures

    # SETUP

    def setup(self, **kwargs):
        log.debug('')
        self.updater = self.create_updater(**kwargs)
        if not self.updater:
            log.warning('Could not create Bot updater instance!')
            return False
        setup_handlers = self.add_bot_ctrl_handlers(self.updater)
        if not setup_handlers:
            log.warning('Could not properly set up Bot CTRL handlers!')
            return False
        return True

# CODE DUMP

