"""
    `operations.py`
"""

from src.data import extract, get_processed_data
from src.loaders import load_default_style
from src.render import render
from src.stats import average, median, standard_dev, progress_coverage
from src.utils import error, notice, level_format

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
    """ Function: Operation Code 'C' (Create Charts) """
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

    # Step 3: -incorrect-p argument
    if '-inc-p' in args:
        # Step 3.1 - Test for valid format
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

    # Step 4: -max-y argument
    if '-max-y' in args:
        # Step 4.1 - Test for valid format
        try:
            max_y_labels = int(args[args.index('-max-y') + 1])
        except (IndexError, ValueError):
            error('Maximum y labels must be an integer.')
            error('Aborting chart creation process.')
            return

        # Step 4.2 - Test for valid requirements
        if not (max_y_labels >= 2):
            error('Maximum y labels must be an integer at least 2.')
            error('Aborting chart creation process.')
            return
    else:
        max_y_labels = 15

    # Step 5: -style argument
    if '-style' in args:
        # Step 5.1.1 - Test for valid format
        try:
            style = args[args.index('-style') + 1]
        except (IndexError, ValueError):
            error('Invalid style.')
            error('Aborting chart creation process.')
            return

        # Step 5.1.2 - Test for valid requirements
        if style not in STYLES:
            error('Invalid style.')
            error('Aborting chart creation process.')
            return
    elif load_default_style():
        style = load_default_style().strip()

        # Step 5.2.1 - Test for valid requirements
        if style not in STYLES:
            error('Invalid style found in \'DEFAULT_STYLE.txt\'.')
            error('Aborting chart creation process.')
            return

        notice('File \'DEFAULT_STYLE.txt\' is found. Now proceeding to chart creation.')
        notice('Style \'{}\' will be used in chart creation.'.format(style))
    else:
        style = 'DefaultStyle'

    # Step 6: Rendering
    render(
        get_processed_data(),
        days=days,
        dot_shrink=('-no-dot-shrink' not in args),
        incorrect_p=incorrect_p,
        max_y_labels=max_y_labels,
        show_correlation=('-show-correl' in args),
        simulation_mode=('-simulate' in args),
        style=style
    )

    # Step 7: -open argument
    if '-open' in args:
        try:
            os.system('open charts/*')
            notice('Opening chart files.')
        except (FileNotFoundError, OSError, PermissionError):
            error('Something unexpected happened, please try again.')


def operate_extract(raw_data, args):
    """ Function: Operation Code 'E' (Extract) """
    extract()


def operate_stat(raw_data, args):
    """ Function: Operation Code 'S' (View Statistics) """
    j = 0
    for i in ('word', 'kanji'):
        print(' - {} Statistics -'.format(i.capitalize()))
        print('   Total: {}'.format(len(raw_data[i])))
        print('   Median: {}'.format(level_format(median(raw_data[i]), initial_level=1, remainder=True)))
        print('   Average: {}'.format(level_format(average(raw_data[i]), initial_level=1, remainder=True)))
        print('   Standard Deviation: {}'.format(level_format(standard_dev(raw_data[i]), initial_level=0, remainder=True)))
        print('   Progress Coverage: {:.2f}%'.format(progress_coverage(raw_data[i]) * 100))

        if j + 1 < 2:
            print()
            j += 1


def operate_exit(raw_data, args):
    """ Function: Operation Code 'X' (Exit) """
    notice('Exitting application.')
    print()
    exit()
