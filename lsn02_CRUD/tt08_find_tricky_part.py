##encoding=utf-8

import pymongo

client = pymongo.MongoClient()
db = client.test
col = db.col
col.drop()

def test_sort_and_limit():
    """跟其他数据库一样, 在limit和sort同时存在时, 是将所有匹配到的都匹配上之后, 再limit前若个
    """
    col.insert([
            {"value": 3},
            {"value": 4},
            {"value": 5},
            {"value": 1},
            {"value": 2},
            ])
    
    for doc in col.find().limit(3).sort("value", 1):
        print(doc)

test_sort_and_limit()

client.close()

