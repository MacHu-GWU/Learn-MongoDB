##encoding=utf-8

"""
Unique index是指对某个所有的值两两不同的关键字创建的索引, 也就是和_id关键字具有相同的性质。类似
与关系数据库中的unique constrain。
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo

col = db.col # 使用col这个collection进行演示
col.drop() # 重置collection

def initialize_collection():
    col.insert({"a": 1})
    col.insert({"a": 2})
    col.insert({"a": 3})
    
def create_unique_index():
    col.create_index([("a", pymongo.ASCENDING)], unique=True)
    
if __name__ == "__main__":
    """本例用于演示unique index对唯一性的限制
    """
    initialize_collection()
    create_unique_index()
    col.insert({"a": 2}) # pymongo.errors.DuplicateKeyError
    client.close()