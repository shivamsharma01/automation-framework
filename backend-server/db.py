from tinydb import TinyDB
import json

DB = None

def get_db():
    '''
    Return an instance of the DB object (singleton for multi-threaded access).
    '''
    global DB
    if DB is None:
        DB = TinyDB('db.json')
        load_initial_data(DB)
    return DB

def load_initial_data(db):
    '''
    Load initial data into the database from a JSON file.
    '''
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            db.truncate()
            db.insert_multiple(data)
            print("Data loaded into TinyDB.")
    except Exception as e:
        print(f"Failed to load data: {e}")