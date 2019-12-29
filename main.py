'''
    Nihongo - Japanese Dictionary Application
    Flashcard Progress Visualizer

    by Teerapat Kraisrisirikul
'''

from math import ceil
from math import floor
from math import sqrt
from pygal.style import DefaultStyle
from pygal.style import DarkStyle
from pygal.style import NeonStyle
from pygal.style import DarkSolarizedStyle
from pygal.style import LightSolarizedStyle
from pygal.style import LightStyle
from pygal.style import CleanStyle
from pygal.style import RedBlueStyle
from pygal.style import DarkColorizedStyle
from pygal.style import LightColorizedStyle
from pygal.style import TurquoiseStyle
from pygal.style import LightGreenStyle
from pygal.style import DarkGreenStyle
from pygal.style import DarkGreenBlueStyle
from pygal.style import BlueStyle

import os
import pygal
import sqlite3


DATABASE_CONTAINER = 'NihongoBackup.nihongodata'
DATABASE_FILE = 'Flashcards.sqlite'
VERSION = 'v0.9.1'


def main():
    ''' Function: Main function '''
    extract()

    raw_data = sorted(get_progress(create_connection()))
    data = [raw_data.count(i) for i in range(0, max(raw_data) + 1)]
    review = [sum(i) for i in estimated(data, days=365)]
    print(review)

    # render(data)

    print()
    print('-- Flashcard Statistics --')
    print()
    print(' - General Stats -')
    print()
    print('   Total: {}'.format(len(raw_data)))
    print('   Median: {}'.format(level_format(median(raw_data), initial_level=1)))
    print('   Average: {}'.format(level_format(average(raw_data), initial_level=1)))
    print('   Standard Deviation: {}'.format(level_format(standard_dev(raw_data), initial_level=0)))
    print()
    print(' - Level Stats -')
    print()

    for i in range(len(data) - 1, -1, -1):
        print('   Level {}-{}: {} ({:.2f}%)'.format(i // 3 + 1, i % 3, data[i], data[i] / sum(data) * 100))

    print()
    print(' - Estimated Flashcard Reviews -')
    print()
    print('   {:4d} day: {:.0f} ({:.2f}%)'.format(1, review[0], review[0] / len(raw_data) * 100))

    for i in (2, 3, 4, 5, 6, 7, 14, 21, 30, 60, 90, 180, 270, 365):
        print('   {:3d} days: {:.0f} ({:.2f}%)'.format(i, review[i - 1], review[i - 1] / len(raw_data) * 100))

    print()


def extract():
    ''' Function: Extracts database file from the zip '''
    try:
        os.system('unzip -o {}/{}.zip'.format(DATABASE_CONTAINER, DATABASE_FILE))
    except (FileNotFoundError, OSError, PermissionError):
        print('[ERROR] Extraction error.')


def create_connection():
    ''' Function: Creates the database connection '''
    conn = None
    try:
        conn = sqlite3.connect('{}'.format(DATABASE_FILE))
    except:
        print('[ERROR] Database connection error.')

    return conn


def get_progress(conn):
    ''' Function: Gets flashcard progress from database '''
    cur = conn.cursor()
    cur.execute('SELECT ZPROGRESS, Z8_BECAMEACTIVEVIAFLASHCARDPACK FROM ZFLASHCARD')

    return [i[0] for i in cur.fetchall() if i[1] != None]


def level_format(level_value, initial_level=1):
    ''' Function: Get a level format from a level value '''
    return '{:.0f}-{:.0f} (+{:.2f})'.format(level_value // 3 + initial_level, floor(level_value % 3), level_value % 1)


def median(raw_data):
    ''' Function: Calculates median '''
    raw_data_copy = sorted([i for i in raw_data])
    if len(raw_data_copy) % 2 == 0:
        return (raw_data_copy[len(raw_data_copy) // 2 - 1] + raw_data_copy[len(raw_data_copy) // 2]) / 2
    return raw_data_copy[len(raw_data_copy) // 2]


def average(raw_data):
    ''' Function: Calculates average '''
    return sum(raw_data) / len(raw_data)


def standard_dev(raw_data):
    ''' Function: Calculates standard deviation '''
    return sqrt(sum([(i - average(raw_data)) ** 2 for i in raw_data])/len(raw_data))


def estimated(data, days=1):
    ''' Function: Calculates estimated flashcards per day '''
    level_weight = 1, 2, 3, 7, 14, 21, 30, 60, 90, 180, 270, 360, None          # Level weight
    data_copy = [i for i in data] + [0] * (13 - len(data))                      # A copy of data
    last_subtractor = [data_copy[i] / level_weight[i] for i in range(12)] + [0] # Lastest subtractor
    is_added = [False for _ in range(13)]                                       # Is added

    reviewed = list()

    for _ in range(days):
        reviewed.append([0 for _ in range(12)])

        for i in range(1, 12):
            if is_added[i]:
                last_subtractor[i] = data_copy[i] / level_weight[i]
                is_added[i] = False
        
        for i in range(12):
            subtractor = max(min(last_subtractor[i], data_copy[i]), 0) # Purpose: To limit the subtractor and prevent references
            data_copy[i] -= subtractor

            # Condition: Check if a cell reaches zero
            if data_copy[i] == 0:
                last_subtractor[i] = 0

            # Condition: Check if a cell is actually reduced to the lower integer completely
            if ceil(data_copy[i]) != ceil(data_copy[i] + subtractor):
                reviewed[-1][i] = abs(ceil(data_copy[i]) - ceil(data_copy[i] + subtractor))
                data_copy[i + 1] += abs(ceil(data_copy[i]) - ceil(data_copy[i] + subtractor))
                is_added[i + 1] = True
    
    return reviewed


def render(data):
    ''' Function: Renders the chart '''
    chart = pygal.HorizontalBar()

    # Chart Data
    chart.add('Learned Words', data)

    # Chart Titles
    chart.title = 'Learned Words by Level'

    # Chart Data
    chart.x_labels = ['{}-{}'.format(i // 3 + 1, i % 3) for i in range(len(data))]
    chart.y_labels = y_labels(min(data), max(data))
    
    # Chart Legends
    chart.show_legend = False

    # Chart Render
    chart.style = DarkStyle
    chart.render_to_file('chart.svg')

    # Chart Open
    try:
        os.system('open chart.svg')
    except (FileNotFoundError, OSError, PermissionError):
        print('[ERROR] Chart file opening error.')


def y_labels(data_min, data_max, max_y_labels=15):
    ''' Function: Calculates y labels of the chart '''
    data_min = floor(data_min)
    data_max = ceil(data_max)
    
    preset = 1, 2, 5
    data_range = list(range(0, data_min - 1, -1)) + list(range(0, data_max + 1, 1))
    i = 0

    while len(data_range) > max_y_labels:
        data_range = list(range(0, data_min - preset[i % 3] * 10 ** (i // 3), -1 * preset[i % 3] * 10 ** (i // 3)))
        data_range += list(range(0, data_max + preset[i % 3] * 10 ** (i // 3), preset[i % 3] * 10 ** (i // 3)))
        i += 1
        
    data_range.sort()

    return data_range


main()
