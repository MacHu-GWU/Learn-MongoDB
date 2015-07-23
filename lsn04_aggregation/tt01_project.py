##encoding=utf-8

"""
project是指将一种数据结构映射成另一种数据结构的转换过程。
"""

from connect import client, db, col
from pprint import pprint as ppt
import random
import time

def prepare_data():
    col.drop()
    data = [{
        "_id" : 1,
        "title": "abc123",
        "isbn": "0001122223334",
        "author": { "last": "zzz", "first": "aaa" },
        "copies": 5,
        }]
    col.insert(data)
    
def include_specific_fields_in_output_documents():
    """只输出title和author两个field
    """
    res = col.aggregate([
        {
            "$project": {
                "full_title": "$title", "author": 1, # 将title的field name换成full_title
                }
        }
        ])
    for doc in res:
        print(doc)

def suppress_id_field():
    """跟上例一样, 只不过抛弃掉_id项
    """
    res = col.aggregate([
        {
            "$project": {
                "_id": 0, "title": 1, "author": 1,
                }
        }
        ])
    for doc in res:
        print(doc)
        
def include_computed_fields():
    """对文档进行计算之后输出。本例中主要将isbn拆分为了几个子field。
    关于string aggregation operations, 请参考:
        http://docs.mongodb.org/manual/reference/operator/aggregation-string/
    """
    res = col.aggregate(
        [
            {
                "$project": {
                    "title": 1,
                    "isbn": {
                        "prefix": { "$substr": [ "$isbn", 0, 3 ] },
                        "group": { "$substr": [ "$isbn", 3, 2 ] },
                        "publisher": { "$substr": [ "$isbn", 5, 4 ] },
                        "title": { "$substr": [ "$isbn", 9, 3 ] },
                        "checkDigit": { "$substr": [ "$isbn", 12, 1] }
                    },
                "lastName": "$author.last",
                "copiesSold": "$copies",
                }
            }
        ]
    )
    
    for doc in res:
        ppt(doc)
        
if __name__ == "__main__":
    prepare_data()
    include_specific_fields_in_output_documents()
#     suppress_id_field()
#     include_computed_fields()
    client.close()