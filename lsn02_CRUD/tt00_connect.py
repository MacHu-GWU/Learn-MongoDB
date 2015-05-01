##encoding=utf-8

"""
from tt00_connect import client, db, users
"""

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test
users = db.users

if __name__ == "__main__":
    print(client.database_names()) # 打印所有的databases
    print(db.collection_names()) # 打印所有的collections