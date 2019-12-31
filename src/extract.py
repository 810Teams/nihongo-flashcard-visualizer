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
