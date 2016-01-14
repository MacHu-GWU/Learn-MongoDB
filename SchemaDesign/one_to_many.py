#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
one-to-many是指一对多中的多数量通常比较多但不是很多情况。例如:一个汽车企业中, 
一个product可能会用到许多parts。

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

products = test.__getattr__("products")
parts = test.__getattr__("parts")

def insert_test_data():
    products.remove()
    parts.remove()
    
    fake = faker.Factory.create()
    n_product = 20 
    n_part = 100
    
    parts_data = [
        {
            "_id": i + 1,
            "partno": fake.ean(),
            "name": fake.word(),
            "vendor": fake.company(),
            "price": random.randint(1, 10000) * 0.01,
        } for i in range(n_part)
    ]
    parts.insert(parts_data)
    
    products_data = [
        {
            "_id": i + 1,
            "name": fake.word(),
            "manufacturer": fake.company(),
            "parts": [
                part_doc["_id"] for part_doc in random.sample(
                    parts_data, random.randint(5, 40))
            ],
        } for i in range(n_product)
    ]
    products.insert(products_data)
    
    return products_data, parts_data
#     pprint(parts_data[0])
#     pprint(products_data[0])
    
def find_all_parts_for_particular_product():
    """获得一个product的所有parts, 需要使用application-level join。
    """
    st = time.clock()
    product = products.find_one({"_id": 1})
    product_parts = list(parts.find({
        "_id": {"$in": product["parts"]}
    }, {"_id": 1, "name": 1}))
    pprint(product_parts) 
    print("find all parts for particular product takes %.6f" % (time.clock() - st,))

def find_all_products_for_particular_part():
    """获得被用到某个part的所有products, 需要使用array operator。
    """
    st = time.clock()
    part_products = list(products.find({
        "parts": {"$all": [1,]}
    }, {"parts": 0}))
    pprint(part_products)
    print("find all products for particular part takes %.6f" % (time.clock() - st,))
    
def find_products_using_any_of_bad_parts():
    """假设某个零件供应商vendor出了诚信危机, 那么很可能该vendor供应的所有part
    都有问题。那么此时我们想知道, 哪些product用了这些潜在有问题的part。
    """
    vendor = parts_data[0]["vendor"] # 随便找一个vendor
    part_id_list = [part["_id"] for part in parts.find({"vendor": vendor}, 
                                                       {"_id": 1})]
    filter = {"$or": [{"parts": part_id} for part_id in part_id_list]}
    for product in products.find(filter):
        print(product)
    
if __name__ == "__main__":
    products_data, parts_data = insert_test_data()
    
    find_all_parts_for_particular_product()
  
    find_all_products_for_particular_part()

    find_products_using_any_of_bad_parts()