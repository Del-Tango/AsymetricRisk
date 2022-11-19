#!/usr/bin/python3
#
# Regards, the Alveare Solutions #!/Society -x
#
# CHECKERS

import os
import stat
import logging

log = logging.getLogger('AsymetricRisk')


def check_pid_running(pid):
    '''
    [ NOTE ]: Sending signal 0 to a PID will raise an OSError exception if the
              PID is not running and do nothing otherwise.
    '''
    log.debug('')
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def check_superuser():
    log.debug('')
    return False if os.geteuid() != 0 else True


def check_is_fifo(fifo_path):
    log.debug('')
    try:
        return stat.S_ISFIFO(os.stat(fifo_path).st_mode)
    except Exception as e:
        log.error(e)
        return None


def check_file_exists(file_path):
    log.debug('')
    try:
        return os.path.exists(file_path)
    except Exception as e:
        log.error(e)
        return None


