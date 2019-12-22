'''
    `nihongo.py`
'''

from pygal.style import CleanStyle

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
    print('Average: {:.0f}-{:.2f}'.format(average(data)//3 + 1, average(data) % 3))
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
    cur.execute(
        "SELECT ZPROGRESS, Z8_BECAMEACTIVEVIAFLASHCARDPACK FROM ZFLASHCARD")

    rows = [i[0] for i in cur.fetchall() if i[1] != None]

    return rows


def average(data):
    return sum([data[i] * i for i in range(len(data))]) / sum(data)


def render(data):
    chart = pygal.Bar()

    # for i in range(0, max(data) + 1):
    #     chart.add('{}-{}'.format(i//3 + 1, i % 3), data.count(i))

    chart.style = CleanStyle

    chart.add('Learned Words', data)

    chart.x_labels = ['{}-{}'.format(i//3 + 1, i % 3) for i in range(len(data))]

    chart.render_to_file('chart.svg')


main()
