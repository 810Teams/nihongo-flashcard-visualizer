'''
    `nihongo.py`
'''

from math import ceil
from math import floor
from math import sqrt
from pygal.style import CleanStyle

import os
import pygal
import sqlite3


def main():
    raw_data = sorted(select_progress(create_connection('Flashcards.sqlite')))
    data = [raw_data.count(i) for i in range(0, max(raw_data) + 1)]

    render(data)

    print()
    print('- Flashcard Statistics -')
    print()
    print('Total: {}'.format(len(raw_data)))
    print()
    print('Median: {}'.format(get_level_format(median(raw_data))))
    print('Average: {}'.format(get_level_format(average(raw_data))))
    print('Standard Deviation: {}'.format(get_level_format(standard_deviation(raw_data))))
    print()

    for i in range(len(data) - 1, -1, -1):
        print('Level {}-{}: {}'.format(i//3 + 1, i % 3, data[i]))

    print()


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print('Error')

    return conn


def select_progress(conn):
    cur = conn.cursor()
    cur.execute('SELECT ZPROGRESS, Z8_BECAMEACTIVEVIAFLASHCARDPACK FROM ZFLASHCARD')

    rows = [i[0] for i in cur.fetchall() if i[1] != None]

    return rows


def get_level_format(level_value):
    return '{:.0f}-{:.0f} (+{:.2f})'.format(level_value // 3 + 1, floor(level_value % 3), level_value % 1)


def median(raw_data):
    raw_data.sort()
    if len(raw_data) % 2 == 0:
        return (raw_data[len(raw_data) // 2 - 1] + raw_data[len(raw_data) // 2])/2
    return raw_data[len(raw_data) // 2]


def average(raw_data):
    return sum(raw_data) / len(raw_data)


def standard_deviation(raw_data):
    return sqrt(sum([(i - average(raw_data)) ** 2 for i in raw_data])/len(raw_data))


def render(data):
    chart = pygal.HorizontalBar()

    # Chart Data
    chart.add('Learned Words', data)

    # Chart Titles
    chart.title = 'Learned Words by Level'

    # Chart Data
    chart.x_labels = ['{}-{}'.format(i//3 + 1, i % 3)
                      for i in range(len(data))]
    chart.y_labels = calculate_y_labels(min(data), max(data))
    
    # Chart Legends
    chart.show_legend = False
    chart.legend_at_bottom = True
    chart.legend_at_bottom_columns = 5
    chart.legend_box_size = 16

    # Chart Render
    chart.style = CleanStyle
    chart.render_to_file('chart.svg')

    # Chart Open
    try:
        os.system('open chart.svg')
    except (FileNotFoundError, OSError, PermissionError):
        print('[ERROR] Something unexpected happened, please try again.')


def calculate_y_labels(data_min, data_max, max_y_labels=15):
    ''' Function: Calculate y labels '''
    data_min = floor(data_min)
    data_max = ceil(data_max)
    
    preset = 1, 2, 5
    data_range = list(range(0, data_min - 1, -1)) + list(range(0, data_max + 1, 1))
    i = 0

    while len(data_range) > max_y_labels:
        data_range = list(range(0, data_min - preset[i % 3] * 10**(i // 3), -1 * preset[i % 3] * 10**(i // 3)))
        data_range += list(range(0, data_max + preset[i % 3] * 10**(i // 3), preset[i % 3] * 10**(i // 3)))
        i += 1
        
    data_range.sort()

    return data_range


main()
