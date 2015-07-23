##encoding=utf-8

"""
索引是一种通过将某一个关键字进行排序之后, 使得对该关键字查找的速度变快的技术(请自行google, 相关资料
很多)。当数据建立索引之后, 所有的CRUD操作都会影响到index, 也会带来少量额外开销。

索引与读/写操作的关系:
    通常来说, 索引越多, 查询速度就越快。索引越多, 写操作速度就越慢。
    
建立索引的时机:
    假设你有10000条文档需要建立索引。那么将所有文档insert到collection之后, 再执行create_index, 效率
    要比: "先插入5000条文档 -> 建立索引 -> 继续插入5000条文档" 快非常多。这是因为在建立新索引的时候
    mongodb engine会使用bulk operation进行批量操作, 所以速度比较快。而一旦索引建立好之后, 插入每一条
    文档时都要在索引中找到文档相应的索引的位置, 这需要大量操作, 所以速度比较慢。
    
用户可以为任意多个关键字创建索引, 但是创建太多的索引会导致数据库写入性能大大降低。
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo
import time

items = db.items

def initialize_collection():
    """初始化演示数据库, 大约用时10-60秒
    """
    st = time.clock()
    if items.find({"_id": "initialized"}).count() == 0: # 检测是否已经被初始化过, 避免重复初始化
        items.drop()
        items.insert({"_id": "initialized"})
        
        complexity = 1000 * 1000
        items.insert_many([{"item_id": i} for i in range(complexity)])
        
    print("initializing the colletion cost %.4f seconds." % (time.clock() - st,) )
    
def find_method_example():
    """find方法在找到了一条文档之后, 并不会停止, 会扫描整个collection, 检查是否还有文档能匹配。
    所以不管item_id是多少, 执行时间都是一样的。
    """
    st = time.clock()
    for doc in items.find({"item_id": 5}):
        pass
    print("find(item_id = 5), elapse %.4f seconds" % (time.clock() - st, ))

    st = time.clock()
    for doc in items.find({"item_id": 500*1000}):
        pass
    print("find(item_id = 500,000), elapse %.4f seconds" % (time.clock() - st, ))

def find_one_method_example():
    """find_one方法找到了一条信息之后就会停止, 所以item_id=5的查询速度非常快, 而item_id=500,000的
    查询时间是find()方法的一半, 这是因为只需要扫描一半的表。
    """
    st = time.clock()
    doc = items.find_one({"item_id": 5})
    print("find(item_id = 5), elapse %.4f seconds" % (time.clock() - st, ))
    
    st = time.clock()
    doc = items.find_one({"item_id": 500*1000})
    print("find(item_id = 500,000), elapse %.4f seconds" % (time.clock() - st, ))

def create_index():
    """为item_id关键字添加索引
    create index的python API语法请参考官方文档:
    http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_indexes
    """
    items.create_index([("item_id", pymongo.ASCENDING)])

def drop_index():
    """删除item_id关键字的索引
    drop index的python API语法请参考官方文档:
    http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.drop_index
    """
    items.drop_index("item_id_1")

def query_with_index():
    """当启用了index之后, 无论是用find还是find_one, 无论item_id的大小如何, 速度都很快。
    """
    st = time.clock()
    doc = items.find({"item_id": 5})
    print("find(item_id = 5), elapse %.4f seconds" % (time.clock() - st, ))

    st = time.clock()
    doc = items.find_one({"item_id": 5})
    print("find_one(item_id = 5), elapse %.4f seconds" % (time.clock() - st, ))

    st = time.clock()
    doc = items.find({"item_id": 500*1000})
    print("find(item_id = 500,000), elapse %.4f seconds" % (time.clock() - st, ))

    st = time.clock()
    doc = items.find_one({"item_id": 500*1000})
    print("find_one(item_id = 500,000), elapse %.4f seconds" % (time.clock() - st, ))
    

if __name__ == "__main__":
    """本例子先生成一个1000,000条数据的collections, 然后分别查找位于前面和中间位置的数据。可以看出
    在没有索引的情况下, 如果用find方法, 会扫描整个表。而用find_one方法, 则查找中间位置的数据会慢
    很多。而一旦有了索引, 无论是用find还是find_one方法, 无论是数据的位置如何, 速度都非常快。
    
    你可以用drop_index()函数删除索引, 重新进行演示
    """
    initialize_collection()
    find_method_example()
    find_one_method_example()
    create_index()
    query_with_index()
#     drop_index()
    client.close()