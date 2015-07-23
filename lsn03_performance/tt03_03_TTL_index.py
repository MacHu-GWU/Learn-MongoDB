##encoding=utf-8

"""
TTL(Time to live)索引是一种在创建索引后, 经过一定时间自动删除索引以及被索引的文档的机制。
主要用于临时需要大量被查找的文档。例如临时的cookie。

至于具体的使用细节, 我还没有研究清楚。
官方文档: http://docs.mongodb.org/manual/core/index-ttl/
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo
import time

col = db.col
col.drop()

def initialize_collection():
    """初始化演示数据库
    """
    col.insert({"value": i} for i in range(3))

def create_TTL_index():
    col.create_index([("value", pymongo.ASCENDING)], expireAfterSeconds=3)
    
if __name__ == "__main__":
    initialize_collection()
    print("at begin, we have:")
    ppt(list(col.find()))
    create_TTL_index()
    time.sleep(65)
    print("wait for 65 seconds, we have:")
    ppt(list(col.find()))
    
    client.close()