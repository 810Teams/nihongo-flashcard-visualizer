'''
    `utils.py`
'''

from math import floor


def error(message, show=True, end='\n'):
    ''' Display error message '''
    if show:
        print('[ERROR]', message, end=end)


def log(message, show=True, end='\n'):
    ''' Display log message '''
    if show:
        print('[LOG]', message, end=end)


def notice(message, show=True, end='\n'):
    ''' Display notice message '''
    if show:
        print('[NOTICE]', message, end=end)


def level_format(level_value, initial_level=1, remainder=False):
    ''' Function: Get a level format from a level value '''
    return '{:.0f}-{:.0f}'.format(level_value // 3 + initial_level, floor(level_value % 3)) + ' (+{:.2f})'.format(level_value % 1) * remainder
