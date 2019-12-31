from src.utils import error
from src.utils import notice

import os
import pygal
import sqlite3

DATABASE_CONTAINER = 'NihongoBackup.nihongodata'
DATABASE_FILE = 'Flashcards.sqlite'

def extract():
    ''' Function: Extracts database file from the zip '''
    try:
        os.system('unzip -o {}/{}.zip'.format(DATABASE_CONTAINER, DATABASE_FILE))
    except (FileNotFoundError, OSError, PermissionError):
        pass


def create_connection():
    ''' Function: Creates the database connection '''
    conn = None
    try:
        conn = sqlite3.connect('{}'.format(DATABASE_FILE))
    except sqlite3.OperationalError:
        error('Please extract SQLite file before proceeding.')

    return conn


def get_progress(conn):
    ''' Function: Gets flashcard progress from database '''
    cur = conn.cursor()
    cur.execute('SELECT ZPROGRESS, Z8_BECAMEACTIVEVIAFLASHCARDPACK FROM ZFLASHCARD')

    return [i[0] for i in cur.fetchall() if i[1] != None]


def get_raw_data():
    ''' Function: Get raw data '''
    try:
        raw_data = get_progress(create_connection())
    except sqlite3.OperationalError:
        error('SQLite file not found. Beginning the extraction.')
        print()
        extract()
        print()
        raw_data = get_progress(create_connection())

    return sorted(raw_data)


def get_processed_data():
    ''' Function: Get processed data '''
    raw_data = get_raw_data()
    return [raw_data.count(i) for i in range(0, max(raw_data) + 1)]
