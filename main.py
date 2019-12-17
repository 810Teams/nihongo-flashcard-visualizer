'''
    `nihongo.py`
'''

import sqlite3


def main():
    conn = create_connection('Flashcards.sqlite')
    rows = select_progress(conn)

    for i in range(max(rows), -1, -1):
        print('Level {}/{} - {}'.format(i//3 + 1, i % 3, rows.count(i)))


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print('Error')

    return conn


def view(conn):
    cur = conn.cursor()
    cur.execute("SELECT ZPROGRESS, Z8_BECAMEACTIVEVIAFLASHCARDPACK FROM ZFLASHCARD")

    rows = cur.fetchall()

    for i in rows:
        print(i)


def select_progress(conn):
    cur = conn.cursor()
    cur.execute("SELECT ZPROGRESS, Z8_BECAMEACTIVEVIAFLASHCARDPACK FROM ZFLASHCARD")

    rows = [i[0] for i in cur.fetchall() if i[1] != None]

    return rows


main()
