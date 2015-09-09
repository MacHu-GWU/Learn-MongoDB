##encoding=utf-8

"""
本例用于展示如何创建和使用Hashed Index
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo
import random
import string
import time

col = db.col
col.drop()

def randstr():
    res = list()
    for _ in range(2):
        res.append(random.choice(string.ascii_letters + string.digits))
    return "".join(res)
        
def initialize_collections():
    data = list()
    for i in range(10000):
        data.append({
            "profile": {"text": randstr()}
        })
    col.insert(data)
    
def query_without_hashed_index():
    st = time.clock()
    res = list(col.find({"profile": {"text": "a1"}}))
    print(time.clock() - st)
    ppt(res)

def query_with_hashed_index():
    col.create_index([("profile", pymongo.HASHED)])
    st = time.clock()
    res = list(col.find({"profile": {"text": "a1"}}))
    print(time.clock() - st)
    ppt(res)
    
    
if __name__ == "__main__":
    initialize_collections()
    query_without_hashed_index()
    query_with_hashed_index()
    client.close()    
