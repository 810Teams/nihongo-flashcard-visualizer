'''
    Nihongo - Japanese Dictionary Application
    Flashcard Progress Visualizer

    by Teerapat Kraisrisirikul
'''

from math import ceil
from math import floor
from math import sqrt

from src.extract import create_connection
from src.extract import extract
from src.extract import get_progress
from src.render import render
from src.statistics import average
from src.statistics import median
from src.statistics import standard_dev
from src.util import level_format

VERSION = 'pre1.0.0-e'


def main():
    ''' Function: Main function '''
    extract()

    raw_data = sorted(get_progress(create_connection()))
    data = [raw_data.count(i) for i in range(0, max(raw_data) + 1)]

    render(data, days=120)

    print()
    print('-- Flashcard Statistics --')
    print()
    print(' - General Stats -')
    print()
    print('   Total: {}'.format(len(raw_data)))
    print()
    print('   Median: {}'.format(level_format(median(raw_data), initial_level=1)))
    print('   Average: {}'.format(level_format(average(raw_data), initial_level=1)))
    print('   Standard Deviation: {}'.format(level_format(standard_dev(raw_data), initial_level=0)))
    print()
    print(' - Level Stats -')
    print()

    for i in range(len(data) - 1, -1, -1):
        print('   Level {}-{}: {} ({:.2f}%)'.format(i // 3 + 1, i % 3, data[i], data[i] / sum(data) * 100))

    print()


main()
