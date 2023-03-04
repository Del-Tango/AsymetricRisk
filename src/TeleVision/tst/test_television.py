import unittest
import os
import time

from src.telegram_bot import TelegramBot
from src.backpack.bp_general import stdout_msg, read_file
from src.backpack.bp_shell import shell_cmd
from src.backpack.bp_checkers import check_pid_running

class TestTeleVision(unittest.TestCase):

    conf_file = 'conf/television.conf.json' \
        if os.path.exists('conf/television.conf.json') else ''
    log_file = 'log/television.log'
    init_script = 'television.py'
    tmp_pid_file = '/tmp/tv_test_suit.pid'

    # PREREQUISITS

    @classmethod
    def setUpClass(cls):
        stdout_msg('Functional test suit -\n', symbol='TeleVision', bold=True)

    @classmethod
    def tearDownClass(cls):
        cmd = 'rm {}'.format(cls.tmp_pid_file)
        shell_cmd(cmd)
        stdout_msg('TeleVision Test Suit\n', done=True)

    # FORMATTERS

    # [ NOTE ]: Don't be a smart ass and refactor these. For future ease of
    #           interface modding each command should have it's own individual
    #           formatter function separated from the others.

    def format_scroll_msg_cmd(self):
        cmd = '{} --config-file {} --log-file {} --action scroll-msg '\
            '--watchdog'.format(self.init_script, self.conf_file, self.log_file)
        return cmd

    def format_scroll_file_cmd(self):
        cmd = '{} --config-file {} --log-file {} --action scroll-file '.format(
                self.init_script, self.conf_file, self.log_file
            )
        return cmd

    def format_bot_ctrl_cmd(self):
        cmd = '{} --config-file {} --log-file {} --action bot-ctrl '\
            '& && echo $! > {}'.format(
                self.init_script, self.conf_file, self.log_file, self.tmp_pid_file
            )
        return cmd

    def format_scroll_msg_watchdog_cmd(self):
        cmd = '{} --config-file {} --log-file {} --action scroll-msg '\
            '--watchdog & && echo $! > {}'.format(
                self.init_script, self.conf_file, self.log_file, self.tmp_pid_file
            )
        return cmd

    def format_scroll_file_watchdog_cmd(self):
        cmd = '{} --config-file {} --log-file {} --action scroll-file '\
            '--watchdog & && echo $! > {}'.format(
                self.init_script, self.conf_file, self.log_file, self.tmp_pid_file
            )
        return cmd

    # TESTERS

    def process_pid(self):
        pid_file_content = read_file(self.tmp_pid_file)
        process_pid = None \
            if (not pid_file_content or len(pid_file_content) == 1 \
                and pid_file_content[0] != '') else int(pid_file_content[0])
        self.assertTrue(process_pid)
        check_pid = check_pid_running(process_pid)
        shell_cmd('echo -n > {}'.format(self.tmp_pid_file))
        self.assertTrue(check_pid)
        shell_cmd('kill -9 {}'.format(process_pid))

    def test_scroll_msg(self):
        stdout_msg('Send scroll message...', symbol='TEST')
        command = self.format_scroll_msg_cmd()
        stdout, stderr, exit_code = shell_cmd(command)
        self.assertEqual(exit_code, 0)

    def test_scroll_file(self):
        stdout_msg('Send scroll file content...', symbol='TEST')
        command = self.format_scroll_file_cmd()
        stdout, stderr, exit_code = shell_cmd(command)
        self.assertEqual(exit_code, 0)

    def test_bot_ctrl(self):
        stdout_msg('Activate user bot controls...', symbol='TEST')
        command = self.format_bot_ctrl_cmd()
        stdout, stderr, exit_code = shell_cmd(command)
        self.process_pid()
        self.assertEqual(exit_code, 0)

    def test_scroll_msg_watchdog(self):
        stdout_msg('Send scroll messages from interactive prompt...', symbol='TEST')
        command = self.format_scroll_msg_watchdog_cmd()
        stdout, stderr, exit_code = shell_cmd(command)
        self.process_pid()
        self.assertEqual(exit_code, 0)

    def test_scroll_file_watchdog(self):
        stdout_msg('Send a new scroll for every new file update...', symbol='TEST')
        command = self.format_scroll_file_watchdog_cmd()
        stdout, stderr, exit_code = shell_cmd(command)
        self.process_pid()
        self.assertEqual(exit_code, 0)
