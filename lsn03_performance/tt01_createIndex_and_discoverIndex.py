##encoding=utf-8

"""
本节介绍如何创建索引和如果查看已有的索引
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo

col = db.col # 使用col这个collection进行演示
col.drop() # 重置collection

def initialize_collection():
    col.insert({"a":1, "b":2, "c":3})

def create_index():
    """pymongo中建立索引的语法请参考官方api文档:
    http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_index
    """
    col.create_index([("a", pymongo.ASCENDING)])

def discover_index():
    """mongodb中每一个database都有一个reserved的collection, 叫system.indexes。里面储存了改数据库中
    所有collection的索引的信息。你可以使用db.system.indexes.find()命令查看所有的metadata。也可以用
    db.system.indexes.find({"ns": #db_name.collection_name})来查看某一个collections相关的索引信息。
    
    mongodb中系统回味任何collection的_id这个特殊的field建立主键索引, 这和关系数据库一样。
    """
    print("\n显示 _id 和 a 这两个field有索引")
    ppt(list(db.system.indexes.find({"ns": "test.col"}))) # 显示 _id 和 a 这两个field有索引
    print("\n返回所有index列表")
    ppt(list(db.col.list_indexes())) # pymongo api, 返回所有index列表
    print("\n返回collection中所有index的信息")
    ppt(db.col.index_information()) # pymongo api, 返回collection中所有index的信息
    
if __name__ == "__main__":
    initialize_collection()
    create_index()
    discover_index()
    client.close()