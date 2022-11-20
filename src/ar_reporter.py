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


# TODO
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

    # TODO
    def read(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
    def generate(self, *args, **kwargs):
        # trade history
        # current trades
        # success rate
        log.debug('TODO - Under construction, building...')
    def list(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
    def remove(self, *args, **kwargs):
        log.debug('TODO - Under construction, building...')
