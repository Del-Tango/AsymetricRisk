import unittest
import os

from src.telegram_bot import TelegramBot
from src.backpack.bp_general import stdout_msg
from src.backpack.bp_convertors import json2dict

class TestTelegramBot(unittest.TestCase):

    conf_file = 'conf/television.conf.json' \
        if os.path.exists('conf/television.conf.json') else ''
    TV_DEFAULT = json2dict(conf_file)

    # PREREQUISITS

    @classmethod
    def setUpClass(cls):
        stdout_msg('Functional test suit -\n', symbol='TelegramBot', bold=True)
        cls.trading_bot = TelegramBot(**cls.TV_DEFAULT)

    @classmethod
    def tearDownClass(cls):
        stdout_msg('TelegramBot\n', done=True)

    # TESTERS

    def test_run_single_message(self,):
        stdout_msg('Run single message...', symbol='TEST')
        message = 'Functional TeleVision test suit says Hi!'
        run = self.trading_bot.run_single_message(message)
        assertTrue(isinstance(run, dict))
        assertTrue(run.get('ok'))

    def test_run_bot_ctrls(self,):
        stdout_msg('Run bot ctrls...', symbol='TEST')
        run = self.trading_bot.run_bot_ctrls(self.trading_bot.updater)
        assertTrue(run)

