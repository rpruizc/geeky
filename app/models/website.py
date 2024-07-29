import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS websites
                  (url TEXT PRIMARY KEY, title TEXT, content TEXT, ai_summary TEXT)''')
    db.commit()

class Website:
    @staticmethod
    def create_or_update(url, title, content, ai_summary):
        db = get_db()
        db.execute(
            'INSERT OR REPLACE INTO websites (url, title, content, ai_summary) VALUES (?, ?, ?, ?)',
            (url, title, content, ai_summary)
        )
        db.commit()

    @staticmethod
    def get_all():
        db = get_db()
        return db.execute('SELECT url, title, ai_summary FROM websites').fetchall()