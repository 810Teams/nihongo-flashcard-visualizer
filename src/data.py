'''
    `data.py`
'''

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


def get_progress():
    ''' Function: Gets flashcard progress from database '''
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('SELECT ZPROGRESS, ZSTATUSASINT, ZKANJITEXT FROM ZFLASHCARD')

    data = cur.fetchall()

    return {
        'word': [i[0] for i in data if bool(i[1]) and i[2] == None],
        'kanji': [i[0] for i in data if bool(i[1]) and i[2] != None],
        'overall': [i[0] for i in data if bool(i[1])]
    }


def get_raw_data():
    ''' Function: Get raw data '''
    try:
        raw_data = get_progress()
    except sqlite3.OperationalError:
        error('SQLite file not found. Beginning the extraction.')
        print()
        extract()
        print()
        raw_data = get_progress()

    return raw_data


def get_processed_data():
    ''' Function: Get processed data '''
    raw_data = get_raw_data()

    raw_data_new = dict()

    for i in raw_data:
        raw_data_new[i] = [raw_data[i].count(j) for j in range(0, 13)]

    return raw_data_new
