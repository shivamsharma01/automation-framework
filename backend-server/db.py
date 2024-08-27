import sqlite3
import threading


thread_local = threading.local()

def get_db():
    if not hasattr(thread_local, "conn"):
        thread_local.conn = sqlite3.connect(':memory:')
        cursor = thread_local.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_status (
                id TEXT PRIMARY KEY,
                percent INTEGER,
                status TEXT
            )
        ''')
        thread_local.conn.commit()
    return thread_local.conn
