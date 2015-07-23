##encoding=utf-8

"""
参考文档:
    使用全文索引: http://docs.mongodb.org/manual/reference/operator/query/text/
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo

col = db.col
col.drop()

def initialize_collections():
    """初始化演示数据库
    """
    col.insert({"article": """An Apple Store employee told Tim Cook that the company treats its staff like "criminals.";"""})
    col.create_index([("article", pymongo.TEXT)])
    
def query_with_full_text_index():
    ppt(list(col.find({
                "$text":{
                    "$search": "apple tim"
                    }})))    

if __name__ == "__main__":
    """本例用于展示如何创建和使用全文搜索引擎
    """
    initialize_collections()
    query_with_full_text_index()
    client.close()