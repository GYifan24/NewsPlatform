from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = 27017
DB_NAME = 'tap-news'

client = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)

def get_db(db = DB_NAME):
    # print("init mongo client")
    db = client[db]
    # print(db)
    return db
