##encoding=utf-8

"""
官方文档:
    创建geospatial索引: http://docs.mongodb.org/manual/administration/indexes-geo/
    使用geospetial索引: http://docs.mongodb.org/manual/reference/operator/query-geospatial/
"""

from introduction import client, db
from pprint import pprint as ppt
import pymongo
import random
import time

col = db.col
col.drop()

def initialize_collection():
    """初始化演示数据库
    """
    col.insert({"loc": [random.random()*10, random.random()*10]} for i in range(100))
    
def query_without_geospatial_index():
    """在100*1000这个数量及下, 需要0.05 - 0.08秒左右
    """   
    col.insert([{"lat": random.random()*10, "lgn": random.random()*10} for i in range(100*1000)])
    st = time.clock()
    cursor = col.find({"$and": [
                {"lat": {"$gte": 3}},
                {"lat": {"$lte": 4}},
                {"lgn": {"$gte": 3}},
                {"lgn": {"$lte": 4}},
                ]})
    for doc in cursor:
        pass
    print(time.clock() - st)
    
def query_with_geospatial_index():
    """在100*1000这个数量及下, 需要0.01 - 0.015秒左右
    """
    col.insert({"loc": [random.random()*10, random.random()*10]} for i in range(100*1000))
    col.create_index([("loc", pymongo.GEO2D)])
    st = time.clock()
    results = col.find({
                    "loc": {
                        "$within": {
                            "$center": [[3.5, 3.5], 0.5]
                            }
                        }
                    })
    for doc in results:
        pass
    print(time.clock() - st)  
    
if __name__ == "__main__":
    """本例是演示地理坐标数据常用的应用, 以某一位置为圆心, 返回距离圆心距离小于x的所有地址。
    传统的方法是将lat, lgn分拆成两个关键字, 先用一个正方形的box筛选出少量的记录, 然后计算这些记录
    离圆心的距离并排序, 最后返回。
    而在mongodb中如果使用了geospatial index, 那么可以用$near直接从近到远返回记录, 也可以用$within
    返回一定距离内的所有记录。并且速度极快。
    """
#     query_without_geospatial_index()
    query_with_geospatial_index()
    client.close()