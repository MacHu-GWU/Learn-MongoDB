##encoding=utf-8

"""
[CN]
用户可以为多个关键字都创建索引, 但是当某个索引的内容是array时, 则会引入multikey index的概念。

例如考虑下面的collection schema:

company = {
    "_id": 1,
    "name": apple,
    "tags": ["IT", "mobile", "desktop", "laptop"],
    "city:: ["New York", "Los Angeles", "Bei Jing", "Longdon"],
    }

混合多重索引(Compound Multikey Indexes)限制:

    如果我们同时为name和tags, 或是name和city建立index, 都会构成multikey index, 不存在任何问题。这样
    能让对于涉及tags和city关键字的查找更快。但是用户不能同时对两个array like的关键字建立
    unique index, 因为这样做需要对tags和city中所有可能的值的两两组合都建立index, 这个开销太大了, 
    所以mongodb禁止这么做。
    
    如果你已经建立了Multikey Indexes, 那么如果你有一个新文档在在所有Multikey Indexes的关键字中有两个
    关键字是array like的, 那么你将无法插入该文档。
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo
import random
import time

companys = db.companys

def random_string(length):
    """用于产生随机字符串
    """
    s = []
    for _ in range(length):
        s.append(random.choice("abcdefghijklmnopqrstuvwxyz"))
    return "".join(s)

def initialize_collection():
    """初始化演示数据库, 大约用时10-60秒
    每个数据库
    """
    st = time.clock()
    if companys.find({"_id": "initialized"}).count() == 0: # 检测是否已经被初始化过, 避免重复初始化
        companys.drop()
        companys.insert({"_id": "initialized"})
        
        complexity = 1000*100
        data = list()
        for i in range(complexity):
            doc = {"_id": str(i),
                   "name": random_string(10),
                   "tags": [random.randint(1, 100) for _ in range(5)],
                   "citys": [random.randint(1, 3000) for _ in range(10)]}
            data.append(doc)
        companys.insert_many(data)

        companys.insert({"_id": str(complexity), "name": "apple", # add explicit one, so we can try find it
                         "tags": list(range(1, 5+1)),
                         "citys": list(range(1, 10+1))})
    
    print("initializing the colletion cost %.4f seconds." % (time.clock() - st,) )
    
def query_without_index():
    """对array like的关键字tags进行查询
    """
    st = time.clock()
    ppt(list(companys.find({"tags": {"$all": [1,2,3]}}))) 
    print("query WITHOUT index cost %.4f seconds." % (time.clock() - st,) )
    
def create_index():
    """为tags关键字添加索引
    """
    companys.create_index([("tags", pymongo.ASCENDING)])

def drop_index():
    """删除所有
    """
    companys.drop_indexes()

def query_with_index():
    """对array like的关键字tags进行查询
    """
    st = time.clock()
    ppt(list(companys.find({"tags": {"$all": [1,2,3]}}))) 
    print("query WITH index cost %.4f seconds." % (time.clock() - st,) )

def create_invalid_index():
    """尝试添加违反规则的multikey index, 执行这个之前请先执行drop_index。
    """
    companys.create_index([("tags", pymongo.ASCENDING), ("city", pymongo.ASCENDING)])
    
def inser_invalid_document():
    companys.insert({"tags": [1,2,3], "city": [1,2,3]})

if __name__ == "__main__":
#     companys.drop()
    initialize_collection()
    drop_index()
#     query_without_index()
#     create_index()
#     query_with_index()

    create_invalid_index() # 创建多重索引
    inser_invalid_document() # pymongo.errors.WriteError: cannot index parallel arrays [city] [tags]

#     ppt(list(companys.list_indexes())) # 打印所有索引信息
    client.close()