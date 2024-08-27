from tinydb import TinyDB

DB = None
def get_db():
    global DB
    if DB is None:
        DB = TinyDB('db.json')
    return DB