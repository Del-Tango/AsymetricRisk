#!/usr/bin/python3
#
# Regards, the Alveare Solutions #!/Society -x
#
# CHECKERS

import os
import stat
import logging
#import pysnooper

log = logging.getLogger('AsymetricRisk')


# @pysnooper.snoop()
def check_value_set_convergence(values1, values2):
    log.debug('')
    if len(values1) != len(values2):
        return False
    return_dict = {
        'flag': False,
        'start1': values1[0],
        'start2': values2[0],
        'end1': values1[len(values1)-1],
        'end2': values2[len(values2)-1],
        'direction1': '',
        'direction2': ''
    }

    crossover = check_value_set_crossover(values1, values2)

    if return_dict['start1'] < return_dict['end1']:
        return_dict['direction1'] = 'up'
    elif return_dict['start1'] > return_dict['end1']:
        return_dict['direction1'] = 'down'

    if return_dict['start2'] < return_dict['end2']:
        return_dict['direction2'] = 'up'
    elif return_dict['start2'] > return_dict['end2']:
        return_dict['direction2'] = 'down'

    if return_dict['direction1'] == 'down' \
            and return_dict['direction2'] == 'up' \
            and return_dict['start1'] > return_dict['start2'] \
            and not crossover:
        return_dict['flag'] = True

    if return_dict['direction1'] == 'up' \
            and return_dict['direction2'] == 'down' \
            and return_dict['start1'] < return_dict['start2'] \
            and not crossover:
        return_dict['flag'] = True

    return return_dict


# @pysnooper.snoop()
def check_value_set_divergence(values1, values2):
    log.debug('')
    if len(values1) != len(values2):
        return False
    return_dict = {
        'flag': False,
        'start1': values1[0],
        'start2': values2[0],
        'end1': values1[len(values1)-1],
        'end2': values2[len(values2)-1],
        'direction1': '',
        'direction2': ''
    }

    crossover = check_value_set_crossover(values1, values2)

    if return_dict['start1'] < return_dict['end1']:
        return_dict['direction1'] = 'up'
    elif return_dict['start1'] > return_dict['end1']:
        return_dict['direction1'] = 'down'

    if return_dict['start2'] < return_dict['end2']:
        return_dict['direction2'] = 'up'
    elif return_dict['start2'] > return_dict['end2']:
        return_dict['direction2'] = 'down'

    if return_dict['direction1'] == 'up' \
            and return_dict['direction2'] == 'down' \
            and return_dict['start1'] > return_dict['start2'] \
            and not crossover:
        return_dict['flag'] = True

    if return_dict['direction1'] == 'down' \
            and return_dict['direction2'] == 'up' \
            and return_dict['start1'] < return_dict['start2'] \
            and not crossover:
        return_dict['flag'] = True

    return return_dict


# @pysnooper.snoop()
def check_value_set_crossover(values1, values2):
    '''
    [ INPUT ]: [1,2,3,4,5], [5,4,3,2,1]

    [ RETURN ]: {
        'flag': True,           # Crossover detected
        'start1': 3,            # values1[0] value
        'start2': 1,            # values2[0] value
        'end1': 2,              # values1[len(values1)-1] value
        'end2': 15,             # values2[len(values2)-1] value
        'crossovers': [5, 7],   # List of positions where crossovers occur (indexes)
        'confirmed': True       # If after a crossover values continuously increase
        'direction1': 'down',
        'direction2': 'up',
    }
    '''
    log.debug('')
    if len(values1) != len(values2):
        return False

    return_dict = {
        'flag': False,
        'start1': values1[0],
        'start2': values2[0],
        'end1': values1[len(values1)-1],
        'end2': values2[len(values2)-1],
        'crossovers': [],
        'confirmed': False,
        'direction1': '',
        'direction2': ''
    }

    if return_dict['start1'] < return_dict['end1']:
        return_dict['direction1'] = 'up'
    elif return_dict['start1'] > return_dict['end1']:
        return_dict['direction1'] = 'down'

    if return_dict['start2'] < return_dict['end2']:
        return_dict['direction2'] = 'up'
    elif return_dict['start2'] > return_dict['end2']:
        return_dict['direction2'] = 'down'

    old_val1, old_val2, confirmed = None, None, 0
    for index in range(len(values1)):
        val1, val2 = values1[index], values2[index]
        if val1 == val2:
            if not return_dict['flag']:
                return_dict.update({
                    'flag': True,
                    'crossovers': return_dict['crossovers'] + [index],
                }) #['flag'] = True
            continue
        elif val1 > val2 \
                and val1 > return_dict['start1'] and val1 > old_val1:
            confirmed += 1
        elif val1 < val2 \
                and val2 > return_dict['start2'] and val2 > old_val2:
            confirmed += 1
        old_val1, old_val2 = val1, val2
    return_dict['confirmed'] = False if not confirmed else True
    return return_dict


def check_majority_in_set(value, value_set):
    log.debug('')
    counter = len([item for item in value_set if item == value])
    return True if counter >= (len(value_set) / 2) else False


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


