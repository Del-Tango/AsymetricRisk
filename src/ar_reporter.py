#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADING REPORTER

import string
import logging
import pysnooper

from src.backpack.bp_generators import generate_msg_id
from src.backpack.bp_ensurance import ensure_directories_exist
from src.backpack.bp_checkers import check_file_exists

log = logging.getLogger('AsymetricRisk')


#@pysnooper.snoop()
class TradingReporter():

#   @pysnooper.snoop()
    def __init__(self, *args, **kwargs):
        log.debug('')
        self.prefix = kwargs.get('report-prefix', 'ar-')
        self.suffix = kwargs.get('report-suffix', '')
        self.extension = kwargs.get('report-extension', 'report')
        self.id_length = int(kwargs.get('report-id-length', 8))
        self.id_characters = list(kwargs.get(
            'report-id-characters', string.ascii_letters + string.digits
        ))
        self.location = kwargs.get('report-location', './data/reports')
        if not check_file_exists(self.location):
            ensure_directories_exist(self.location)
        self.identifier = kwargs.get(
            'report-id', generate_msg_id(self.id_length, self.id_characters)
        )

    # INTERFACE

    # TODO
    def list(self, *args, **kwargs):
        '''
        [ NOTE ]: Lists existing reports.
        '''
        log.debug('TODO - Under construction, building...')
    def remove(self, *args, **kwargs):
        '''
        [ NOTE ]: Deletes specified report files.
        '''
        log.debug('TODO - Under construction, building...')
    def read(self, *args, **kwargs):
        '''
        [ NOTE ]: Displays the content of an existing report.
        '''
        log.debug('TODO - Under construction, building...')

    @pysnooper.snoop()
    def generate(self, *args, **kwargs):
        '''
        [ NOTE ]: High level interface function for report generation. Currently
                  supports trade history reports, current (active) trades and
                  success rate.

        [ INPUT ]: *args - (<report-type>, ...)

                   **kwargs - {
                        ...
                        'evaluation': {
                            'buy': {},
                            'sell': {},
                        },
                        ...
                   }

        [ RETURN ]: {
            'flag': False,
            'reports': {
                'trade-history': {
                    'timestamp': '',
                    'report-id': '',
                    'report-type': '',
                    'report-location': '',
                },
                'current-trades': {
                    'timestamp': '',
                    ...
                },
                'success-rate': {
                    'timestamp': '',
                    ...
                },
            }
            'errors': [{msg: '', type: '', code: ,}],
        }
        '''
        log.debug('')
        report_types = {
            'trade-history': self.generate_trade_history_report,
            'current-trades': self.generate_current_trades_report,
            'success-rate': self.generate_success_rate_report,
        }
        return_dict = {
            'flag': False,
            'reports': {
                'trade-history': {
                    'timestamp': '',
                    'report-id': '',
                    'report-type': '',
                    'report-location': '',
                },
                'current-trades': {},
                'success-rate': {},
            },
            'errors': [],
        }
        for label in args:
            if label not in report_types.keys():
                continue
            generate = report_types[label](**kwargs)
            if generate and isinstance(generate, dict):
                return_dict['reports'][label].update(generate)
            else:
                return_dict['errors'].append({
                    'msg': 'Could not generate {} report!'.format(label),
                    'type': 'Reporter High Level ERROR',
                    'code': 10,
                    'details': generate,
                })
        return return_dict

# GENERATORS

    # TODO
    def generate_trade_history_report(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
        return_dict = {
            'timestamp': '',
            'report-id': '',
            'report-type': '',
            'report-location': '',
        }
    def generate_current_trades_report(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
        return_dict = {
            'timestamp': '',
            'report-id': '',
            'report-type': '',
            'report-location': '',
        }
    def generate_success_rate_report(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
        return_dict = {
            'timestamp': '',
            'report-id': '',
            'report-type': '',
            'report-location': '',
        }

# CODE DUMP














