##encoding=utf-8

from pymongo import MongoClient

client = MongoClient()
db = client.test
col = db.col