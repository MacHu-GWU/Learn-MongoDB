#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
one-to-many是指一对多中的多数量通常比较多但不是很多情况。例如:一个电商系统中, 
一个item可能会用到许多tag, 但一个item可能有的tag不会太多。总共的item肯定是远远
多于tag数的。但是item和tag数量都会比较大。

schema::
    
    >>> parts.find_one()
    
    {'_id': 1, 'name': 'id', 'partno': '7488444825756', 'price': 78.87}
    
    >>> products.find_one()
    
    {'_id': 1,
     'manufacturer': 'Flatley-Koch',
     'name': 'dolorum',
     'parts': [71,
               100,
               etc...,
               87]}

pro:

- 潜在地实现了many-to-many。从one-to-many中的many视角查询时, 只需要使用array
  operation query即可。

con:

- 从one的视角查询时, 只能获得many对象的primary_key, 如果需要获得完整的many对象,
  需要再做一次application-level join查询。
"""

from __future__ import print_function, unicode_literals
from database import test
from pprint import pprint
import faker, random
import time

items = test.__getattr__("items")
tags = test.__getattr__("tags")

def insert_test_data():
    items.remove()
    tags.remove()
    
    fake = faker.Factory.create()
    n_items = 100 
    n_tags = 100

    tags_data = [
        {
            "_id": i + 1,
            "name": fake.word(),
        } for i in range(n_tags)
    ]

    items_data = [
        {
            "_id": i + 1,
            "name": fake.word(),
            "tags": [tag["_id"] for tag in random.sample(tags_data, random.randint(1, 5))]
        } for i in range(n_items)
    ]
    
    items.insert(items_data)
    tags.insert(tags_data)    
    
#     pprint(items_data[0])
#     pprint(tags_data[0])
    
def find_all_tag_associated_with_an_item():
    """获得一个item的所有tags, 需要使用application-level join。
    """
    st = time.clock()
    item = items.find_one({"_id": 1})
    item_tags = list(tags.find({
        "_id": {"$in": item["tags"]}
    }))
    pprint(item_tags) 
    print("find all tag asoociated with an item takes %.6f" % (time.clock() - st,))

def find_all_item_associated_with_an_tag():
    """获得被用到某个part的所有products, 需要使用array operator。
    """
    st = time.clock()
    part_products = list(products.find({
        "parts": {"$all": [1,]}
    }, {"parts": 0}))
    pprint(part_products)
    print("find all products for particular part takes %.6f" % (time.clock() - st,))
    
if __name__ == "__main__":
    insert_test_data()
    
    find_all_tag_associated_with_an_item()
#  
#     find_all_products_for_particular_part()