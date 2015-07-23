##encodin=utf-8

"""
explain方法是用于让用户能更深刻的了解到query时究竟发生了什么。
当用户使用collections.find()的时候, pymongo会解析query, 然后生成一个cursor对象。所以在执行了
collections.find()之后, 数据库并没有开始进行取文档的操作。而是在用户显示的执行:
    for document in collections.find():
之类的行为之后才真正开始。

既然collections.find()返回的是cursor, 那么我们就可以使用cursor.explain()方法查看数据库对query
的解析结果如何。其中我们比较感兴趣的是到底有哪些index被使用到。

参考文档:
    mongodb官方文档: http://docs.mongodb.org/manual/reference/method/cursor.explain/
    pymongo API: http://api.mongodb.org/python/current/tutorial.html#indexing
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo

col = db.col
col.drop()

def initialize_collections():
    col.insert_many([{"a": i, "b": i, "c": i} for i in range(100)])
    col.create_index([("a", pymongo.ASCENDING), ("b", pymongo.ASCENDING)])
    
def explain_example():
    cursor = col.find({"a": 17}).sort("b", pymongo.ASCENDING)
    ppt(cursor.explain())
    
#     ppt(list(col.find()))

if __name__ == "__main__":
    """本例用于展示cursor.explain()方法的功能
    """
    initialize_collections()
    explain_example()
    client.close()