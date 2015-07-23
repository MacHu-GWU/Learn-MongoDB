##encoding=utf-8

"""
Sparse Index是指在整个collection中, 某个关键字并不是经常出现, 而我们又需要为该关键字创建索引。普通
索引需要为所有的documents创建索引, 会带来大量的硬盘空间消耗。而如果使用Sparse Index, 则只需要对部分
包含该关键字的文档创建索引, 这样可以节省硬盘和内存(Mongodb会将一部分索引读取到内存中)。
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo
import random
import time

col = db.col # 使用col这个collection进行演示

def initialize_collection():
    """初始化演示数据库, 大约用时1-10秒
    """
    st = time.clock()
    if col.find({"_id": "initialized"}).count() == 0: # 检测是否已经被初始化过, 避免重复初始化
        col.drop()
        col.insert({"_id": "initialized"})
        
        data = list()
        complexity = 100*1000
        for i in range(complexity):
            if (i % 1000 == 0):
                data.append({"series_id": i, "foo": i})
            else:
                data.append({"series_id": i})
        col.insert_many(data)
    print("initializing the colletion cost %.4f seconds." % (time.clock() - st,) )
    
def create_index():
    col.create_index([("foo", pymongo.ASCENDING)])

def create_sparse_index():
    """创建稀疏索引, 只对包含foo关键字的文档建立索引, 所以磁盘空间占用较小
    """
    col.create_index([("foo", pymongo.ASCENDING)], sparse=True)

def drop_index():
    col.drop_indexes()
    
if __name__ == "__main__":
    """本例用于演示对不常用的关键字使用普通索引和稀疏索引所占的硬盘空间的区别
    """
#     initialize_collection()
    drop_index()
#     create_index() # size = 1716960
    create_sparse_index() # size = 8176
    ppt(db.command("collstats", "col")) # print information
    client.close()