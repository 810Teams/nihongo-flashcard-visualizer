'''
    `nihongo.py`
'''

from math import ceil
from math import floor
from pygal.style import CleanStyle

import os
import pygal
import sqlite3


def main():
    rows = select_progress(create_connection('Flashcards.sqlite'))
    data = [rows.count(i) for i in range(0, max(rows) + 1)]

    render(data)

    print()
    print('- Flashcard Statistics -')
    print()
    print('Total: {}'.format(len(rows)))
    print('Average: {:.0f}-{:.0f} (+{:.2f})'.format(average(data) // 3 + 1, floor(average(data) % 3), average(data) % 3))
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


def average(data):
    return sum([data[i] * i for i in range(len(data))]) / sum(data)


def render(data):
    chart = pygal.Bar()

    # Chart Data
    # for i in range(0, ceil(len(data)/3)):
    #     chart.add('Level {}'.format(i), data[i*3: i*3 + 3])
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

    try:
        os.system('open chart.svg')
    except (FileNotFoundError, OSError, PermissionError):
        print('[ERROR] Something unexpected happened, please try again.')
    return


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
