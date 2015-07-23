##encoding=utf-8

"""
aggregation framework是一种对文档数据流分类, 整理, 计算, 输出的过程。
    对数据进行分类整理过程中所用的方法叫做: stage。常用的stage operator有:
        $match, $group, $project, ...
    
    关于stage operator更多信息请参考:
        http://docs.mongodb.org/manual/reference/operator/aggregation/#stage-operators

关于对数据进行计算的operator, 例如$sum, $avg请参考Accumulators operators:
    http://docs.mongodb.org/manual/reference/operator/aggregation/#aggregation-accumulator-operators

reference:
    http://docs.mongodb.org/manual/core/aggregation-introduction/
"""

from connect import client, db, col
from pprint import pprint as ppt
import random
import time

def prepare_data():
    """准侧测试数据
    """
    if col.find({"_id": "finished"}).count() == 0:
        col.drop()
        col.insert({"_id": "finished"})
        all_names = list("abcdefghij")
        data = [{"name": random.choice(all_names), 
                 "value": random.randint(1, 1000)} for i in range(1000*1000)]
        col.insert(data)

def group_example():
    """计算每一个name的value之和是多少
    """
    res = col.aggregate([{"$group": {"_id": "$name", "total": {"$sum": "$value"}}}])
    for doc in res:
        print(doc)

def match_and_group_example():
    """求name = a, b, c各自的total value是多少。
    先用match选择一部分文档, 然后再用group统计每一类的value总和
    """
    res = col.aggregate([{"$match": {"name": {"$in": list("abc")}}}, 
                         {"$group": {"_id": "$name", "total": {"$sum": "$value"}}}])
    for doc in res:
        print(doc)

def count_example():
    """计算某个多少个文档 {"name": "a"}
    """
    print(col.count({"name": "a", "value": 1}))

def distinct_example():
    """计算 "name" field 有多少个不同的值。注意, distinct方法只能对一个field进行操作, 如果要对
    多个field进行操作, 请参考distinct_multi_fields_example()中的例子
    """
    print(col.distinct("name"))
    
def distinct_multi_fields_example():
    """计算 name, value 有多少种不同的组合, 本例中一共使用了三种方法, 其中以使用内置的
    aggregation framework的方法最好。
    方法1, 先按照 name, value group up 到 _id, 然后再对group结果中所有的document计数
    方法2, 先按照 name, value group up 到 _id, 然后对结果进行遍历+计数。
    方法3, 选择所有的文档, 用集合储存 unique name, value combination, 然后求集合的大小
    """
    # 方法1
    st = time.clock()
    res = col.aggregate([
            {
                "$group": {
                    "_id": {
                        "name": "$name",
                        "value": "$value",
                        },
                    }
            }, 
            {
                "$group": {"_id": None, "count": {"$sum": 1}}
            },
            ], allowDiskUse=True,
        )
    for doc in res:
        print("total distinct name, value combination is: %s" % doc["count"])
    print("double group method elapse: %.4f" % (time.clock() - st))
    
    # 方法2
    st = time.clock()
    res = col.aggregate([
            {
                "$group": {
                    "_id": {
                        "name": "$name",
                        "value": "$value",
                        },
                    }
            }])
    counter = 0
    for doc in res:
        counter += 1
    print("total distinct name, value combination is: %s" % counter)
    print("for loop method takes: %.4f" % (time.clock() - st))
    
    # 方法3
    st = time.clock()
    s = set()
    res = col.find({})
    for doc in res:
        try:
            s.add("%s%s" % (doc["name"], doc["value"]))
        except:
            pass
    print("total distinct name, value combination is: %s" % len(s))
    print("for loop method takes: %.4f" % (time.clock() - st))
    
def map_reduce_example():
    """mongodb中不接受使用python写成的mapper和reducer, 只接受java script脚本。
    所以在pymongo中无法使用python function进行map reduce
    """
        
    
if __name__ == "__main__":
#     col.drop()
#     prepare_data()
#     group_example()
#     match_and_group_example()
#     count_example()
#     distinct_example()
#     distinct_multi_fields_example()
    client.close()