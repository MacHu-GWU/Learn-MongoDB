#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
one-to-few是指一对多中的多数量通常很小的情况。例如:一个person可能有多个address。

schema::
    
    >>> person.find_one()
    
    {'_id': ObjectId('568ec7820080d41c282b098e'),
     'address': [{'city': 'Nallelymouth',
                  'country': 'Swaziland',
                  'state': 'Rhode Island',
                  'street': '0983 Mann Turnpike'},
                 {'city': 'West Fleeta',
                  'country': 'Russian Federation',
                  'state': 'California',
                  'street': '67973 Swift Mountains'},
                 {'city': 'Lake Felisha',
                  'country': 'Israel',
                  'state': 'Arizona',
                  'street': '8916 Becker Shore Suite 857'}],
     'name': 'Monique King DVM',
     'ssn': '019-66-1721'}

pro:

- 所有的数据包含在了一个document中, 一次查询即可获得所有数据

con:

- 对embedded document中的项查询无法利用索引
- 对embedded document的查询很不方便, 例如在: 一个person有多个task, task有
  due time。那么当查询 "在明天due的所有task" 就不是很方便, 在别的设计中完全可以
  更简单
- 由于16MB Size限制, embedded document的数量不可以太多
"""

from __future__ import print_function, unicode_literals
from database import test
from pprint import pprint
import faker, random
import time

person = test.__getattr__("person")

def insert_test_data():
    person.remove()
    
    fake = faker.Factory.create()
    n_person = 1000
    person_data = [
        {
            "name": fake.name(),
            "ssn": fake.ssn(),
            "address": [
                {
                    "street": fake.street_address(),
                    "city": fake.city(),
                    "state": fake.state(),
                    "country": fake.country(),
                } for i in range(random.randint(1, 3))
            ],
        } for i in range(n_person)
    ]
    person.insert(person_data)

    pprint(person_data[0])
    
def find_person():
    """对非embedded field做查询。
    """
    filter = {"name": {"$regex": "^A"}}
    st = time.clock()
    for doc in person.find(filter):
        pprint(doc)
        pass
    print("using field takes %.6f" % (time.clock() - st,))
    
def find_person_by_state():
    """对embedded document中的field做query, 无法利用index, 也很不方便直观。
    """
    filter = {
        "address.state": "New York"
    }
    st = time.clock()
    for doc in person.find(filter):
        pprint(doc)
        pass
    print("using field in embedded document takes %.6f" % (time.clock() - st,))

if __name__ == "__main__":
    insert_test_data()
    
    find_person()

    find_person_by_state()