#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
我们以task tracking system为例:

如果使用了two-way-referencing, 当然你从两种object的视角都能享受referencing的
benefit。但是请注意, 每当你要修改一个task和person的关系时, 你必须执行两个update。
而这意味着, **无法在一个atomic(原子操作)** 内完成这个update。
"""

from __future__ import print_function, unicode_literals
from database import test
from pprint import pprint
import pymongo
import faker, random
import time

person = test.__getattr__("person")
tasks = test.__getattr__("tasks")

def insert_test_data():
    person.remove()
    tasks.remove()
    
    fake = faker.Factory.create()
    n_person = 5
    n_task = 10

    person_data = list()
    tasks_data = list()
    
    task_id = 0
    for i in range(n_person):
        _person = {
            "_id": i + 1,
            "name": fake.name(),
            "tasks": list(),
        }
        
        for i in range(random.randint(1, 3)):
            task_id += 1
            task = {
                "_id": task_id,
                "description": fake.sentence(),
                "due_date": fake.date_time(),
                "owner": _person["_id"],
            }
            _person["tasks"].append(task["_id"])
            tasks_data.append(task)
        
        person_data.append(_person)

    person.insert(person_data)
    tasks.insert(tasks_data)
    
#     pprint(person_data[0])
#     pprint(task_data[0])

def find_my_first_due_task():
    """获得一个人的所有任务中最先due的那个。
    """
    st = time.clock()
    task = tasks.find({"owner": 1}).sort("due_date", pymongo.DESCENDING).limit(1)[0]
    print("find my first due task takes %.6f" % (time.clock() - st,))
    
if __name__ == "__main__":
    insert_test_data()
    
    find_my_first_due_task()