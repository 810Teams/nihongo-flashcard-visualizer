'''
    Nihongo - Japanese Dictionary Application
    Flashcard Progress Visualizer

    by Teerapat Kraisrisirikul
'''

from math import ceil
from math import floor
from math import sqrt

from src.data import get_raw_data
from src.operations import Operation
from src.operations import Argument
from src.operations import operate_chart
from src.operations import operate_extract
from src.operations import operate_stat
from src.operations import operate_exit
from src.render import render
from src.statistics import average
from src.statistics import median
from src.statistics import standard_dev
from src.utils import error
from src.utils import notice
from src.utils import level_format

import os


APP_NAME = 'Nihongo Flashcard Visualizer'
AUTHOR = '810Teams'
VERSION = 'v1.1.1'
OPERATIONS = [
    Operation('c', 'chart', 'Create Charts', [
        Argument('-days INTEGER', 'Duration (Default: All)'),
        Argument('-max-y INTEGER', 'Maximum y-labels (Default: 15)'),
        Argument('-incorrect-p NUMBER', 'Incorrect probability'),
        Argument('-style STYLE_NAME', 'Style'),
        Argument('-open', 'Open'),
        Argument('-open-only', 'Open Only'),
    ]),
    Operation('e', 'extract', 'Extract SQLite file', []),
    Operation('s', 'stat', 'View Statistics', []),
    Operation('x', 'exit', 'Exit Application', []),
]


def main():
    ''' Main Function '''
    run_check()
    show_app_title()
    show_operations()
    start_operating()


def run_check():
    ''' Function: Run checking '''
    if not os.path.exists('NihongoBackup.nihongodata'):
        print()
        error('Nihongo backup file not found. Unable to start application.')
        print()
        exit()


def show_app_title():
    ''' Function: Show application title '''
    print()
    print('- {} -'.format(APP_NAME))
    print(('by {} ({})'.format(AUTHOR, VERSION)).center(len(APP_NAME) + 4))


def show_operations():
    ''' Function: Show operation list '''
    print()
    print('- Operation List -')

    for i in OPERATIONS:
        print('[{}]'.format(i.command))
        for j in i.args:
            print('    {}{}: {}'.format(j.name, ' ' * (max([len(k.name) for k in i.args]) - len(j.name) + 1), j.description))


def start_operating():
    ''' Function: Start operating application '''
    while True:
        print()
        try:
            action = [i for i in input('(Command) ').split()]
            print()
            operate(action[0].lower(), action[1:])
        except IndexError:
            error('Invalid action format. Please try again.')


def operate(action, args):
    ''' Function: Operate a specific action '''
    try:
        eval('operate_{}(get_raw_data(), args)'.format(action.lower()))
    except (NameError, SyntaxError):
        try:
            eval('operate_{}(get_raw_data(), args)'.format([i.command for i in OPERATIONS if i.code == action.lower()][0]))
        except (IndexError, NameError, SyntaxError): 
            error('Invalid action. Please try again.')


main()
