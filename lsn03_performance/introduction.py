##encoding=utf-8

"""
[CN]
本章主题: 索引与性能

包含的主题:
1. 创建和查看索引

2. 索引的作用
    - 索引的作用
    - 多重索引(multikey indexes)
    
3. 创建不同类型的索引
    - Unique Index, 普通的Btree索引
    - Sparse Index, 稀疏索引, 用于非常见的field上
    - TTL(Time To Live) Index, 仅在一定时间内存在的索引, 索引失效后会连文档一起删除。
        通常用于有时效性的文档。
    - Geospatial Index, 2d/3d地理位置索引(仅高版本支持)
    - Text Index, 全文搜索引擎索引
    
4. explain, 查看query中用到了哪些索引

5. 

Import Command
--------------
    from introduction import client, db
"""

from pymongo import MongoClient
from pprint import pprint as ppt

client = MongoClient("localhost", 27017)
db = client.test