from tinydb import TinyDB

DB = None
def get_db():
    '''
    return an instance of the db object (multithreaded)
    '''
    global DB
    if DB is None:
        DB = TinyDB('db.json')
    return DB