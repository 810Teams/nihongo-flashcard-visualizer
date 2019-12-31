from math import ceil
from math import floor
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

from src.statistics import estimated

import os
import pygal

def render(data, days=30):
    ''' Function: Renders the chart '''
    # Old Chart Deletion
    try:
        os.system('rm charts/*')
    except (FileNotFoundError, OSError, PermissionError):
        print('[ERROR] Old chart files deletion error.')

    render_word_by_level(data)
    render_estimated(data, days=days)
    
    # Chart Opening
    try:
        os.system('open charts/*')
    except (FileNotFoundError, OSError, PermissionError):
        print('[ERROR] Chart files opening error.')


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


def render_estimated(data, days=30):
    ''' Function: Renders the estimated chart '''
    chart = pygal.Line()

    # Chart Data
    learn_patterns = [
        ('Never Study', [0]),
        ('10 Per Day', [10]),
        ('20 Per Day', [20]),
    ]

    estimated_list = list()

    for i, j in learn_patterns:
        estimated_list.append([sum(k) for k in estimated(data, days=days, learn_pattern=j, result='flashcard')])
        chart.add(i, estimated_list[-1])

    # Chart Titles
    chart.title = 'Estimated Flashcards Per Day'
    chart.x_title = 'Days'

    # Chart Labels
    chart.x_labels = [i for i in range(1, days + 1)]
    chart.x_labels_major_count = 8
    chart.show_minor_x_labels = False

    chart.y_labels = y_labels(
        min([min([j for j in i]) for i in estimated_list]),
        max([max([j for j in i]) for i in estimated_list]),
        skip=True
    )

    chart.truncate_label = -1
    
    # Chart Legends
    chart.show_legend = True
    chart.legend_at_bottom = False
    chart.legend_at_bottom_columns = 4
    chart.legend_box_size = 16

    # Chart Interpolation
    chart.interpolate = 'cubic'

    # Chart Render
    chart.style = DarkStyle
    chart.dots_size = 2
    chart.render_to_file('charts/estimated.svg')


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