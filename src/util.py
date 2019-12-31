from math import floor

def level_format(level_value, initial_level=1):
    ''' Function: Get a level format from a level value '''
    return '{:.0f}-{:.0f} (+{:.2f})'.format(level_value // 3 + initial_level, floor(level_value % 3), level_value % 1)
