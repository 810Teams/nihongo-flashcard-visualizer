'''
    `render.py`
'''

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
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from time import perf_counter

from src.statistics import estimated
from src.utils import notice
from src.utils import level_format

import numpy
import os
import pygal


def render(data, days=60, dot_shrink=True, incorrect_p=0.0, max_y_labels=15, show_correlation=False, simulation_mode=False, style='DefaultStyle'):
    ''' Function: Renders the chart '''
    time_start = perf_counter()

    render_by_level(data, days=days, max_y_labels=max_y_labels, simulation_mode=simulation_mode, style=eval(style))
    render_progress(data, days=days, max_y_labels=max_y_labels, simulation_mode=simulation_mode, style=eval(style))
    render_estimated(data, days=days, dot_shrink=dot_shrink, incorrect_p=incorrect_p, max_y_labels=max_y_labels, show_correlation=show_correlation, simulation_mode=simulation_mode, style=eval(style))
    
    notice('Total time spent rendering charts is {:.2f} seconds.'.format(perf_counter() - time_start))


def render_by_level(data, days=60, max_y_labels=15, simulation_mode=False, style=DefaultStyle):
    ''' Function: Renders the words and kanji by level chart '''
    chart = pygal.HorizontalStackedBar()

    # Chart Data
    data_word = [i for i in data['word']]
    data_kanji = [i for i in data['kanji']]
    if simulation_mode:
        data_word = estimated([0 for _ in range(13)], days=days, learn_pattern=[10], result='vocabulary')[-1]
        
    chart.add('Learned Words', [{'value': i, 'label': '{:.2f}%'.format(i / (sum(data_word) + (sum(data_word) == 0)) * 100)} for i in data_word])
    chart.add('Learned Kanjis', [{'value': i, 'label': '{:.2f}%'.format(i / (sum(data_kanji) + (sum(data_kanji) == 0)) * 100)} for i in data_kanji])

    # Chart Titles
    chart.title = 'Learned Words & Kanjis by Level'

    # Chart Labels
    chart.x_labels = ['{}-{}'.format(i // 3 + 1, i % 3) for i in range(len(data_word))]
    chart.y_labels = y_labels(0, max(data['overall']), max_y_labels=max_y_labels)
    
    # Chart Legends
    chart.show_legend = False

    # Chart Render
    chart.style = style
    chart.render_to_file('charts/by_level.svg')

    # Notice
    notice('Chart \'by_level\' successfully exported.')


def render_progress(data, days=60, max_y_labels=15, simulation_mode=False, style=DefaultStyle):
    ''' Function: Renders the progress chart '''
    chart = pygal.Histogram()

    # Chart Data
    data_copy = [i for i in data['word']]
    if simulation_mode:
        data_copy = estimated([0 for _ in range(13)], days=days, learn_pattern=[10], result='vocabulary')[-1]

    for i in range(0, 13, 3):
        chart.add(
            'Level {:.0f}'.format(i//3 + 1),
            [{
                'value': (round((i + j) / 3 + 1, 2), sum(data_copy[:i + j + 1]) - data_copy[i + j], sum(data_copy[:i + j + 1])),
                'label': '{:.2f}%'.format(data_copy[i + j] / (sum(data_copy) + (sum(data_copy) == 0)) * 100)
            } for j in range(len(data_copy[i:i + 3]))],
            formatter=lambda x: '{}'.format(x[2] - x[1])
        )

    # Chart Titles
    chart.title = 'Word Progress'
    chart.x_title = 'Words'

    # Chart Labels
    chart.x_labels = range(1, sum(data_copy) + 1)
    chart.x_labels_major_count = 8
    chart.show_minor_x_labels = False
    chart.y_labels = [0, 1, 2, 3, 4, 5]
    chart.truncate_label = -1

    # Chart Legends
    chart.show_legend = True
    
    # Chart Render
    chart.style = style
    chart.dots_size = 2
    chart.render_to_file('charts/progress.svg')

    # Notice
    notice('Chart \'progress\' successfully exported.')


def render_estimated(data, days=60, dot_shrink=True, incorrect_p=0.0, max_y_labels=15, show_correlation=False, simulation_mode=False, style=DefaultStyle):
    ''' Function: Renders the estimated flashcards per day chart '''
    chart = pygal.Line()

    # Chart Data
    data_copy = [i for i in data['overall']]
    if simulation_mode:
        data_copy = [0 for _ in range(13)]

    learn_patterns = [
        ('Never Study', [0]),
        ('10 Per Day', [10]),
        ('20 Per Day', [20])
    ]

    estimated_list = list()

    for i, j in learn_patterns:
        estimated_list.append([sum(k) for k in estimated(data_copy, days=days, incorrect_p=incorrect_p, learn_pattern=j, result='flashcard')])
        chart.add(i, [None] + estimated_list[-1], allow_interruptions=True, stroke=True)

    # Correlation
    for i in range(len(estimated_list) * show_correlation):
        x = numpy.array([[j] for j in range(1, len(estimated_list[i]) + 1)])
        y = numpy.array(estimated_list[i])

        poly_f = PolynomialFeatures(degree = 3)
        x = poly_f.fit_transform(x)

        regressor = LinearRegression()
        regressor.fit(x, y)

        chart.add('Correlation-{}'.format((0, 10, 20)[i]), [None] + regressor.predict(x).tolist(), stroke_style={'width': 4}, show_dots=False)

    # Chart Titles
    chart.title = 'Estimated Flashcards Per Day'
    chart.x_title = 'Days'

    # Chart Labels
    chart.x_labels = [i for i in range(0, days + 1)]
    chart.x_labels_major_count = 8
    chart.show_minor_x_labels = False

    chart.y_labels = y_labels(
        min([min([j for j in i]) for i in estimated_list]),
        max([max([j for j in i]) for i in estimated_list]),
        max_y_labels=max_y_labels,
        skip=True
    )

    chart.truncate_label = -1
    
    # Chart Legends
    chart.show_legend = True
    chart.legend_at_bottom = False
    chart.legend_at_bottom_columns = 4
    chart.legend_box_size = 16

    # Chart Render
    chart.style = style
    chart.dots_size = 2.5

    if dot_shrink:
        bp = 60     # Data amount which dots started shrinking
        factor = 3  # Closer to 1, slower the dots shart shinking. If at 1, dots will never shrink.
        chart.dots_size = 2.5 * ((bp + max(0, days - bp) / factor) / max(bp, days))

    chart.render_to_file('charts/estimated.svg')
    
    # Notice
    notice('Chart \'estimated\' successfully exported.')


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
