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
    col.insert({"a": 1, "b": 1})
    col.insert({"a": 2, "b": 2})
    col.insert({"a": 3, "b": 3})
    
def use_unique_index():
    """建立了unique index之后, 该field就跟_id一样, 不可以重复了
    """
    col.create_index([("a", pymongo.ASCENDING)], unique=True)
    col.insert({"a": 1})
    
def use_multiple_unique_index():
    """为多个field建立unique index, 可以保证多个field的组合的唯一性。
    """
    col.create_index([("a", pymongo.ASCENDING), ("b", pymongo.ASCENDING)], 
                     unique=True)
    col.insert({"a": 1, "b": 2}) # ok
    col.insert({"a": 1, "b": 1, "c": 1}) # DuplicateKeyError
    
if __name__ == "__main__":
    """本例用于演示unique index对唯一性的限制
    """
    initialize_collection()
#     use_unique_index()
#     use_multiple_unique_index()
    client.close()