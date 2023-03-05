#!/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# TeleVision - Telegram Messaging Bot

import os
import logging
import optparse
import time
import json
import pysnooper

from src.backpack.bp_log import log_init
from src.backpack.bp_shell import shell_cmd
from src.backpack.bp_general import (
    stdout_msg, clear_screen, pretty_dict_print, write2file, read_file
)
from src.backpack.bp_filters import filter_directory_from_path
from src.backpack.bp_checkers import check_file_exists
from src.backpack.bp_fetchers import fetch_timestamp

TV_SCRIPT_NAME = 'TeleVision'
TV_SCRIPT_DESCRIPTION = 'Telegram Messaging Bot'
TV_VERSION = 'UnitsOfThought'
TV_VERSION_NO = '1.0'
TV_DEFAULT = {
    'conf-file': 'conf/television.conf.json',
    'log-file': 'log/television.log',
    'input-file': 'dta/television.in',      # For outgoing messages
    'out-file': 'dta/television.out',       # For incomming messages
    'log-format': '[ %(asctime)s ] %(name)s [ %(levelname)s ] %(thread)s - %(filename)s - %(lineno)d: %(funcName)s - %(message)s',
    'timestamp-format': '%d/%m/%Y-%H:%M:%S',
    'target-url': 'https://api.telegram.org',
    'message': 'TeleVision works!',
    'poll-interval': 0.0,
    'scroll-interval': 0,
    'bot-token': str(),
    'chat-id': str(),
    "action": "scroll-msg", # scroll-msg, scroll-file, bot-ctrl
    "watchdog": False,
    "silence": False,
    'debug': False,
}
log = logging.getLogger(TV_SCRIPT_NAME)

# FETCHERS

def fetch_action_handlers():
    log.debug('')
    return {
        'scroll-msg': action_scroll_msg,
        'scroll-file': action_scroll_file,
        'bot-ctrl': action_bot_ctrl,
    }

# CHECKERS

def check_preconditions(**kwargs):
    log.debug('')
    stdout_msg(
        'Verifying action preconditions...',
        info=True, silence=TV_DEFAULT['silence']
    )
    checkers = {
        'preconditions-conf': check_config_file(**kwargs),
        'preconditions-log': check_log_file(**kwargs),
    }
    log.debug('checkers: {}'.format(checkers))
    if False in checkers.values():
        return len([item for item in checkers.values() if not item])
    return 0

def check_config_file(**kwargs):
    log.debug('')
    stdout_msg('Check config file...', info=True, silence=TV_DEFAULT['silence'])
    exit_code = 0
    if not check_file_exists(TV_DEFAULT['conf-file']):
        cmd_out, cmd_err, exit_code = shell_cmd(
            'touch ' + TV_DEFAULT['conf-file'] + ' &> /dev/null'
        )
    return_flag = False if exit_code != 0 else True
    if return_flag:
        stdout_msg('Config file!', ok=True, silence=TV_DEFAULT['silence'])
    else:
        stdout_msg(
            'Could not make sure config file exists and is writable!',
            nok=True, silence=TV_DEFAULT['silence']
        )
    return return_flag

def check_log_file(**kwargs):
    log.debug('')
    stdout_msg('Checking log file...', info=True, silence=TV_DEFAULT['silence'])
    exit_code = 0
    if not check_file_exists(TV_DEFAULT['log-file']):
        cmd_out, cmd_err, exit_code = shell_cmd(
            'touch ' + TV_DEFAULT['log-file'] + ' &> /dev/null'
        )
    return_flag = False if exit_code != 0 else True
    if return_flag:
        stdout_msg('Log file!', ok=True, silence=TV_DEFAULT['silence'])
    else:
        stdout_msg(
            'Could not make sure log file exists and is writable!',
            nok=True, silence=TV_DEFAULT['silence']
        )
    return return_flag

# CLEANERS

def cleanup():
    log.debug('Nothing to cleanup... yet.')
    return True

# FORMATTERS

def format_header_string():
    header = '''
    ___________________________________________________________________________

     *                            *  {}  *                           *
    __________________________________________________v{}{}_______
               Excellent Regards, the Alveare Solutions #!/Society -x
    '''.format(TV_SCRIPT_NAME, TV_VERSION_NO, TV_VERSION)
    return header

# GENERAL

def update_log():
    global log
    del log
    log = log_init(
        TV_DEFAULT['log-file'], TV_DEFAULT['log-format'],
        TV_DEFAULT['timestamp-format'], TV_DEFAULT['debug'],
        log_name=TV_SCRIPT_NAME
    )
    return log

#@pysnooper.snoop()
def load_config_json():
    global TV_DEFAULT
    global TV_SCRIPT_NAME
    global TV_SCRIPT_DESCRIPTION
    global TV_VERSION
    global TV_VERSION_NO
    log.debug('')
    if not os.path.isfile(TV_DEFAULT['conf-file']):
        stdout_msg(
            'File not found! ({})'.format(TV_DEFAULT['conf-file']),
            nok=True, silence=TV_DEFAULT['silence']
        )
        return False
    try:
        with open(TV_DEFAULT['conf-file'], 'r', encoding='utf-8', errors='ignore') as fl:
            content = json.load(fl)
        TV_DEFAULT.update(content['TV_DEFAULT'])
        TV_SCRIPT_NAME = content['TV_SCRIPT_NAME']
        TV_SCRIPT_DESCRIPTION = content['TV_SCRIPT_DESCRIPTION']
        TV_VERSION = content['TV_VERSION']
        TV_VERSION_NO = content['TV_VERSION_NO']
    except Exception as e:
        log.error(e)
        stdout_msg(
            'Could not load config file! ({})'.format(TV_DEFAULT['conf-file']),
            nok=True, silence=TV_DEFAULT['silence']
        )
        return False
    stdout_msg(
        'Settings loaded from config file! ({})'.format(TV_DEFAULT['conf-file']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

# ACTIONS

# [ NOTE ]: Actions must return a numerical exit code to their handler and
#           accept any number of positional and keyword arguments.

def action_scroll_msg(*args, **kwargs):
    log.debug('')
    if TV_DEFAULT['watchdog']:
        while True:
            stdout_msg(
                'Type TeleVision scroll message or (.back)...',
                info=True, silence=TV_DEFAULT['silence']
            )
            msg = input('(TV)Scroll: ')
            if msg == '.back':
                stdout_msg(
                    'Aborting action..', info=True, silence=TV_DEFAULT['silence']
                )
                break
            stdout_msg('Sending..', silence=TV_DEFAULT['silence'])
            send = bot.run_single_message(msg)
            if not send:
                stdout_msg(
                    'Could not send TV scroll!',
                    warn=True, silence=TV_DEFAULT['silence']
                )
            time.sleep(TV_DEFAULT['scroll-interval'])
    else:
        send = bot.run_single_message(TV_DEFAULT['message'])
        if not send:
            stdout_msg(
                'Could not send TV scroll!',
                warn=True, silence=TV_DEFAULT['silence']
            )
    return 0

#@pysnooper.snoop()
def action_scroll_file(*args, **kwargs):
    log.debug('')
    log.debug('Action *args, **kwargs - {}, {}'.format(args, kwargs))
    in_files = kwargs.get('input-file', TV_DEFAULT['input-file']).split(',')
    log.debug('Input files: {}'. format(in_files))
    return action_scroll(*in_files, **kwargs)

#@pysnooper.snoop()
def action_scroll(*args, **kwargs):
    log.debug('TODO - Refactor')
    if TV_DEFAULT['watchdog']:
        while True:
            for path in args:
                content = read_file(path)
                if not content or len(content) == 1 and content[0] in ('', '\n'):
                    continue
                stdout_msg(
                    'Updates found in file ({})'.format(path),
                    symbol=fetch_timestamp(), silence=TV_DEFAULT['silence']
                )
                send = bot.run_single_message(''.join(content))
                if not send:
                    stdout_msg(
                        'Could not send updated message! \n\n({})'.format(
                            ''.join(content)
                        ), nok=True, silence=TV_DEFAULT['silence']
                    )
                else:
                    stdout_msg(
                        'Message sent!',
                        ok=True, silence=TV_DEFAULT['silence']
                    )
                stdout_msg(
                    'Cleaning up file', info=True, silence=TV_DEFAULT['silence']
                )
                write2file('', file_path=path)
            time.sleep(TV_DEFAULT['scroll-interval'])
    else:
        for path in args:
            content = read_file(path)
            if not content:
                continue
            stdout_msg(
                '{} - Updates found in file ({})'.format(
                    fetch_timestamp(), path
                ), info=True, silence=TV_DEFAULT['silence']
            )
            send = bot.run_single_message(''.join(content))
            if not send:
                stdout_msg(
                    'Could not send updated message! \n\n({})'.format(
                        ''.join(content)
                    ), nok=True, silence=TV_DEFAULT['silence']
                )
            else:
                stdout_msg(
                    'Message sent!',
                    ok=True, silence=TV_DEFAULT['silence']
                )
            stdout_msg(
                'Cleaning up file', info=True, silence=TV_DEFAULT['silence']
            )
            overwrite = write2file('', file_path=path)
    return 0

def action_bot_ctrl(*args, **kwargs):
    log.debug('')
    start = bot.run_bot_ctrls(bot.updater)
    return 0

# HANDLERS

#@pysnooper.snoop()
def handle_actions(*args, **kwargs):
    log.debug('')
    failure_count = 0
    handlers = fetch_action_handlers()
    if not args:
        stdout_msg(
            'No action label specified. You may need some --help.',
            warn=True, silence=TV_DEFAULT['silence']
        )
        return 1
    for action_label in args:
        stdout_msg(
            'Processing action... ({})'.format(action_label),
            info=True, silence=TV_DEFAULT['silence']
        )
        if action_label not in handlers.keys():
            stdout_msg(
                'Invalid action label specified! ({})'
                .format(action_label), nok=True, silence=TV_DEFAULT['silence']
            )
            failure_count += 1
            continue
        try:
            handle = handlers[action_label](**kwargs)
            if (handle != 0 and not handle) \
                    or (isinstance(handle, int) and handle != 0):
                stdout_msg(
                    'Action ({}) failures detected! ({})'
                    .format(action_label, handle),
                    warn=True, silence=TV_DEFAULT['silence']
                )
                failure_count += 1
                continue
        except Exception as e:
            log.error(e)
            stdout_msg(
                'Action ({}) terminated abnormaly! Details: {}'.format(
                    action_label, e
                ), err=True, silence=TV_DEFAULT['silence'])
            return failure_count + 1
        stdout_msg(
            "Action executed successfully! ({})".format(action_label),
            ok=True, silence=TV_DEFAULT['silence']
        )
    return failure_count

# DISPLAY

def display_header():
    if TV_DEFAULT['silence']:
        return False
    stdout_msg(format_header_string(), bold=True, silence=TV_DEFAULT['silence'])
    return True

# CREATORS

def create_telegram_bot(**kwargs):
    log.debug('')
    tbot = TelegramBot(context=True, **kwargs)
    return tbot

def create_command_line_parser():
    log.debug('')
    help_msg = format_header_string() + '''
    [ EXAMPLE ]: Issue single message using bot xXx in debug mode but with
                 STDOUT and STDERR silenced, soo no output... yeah, that's right -

        ~$ %prog \\
            -D  | --debug \\
            -S  | --silence \\
            -c  | --config-file /etc/conf/tv.conf.json \\
            -l  | --log-file /etc/log/tv.log \\
            -a  | --action scroll-msg \\
            -t  | --bot-token xXx \\
            -i  | --chat-id xXx \\
            -m  | --message 'TeleVision Works!'

    [ EXAMPLE ]: Open interactive promp for issuing single messages -

        ~$ %prog \\
            -c  | --config-file /etc/conf/tv.conf.json \\
            -l  | --log-file /etc/log/tv.log \\
            -a  | --action scroll-msg \\
            -t  | --bot-token xXx \\
            -i  | --chat-id xXx \\
            -w  | --watchdog

    [ EXAMPLE ]: Dump contents of file in chat room  -

        ~$ %prog \\
            -c  | --config-file /etc/conf/tv.conf.json \\
            -l  | --log-file /etc/log/tv.log \\
            -a  | --action scroll-file \\
            -t  | --bot-token xXx \\
            -i  | --chat-id xXx \\
            -f  | --input-file /file/path1,/file/path2

    [ EXAMPLE ]: Monitor file and issue messages with all new file lines -

        ~$ %prog \\
            -c  | --config-file /etc/conf/tv.conf.json \\
            -l  | --log-file /etc/log/tv.log \\
            -a  | --action scroll-file \\
            -t  | --bot-token xXx \\
            -i  | --chat-id xXx \\
            -f  | --input-file /file/path1,/file/path2 \\
            -w  | --watchdog

    [ EXAMPLE ]: Start custom bot control handlers the user can access with
                 /commands to run functions from src/backpack/tv_bot_ctrls.py -

        ~$ %prog \\
            -c  | --config-file /etc/conf/tv.conf.json \\
            -l  | --log-file /etc/log/tv.log \\
            -a  | --action bot-ctrl \\
            -t  | --bot-token xXx'''
    parser = optparse.OptionParser(help_msg)
    return parser

# PROCESSORS

def process_command_line_options(parser):
    log.debug('')
    (options, args) = parser.parse_args()
    processed = {
        'config_file': process_config_file_argument(parser, options),
        'log_file': process_log_file_argument(parser, options),
        'input_file': process_input_file_argument(parser, options),
        'action': process_action_argument(parser, options),
        'message': process_message_argument(parser, options),
        'bot_token': process_bot_token_argument(parser, options),
        'chat_id': process_chat_id_argument(parser, options),
        'debug_flag': process_debug_mode_argument(parser, options),
        'silence_flag': process_silence_argument(parser, options),
        'watchdog_flag': process_watchdog_argument(parser, options),
    }
    return processed

def process_chat_id_argument(parser, options):
    global TV_DEFAULT
    log.debug('')
    identifier = options.chat_id
    if identifier == None:
        log.warning(
            'No chat ID provided. Defaulting to ({}).'\
            .format(TV_DEFAULT['chat-id'])
        )
        return False
    TV_DEFAULT['chat-id'] = identifier
    stdout_msg(
        'Chat ID setup ({})'.format(TV_DEFAULT['chat-id']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

def process_input_file_argument(parser, options):
    global TV_DEFAULT
    log.debug('')
    file_path = options.input_file_path
    if file_path == None:
        log.warning(
            'No input file provided. Defaulting to ({}).'\
            .format(TV_DEFAULT['input-file'])
        )
        return False
    TV_DEFAULT['input-file'] = file_path
    stdout_msg(
        'Input file setup ({})'.format(TV_DEFAULT['input-file']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

def process_action_argument(parser, options):
    global TV_DEFAULT
    log.debug('')
    action = options.action
    if action == None:
        log.warning(
            'No action label provided. Defaulting to ({}).'\
            .format(TV_DEFAULT['action'])
        )
        return False
    TV_DEFAULT['action'] = action
    stdout_msg(
        'Action setup ({})'.format(TV_DEFAULT['action']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

def process_message_argument(parser, options):
    global TV_DEFAULT
    log.debug('')
    msg = options.message
    if msg == None:
        log.warning(
            'No message provided. Defaulting to ({}).'\
            .format(TV_DEFAULT['message'])
        )
        return False
    TV_DEFAULT['message'] = msg
    stdout_msg(
        'Message setup ({})'.format(TV_DEFAULT['message']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

def process_bot_token_argument(parser, options):
    global TV_DEFAULT
    log.debug('')
    room = options.bot_token_id
    if room == None:
        log.warning(
            'No bot token provided. Defaulting to ({}).'\
            .format(TV_DEFAULT['bot-token'])
        )
        return False
    TV_DEFAULT['bot-token'] = room
    stdout_msg(
        'Bot Token setup ({})'.format(TV_DEFAULT['bot-token']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

def process_silence_argument(parser, options):
    global TV_DEFAULT
    log.debug('')
    flag = options.silence_flag
    if flag == None:
        log.warning(
            'No silence flag provided. Defaulting to ({}).'\
            .format(TV_DEFAULT['watchdog'])
        )
        return False
    TV_DEFAULT['silence'] = flag
    stdout_msg(
        'Silence FLAG setup ({})'.format(TV_DEFAULT['silence']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

def process_watchdog_argument(parser, options):
    global TV_DEFAULT
    log.debug('')
    flag = options.watchdog_flag
    if flag == None:
        log.warning(
            'No watchdog flag provided. Defaulting to ({}).'\
            .format(TV_DEFAULT['watchdog'])
        )
        return False
    TV_DEFAULT['watchdog'] = flag
    stdout_msg(
        'Watchdog FLAG setup ({})'.format(TV_DEFAULT['watchdog']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

def process_config_file_argument(parser, options):
    global TV_DEFAULT
    log.debug('')
    file_path = options.config_file_path
    if file_path == None:
        log.warning(
            'No config file provided. Defaulting to ({}).'\
            .format(TV_DEFAULT['conf-file'])
        )
        return False
    TV_DEFAULT['conf-file'] = file_path
    # NOTE: You must load_config_json() after setting a new config file path in
    #       order to benefit of the new configuration.
    stdout_msg(
        'Loading config file...', info=True, silence=TV_DEFAULT['silence']
    )
    config_setup = load_config_json()
    if not config_setup:
        stdout_msg(
            'Could not load config file!',
            warn=True, silence=TV_DEFAULT['silence']
        )
    stdout_msg(
        'Config file setup ({})'.format(TV_DEFAULT['conf-file']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

def process_debug_mode_argument(parser, options):
    global TV_DEFAULT
    log.debug('')
    debug_mode = options.debug_flag
    if debug_mode == None:
        log.warning(
            'Debug mode flag not specified. '
            'Defaulting to ({}).'.format(TV_DEFAULT['debug'])
        )
        return False
    TV_DEFAULT['debug'] = debug_mode
    stdout_msg(
        'Debug mode setup ({})'.format(TV_DEFAULT['debug']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

def process_log_file_argument(parser, options):
    global TV_DEFAULT
    log.debug('')
    file_path = options.log_file_path
    if file_path == None:
        log.warning(
            'No log file provided. Defaulting to ({}).'\
            .format(TV_DEFAULT['log-file'])
        )
        return False
    TV_DEFAULT['log-file'] = file_path
    stdout_msg(
        'Log file setup ({})'.format(TV_DEFAULT['log-file']),
        ok=True, silence=TV_DEFAULT['silence']
    )
    return True

# PARSERS

def add_command_line_parser_options(parser):
    log.debug('')
    parser.add_option(
        '-c', '--config-file', dest='config_file_path', type='string',
        help='Configuration file to load default values from.',
        metavar='FILE_PATH'
    )
    parser.add_option(
        '-D', '--debug', dest='debug_flag', action='store_true',
        help='Display more verbose output and log messages.'
    )
    parser.add_option(
        '-l', '--log-file', dest='log_file_path', type='string',
        help='Path to the log file.', metavar='FILE_PATH'
    )
    parser.add_option(
        '-a', '--action', dest='action', type='string',
        help='Action to execute. '\
        'Values can be (scroll-msg|scroll-file|bot-ctrl)',
        metavar='ACTION'
    )
    parser.add_option(
        '-t', '--bot-token', dest='bot_token_id', type='string',
        help='String token the Telegram @BotFather gave you for your /newbot.',
        metavar='TOKEN'
    )
    parser.add_option(
        '-i', '--chat-id', dest='chat_id', type='string',
        help='Chat ID for your Telegram bot. You can ask @RawDataBot what it is.',
        metavar='ID'
    )
    parser.add_option(
        '-f', '--input-file', dest='input_file_path', type='string',
        help='Path to file to read and redirect content.', metavar='PATH_CSV'
    )
    parser.add_option(
        '-w', '--watchdog', dest='watchdog_flag', action='store_true',
        help='Makes --action scroll-msg open an interactive prompt for the user '\
        'to continuously write messages, and scroll-file to continuously read '\
        'file and redirect new lines to chat.',
    )
    parser.add_option(
        '-m', '--message', dest='message', type='string',
        help='Implies --action scroll-msg. Message to send.', metavar='MSG'
    )
    parser.add_option(
        '-S', '--silence', dest='silence_flag', action='store_true',
        help='Supress STDOUT output.',
    )

def parse_command_line_arguments():
    log.debug('')
    parser = create_command_line_parser()
    add_command_line_parser_options(parser)
    return process_command_line_options(parser)

# INIT

#@pysnooper.snoop()
def init_television(**kwargs):
    log.debug('')
    display_header()
    check = check_preconditions(**kwargs)
    if not isinstance(check, int) or check != 0:
        stdout_msg(
            'Preconditions not met!', err=True, silence=TV_DEFAULT['silence']
        )
        return check
    bot = create_telegram_bot(**kwargs)
    if not bot:
        stdout_msg(
            'Something went wrong! Could not set up Telegram bot.',
            err=True, silence=TV_DEFAULT['silence']
        )
        return 1
    handle = handle_actions(kwargs['action'], **kwargs)
    exit_code = 0 if ((isinstance(handle, int) and handle == 0) or handle) else 1
    return exit_code

# MISCELLANEOUS

if __name__ == '__main__':
    parse_command_line_arguments()
    if not update_log():
        stdout_msg(
            'Could not properly setup logger!',
            warn=True, silence=TV_DEFAULT['silence']
        )
    # NOTE: Import and Bot init moved here for optimisation of --help exec time
    from src.telegram_bot import TelegramBot
    bot = create_telegram_bot(**TV_DEFAULT)
    clear_screen()
    EXIT_CODE = 1
    try:
        EXIT_CODE = init_television(**TV_DEFAULT)
    finally:
        cleanup()
    stdout_msg(
        'Terminating! ({})\n'.format(EXIT_CODE),
        done=True, silence=TV_DEFAULT['silence']
    )
    exit(EXIT_CODE)

# CODE DUMP


