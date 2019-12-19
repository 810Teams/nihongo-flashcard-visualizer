'''
    `nihongo.py`
'''

from pygal.style import CleanStyle

import pygal
import sqlite3


def main():
    conn = create_connection('Flashcards.sqlite')
    rows = select_progress(conn)

    render(rows)

    print()
    print('- Flashcard Statistics -')
    print()
    print('Total: {}'.format(len(rows)))
    print()

    for i in range(max(rows), -1, -1):
        print('Level {}-{}: {}'.format(i//3 + 1, i % 3, rows.count(i)))

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


def render(data):
    chart = pygal.Bar()

    # for i in range(0, max(data) + 1):
    #     chart.add('{}-{}'.format(i//3 + 1, i % 3), data.count(i))

    chart.style = CleanStyle

    chart.add('Learned Words', [data.count(i)
                                for i in range(0, max(data) + 1)])

    chart.x_labels = ['{}-{}'.format(i//3 + 1, i % 3)
                      for i in range(0, max(data) + 1)]

    chart.render_to_file('chart.svg')


main()
