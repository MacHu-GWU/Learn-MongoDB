##encoding=utf-8

"""


"""

from connect import client, db, col
from pprint import pprint as ppt
import random
import time

def prepare_data():
    col.drop()
    data = [{ "_id" : 1, "item" : "ABC1", "sizes": [ "S", "M", "L"] }]
    col.insert(data)
    
def example():
    """将$sizes拆分, 然后将field name替换成size
    """
    for doc in db.col.aggregate([
            {"$unwind": "$sizes"},
            {"$project": {"item": 1, "size": "$sizes"}},
            ]):
        print(doc)
        
if __name__ == "__main__":
#     prepare_data()
    example()