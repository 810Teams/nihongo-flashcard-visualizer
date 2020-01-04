'''
    `operations.py`
'''

from src.data import extract
from src.data import get_processed_data
from src.loaders import load_default_style
from src.render import render
from src.statistics import average
from src.statistics import median
from src.statistics import standard_dev
from src.statistics import progress_ratio
from src.utils import error
from src.utils import notice
from src.utils import level_format

import os

STYLES = (
    'DefaultStyle',
    'DarkStyle',
    'NeonStyle',
    'DarkSolarizedStyle',
    'LightSolarizedStyle',
    'LightStyle',
    'CleanStyle',
    'RedBlueStyle',
    'DarkColorizedStyle',
    'LightColorizedStyle',
    'TurquoiseStyle',
    'LightGreenStyle',
    'DarkGreenStyle',
    'DarkGreenBlueStyle',
    'BlueStyle'
)


class Operation:
    def __init__(self, code, command, title, args):
        self.code = code
        self.command = command
        self.title = title
        self.args = args
    
    def operate(self, raw_data, args):
        try:
            eval('operate_{}(raw_data, args)'.format(self.command.lower()))
        except (NameError, SyntaxError):
            error('Invalid action. Please try again.')


class Argument:
    def __init__(self, name, description):
        self.name = name
        self.description = description


def operate_chart(raw_data, args):
    ''' Function: Operation Code 'C' (Create Charts) '''
    # Step 1: -open-only argument
    if '-open-only' in args:
        try:
            os.system('open charts/*')
            notice('Opening chart files.')
        except (FileNotFoundError, OSError, PermissionError):
            error('Something unexpected happened, please try again.')
        return

    # Step 2: -days argument
    if '-days' in args:
        # Test for valid format
        try:
            days = int(args[args.index('-days') + 1])
            if days < 2:
                error('Days value must be an integer at least 2.')
                error('Aborting chart creation process.')
                return
        except (IndexError, ValueError):
            error('Days value must be an integer.')
            error('Aborting chart creation process.')
            return
    else:
        days = 60

    # Step 3: -dot_shrink argument
    if '-dot-shrink' in args:
        # Test for valid format
        dot_shrink = args[args.index('-dot-shrink') + 1]

        if dot_shrink.lower().lstrip('0') in ['true', 'yes', '1']:
            dot_shrink = True
        elif dot_shrink.lower().lstrip('0') in ['false', 'no', '0']:
            dot_shrink = False
        else:
            error('Dots shrinking value must be \'false\', \'true\', \'no\', \'yes\', 0, or 1')
            error('Aborting chart creation process.')
            return
    else:
        dot_shrink = True
    
    # Step 4: -incorrect-p argument
    if '-inc-p' in args:
        # Step 4.1 - Test for valid format
        try:
            incorrect_p = float(args[args.index('-inc-p') + 1])
            if (incorrect_p < 0) or (1 < incorrect_p):
                error('Incorrect probability value must be a real number from 0 to 1.')
                error('Aborting chart creation process.')
                return
        except (IndexError, ValueError):
            error('Incorrect probability value must be a real number.')
            error('Aborting chart creation process.')
            return
    else:
        incorrect_p = 0.0
    
    # Step 5: -max-y argument
    if '-max-y' in args:
        # Step 5.1 - Test for valid format
        try:
            max_y_labels = int(args[args.index('-max-y') + 1])
        except (IndexError, ValueError):
            error('Maximum y labels must be an integer.')
            error('Aborting chart creation process.')
            return
        
        # Step 5.2 - Test for valid requirements
        if not (max_y_labels >= 2):
            error('Maximum y labels must be an integer at least 2.')
            error('Aborting chart creation process.')
            return
    else:
        max_y_labels = 15

    # Step 6: -style argument
    if '-style' in args:
        # Step 6.1.1 - Test for valid format
        try:
            style = args[args.index('-style') + 1]
        except (IndexError, ValueError):
            error('Invalid style.')
            error('Aborting chart creation process.')
            return

        # Step 6.1.2 - Test for valid requirements
        if style not in STYLES:
            error('Invalid style.')
            error('Aborting chart creation process.')
            return
    elif load_default_style():
        style = load_default_style().strip()

        # Step 6.2.1 - Test for valid requirements
        if style not in STYLES:
            error('Invalid style found in \'DEFAULT_STYLE.txt\'.')
            error('Aborting chart creation process.')
            return

        notice('File \'DEFAULT_STYLE.txt\' is found. Now proceeding to chart creation.')
        notice('Style \'{}\' will be used in chart creation.'.format(style))
    else:
        style = 'DefaultStyle'
    
    # Step 7: Rendering
    render(get_processed_data(), days=days, dot_shrink=dot_shrink, incorrect_p=incorrect_p, max_y_labels=max_y_labels, style=style)
    
    # Step 8: -open argument
    if '-open' in args:
        try:
            os.system('open charts/*')
            notice('Opening chart files.')
        except (FileNotFoundError, OSError, PermissionError):
            error('Something unexpected happened, please try again.')


def operate_extract(raw_data, args):
    ''' Function: Operation Code 'E' (Extract) '''
    extract()


def operate_stat(raw_data, args):
    ''' Function: Operation Code 'S' (View Statistics) '''
    notice('Total: {}'.format(len(raw_data)))
    notice('Median: {}'.format(level_format(median(raw_data), initial_level=1, remainder=True)))
    notice('Average: {}'.format(level_format(average(raw_data), initial_level=1, remainder=True)))
    notice('Standard Deviation: {}'.format(level_format(standard_dev(raw_data), initial_level=0, remainder=True)))
    notice('Progress Ratio: {:.2f}%'.format(progress_ratio(raw_data) * 100))


def operate_exit(raw_data, args):
    ''' Function: Operation Code 'X' (Exit) '''
    notice('Exitting application.')
    print()
    exit()
