##encodin=utf-8

"""
covered query是指一种特殊的query, 完全没有访问磁盘上的document, 而只是在内存中的index中进行查找。
在下面的例子中, 我们对关键字a, b, c建立了索引, 而如果我们只要返回a, b, c而不反悔_id关键字, 那么
就构成了一个covered query。
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo

col = db.col
col.drop()

def initialize_collections():
    col.insert_many([{"a": i, "b": i, "c": i, "d": ["pading"]*3} for i in range(1000)])
    col.create_index([("a", pymongo.ASCENDING), ("b", pymongo.ASCENDING), ("c", pymongo.ASCENDING)])
    
def non_covered_query_example():
    cursor = col.find({"a": 7, "b": 7, "c": 7})
    print("this is not a covered query")
    ppt(cursor.explain()["executionStats"])
    
def covered_query_example():
    """由于我们要求只返回a, b, c关键字而不返回_id关键字, 所以这是一个covered query
    executionTimeMillis 非常小, 接近于0
    totalDocsExamined 等于0, 因为只用到了索引而没有用到数据库
    """
    cursor = col.find({"a": 7, "b": 7, "c": 7}, {"_id": False, "a": True, "b": True, "c": True})
    print("this is a covered query")
    ppt(cursor.explain()["executionStats"])

if __name__ == "__main__":
    """本例用于展示cursor.explain()方法的功能
    """
    initialize_collections()
    non_covered_query_example()
    covered_query_example()
    client.close()