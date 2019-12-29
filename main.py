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
VERSION = 'pre1.0.0-b'


def main():
    ''' Function: Main function '''
    extract()

    raw_data = sorted(get_progress(create_connection()))
    data = [raw_data.count(i) for i in range(0, max(raw_data) + 1)]
    # review = [sum(i) for i in estimated(data, days=30)]

    render(data, days=180, learn_period=1, learn_each_period=10)

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
    # print(' - Estimated Flashcard Reviews -')
    # print()
    # print('   {:3d} day : {:.0f} ({:.2f}%)'.format(1, review[0], review[0] / len(raw_data) * 100))

    # for i in (2, 3, 7, 30):
    #     print('   {:3d} days: {:.0f} ({:.2f}%)'.format(i, review[i - 1], review[i - 1] / len(raw_data) * 100))
    
    # print()


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


def estimated(data, days=7, learn_period=1, learn_each_period=0, result='flashcard'):
    ''' Function: Calculates estimated flashcards per day '''
    level_weight = 1, 2, 3, 7, 14, 21, 30, 60, 90, 180, 270, 360, None          # Level weight
    data_copy = [i for i in data] + [0] * (13 - len(data))                      # A copy of data
    last_subtractor = [data_copy[i] / level_weight[i] for i in range(12)] + [0] # Lastest subtractor
    is_added = [False for _ in range(13)]                                       # Is added

    vocab_size = list()
    reviewed = list()

    for i in range(days):
        reviewed.append([0 for _ in range(12)])

        if i != 0 and i % learn_period == 0:
            data_copy[0] += learn_each_period
            is_added[0] = True

        for j in range(0, 12):
            if is_added[j]:
                last_subtractor[j] = data_copy[j] / level_weight[j]
                is_added[j] = False
        
        for j in range(12):
            subtractor = max(min(last_subtractor[j], data_copy[j]), 0) # Purpose: To limit the subtractor and prevent references
            data_copy[j] -= subtractor

            # Condition: Check if a cell reaches zero
            if data_copy[j] == 0:
                last_subtractor[j] = 0

            # Condition: Check if a cell is actually reduced to the lower integer completely
            if ceil(data_copy[j]) != ceil(data_copy[j] + subtractor):
                reviewed[-1][j] = abs(ceil(data_copy[j]) - ceil(data_copy[j] + subtractor))
                data_copy[j + 1] += abs(ceil(data_copy[j]) - ceil(data_copy[j] + subtractor))
                is_added[j + 1] = True
        
        vocab_size.append([ceil(j) for j in data_copy])
    
    if result == 'flashcard':
        return reviewed
    elif result == 'vocabulary':
        return vocab_size


def render(data, days=7, learn_period=1, learn_each_period=0):
    ''' Function: Renders the chart '''
    render_word_by_level(data)
    render_estimated(data, days=days, title='flashcard',  mode='single',   learn_period=learn_period, learn_each_period=learn_each_period)
    # render_estimated(data, days=days, title='flashcard',  mode='multiple', learn_period=learn_period, learn_each_period=learn_each_period)
    # render_estimated(data, days=days, title='flashcard',  mode='stacked',  learn_period=learn_period, learn_each_period=learn_each_period)
    # render_estimated(data, days=days, title='vocabulary', mode='single',   learn_period=learn_period, learn_each_period=learn_each_period)
    # render_estimated(data, days=days, title='vocabulary', mode='multiple', learn_period=learn_period, learn_each_period=learn_each_period)
    # render_estimated(data, days=days, title='vocabulary', mode='stacked',  learn_period=learn_period, learn_each_period=learn_each_period)
    
    # Chart Open
    try:
        os.system('open charts/*')
    except (FileNotFoundError, OSError, PermissionError):
        print('[ERROR] Chart file opening error.')


def render_word_by_level(data):
    ''' Function: Renders the word by level chart '''
    chart = pygal.HorizontalBar()

    # Chart Data
    chart.add('Learned Words', data)

    # Chart Titles
    chart.title = 'Learned Words by Level'

    # Chart Labels
    chart.x_labels = ['{}-{}'.format(i // 3 + 1, i % 3) for i in range(len(data))]
    chart.y_labels = y_labels(min(data), max(data))
    
    # Chart Legends
    chart.show_legend = False

    # Chart Render
    chart.style = DarkStyle
    chart.render_to_file('charts/words_by_level.svg')


def render_estimated(data, days=30, title='flashcard', mode='single', learn_period=1, learn_each_period=10):
    ''' Function: Renders the estimated chart '''
    if mode == 'single' or mode == 'multiple':
        chart = pygal.Line()
    elif mode == 'stacked':
        chart = pygal.StackedLine()
    else:
        return

    # Chart Data
    estimated_data = estimated(data, days=days, learn_period=learn_period, learn_each_period=learn_each_period, result=title)
    if mode == 'single':
        processed = [sum(i) for i in estimated_data]
        chart.add('Flashcards per day', processed)
    elif mode == 'multiple' or mode == 'stacked':
        processed = [[sum(j[i*3: i*3 + 3]) for j in estimated_data] for i in range(4)]
        for i in range(4):
            chart.add('Level {}'.format(i + 1), processed[i])

    # Chart Titles
    chart.title = 'Estimated Flashcards Per Day'
    chart.x_title = 'Days'

    # Chart Labels
    chart.x_labels = [i for i in range(1, days + 1)]
    chart.x_labels_major_count = 8
    chart.show_minor_x_labels = False

    if mode == 'single':
        chart.y_labels = y_labels(
            min([sum(i) for i in estimated_data]),
            max([sum(i) for i in estimated_data]),
            skip=True
        )
    elif mode == 'multiple':
        chart.y_labels = y_labels(
            min([min(processed[i]) for i in range(4)]),
            max([max(processed[i]) for i in range(4)]),
            skip=False
        )
    elif mode == 'stacked':
        chart.y_labels = y_labels(
            min([sum(estimated_data[i]) for i in range(12)]),
            max([sum(estimated_data[i]) for i in range(12)]),
            skip=False
        )

    chart.truncate_label = -1
    
    # Chart Legends
    if mode == 'single':
        chart.show_legend = False
    chart.legend_at_bottom = True
    chart.legend_at_bottom_columns = 4
    chart.legend_box_size = 16

    # Chart Interpolation
    chart.interpolate = 'cubic'

    # Chart Render
    if mode == 'stacked':
        chart.fill = True

    chart.style = DarkStyle
    chart.dots_size = 2
    chart.render_to_file('charts/estimated_{}_{}.svg'.format(title, mode))


def y_labels(data_min, data_max, max_y_labels=15, skip=False):
    ''' Function: Calculates y labels of the chart '''
    data_min = floor(data_min)
    data_max = ceil(data_max)
    
    preset = 1, 2, 5
    
    if not skip:
        data_range = list(range(0, data_min - 1, -1)) + list(range(0, data_max + 1, 1))
        i = 0

        while len(data_range) > max_y_labels:
            data_range = list(range(0, data_min - preset[i % 3] * 10 ** (i // 3), -1 * preset[i % 3] * 10 ** (i // 3)))
            data_range += list(range(0, data_max + preset[i % 3] * 10 ** (i // 3), preset[i % 3] * 10 ** (i // 3)))
            i += 1
    else:
        data_min = int(data_min/10) * 10
        data_range = list(range(data_min, data_max + 1, 1))
        i = 0

        while len(data_range) > max_y_labels:
            data_range = list(range(data_min, data_max + preset[i % 3] * 10 ** (i // 3), preset[i % 3] * 10 ** (i // 3)))
            i += 1
        
    data_range.sort()

    return data_range


main()
