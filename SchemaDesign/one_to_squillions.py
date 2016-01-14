#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
one-to-squillion是指一对多中的多数量通常极多的情况。例如:一个log系统中, 
一个host上可能有几百万条log, 这样即使只存_id, 也可能存不下。

schema::
    
    >>> hosts.find_one()
    
    {'_id': 1, 'ipaddr': '199.49.248.44', 'name': 'http://damorelarson.com/'}
    
    >>> logs.find_one()

    {'_id': ObjectId('568ed9460080d430a02280bd'),
     'host_id': 3,
     'msg': 'Cumque inventore sed voluptatem doloremque eaque aperiam.',
     'time': datetime.datetime(2016, 1, 7, 16, 31, 50, 445462)}

pro:


con:

- 从one视角做查询时性能不会很高

"""

from __future__ import print_function, unicode_literals
from database import test
from pprint import pprint
import faker, random
import time, datetime

hosts = test.__getattr__("hosts")
logs = test.__getattr__("logs")

def insert_test_data():
    hosts.remove()
    logs.remove()
    
    fake = faker.Factory.create()
    n_host = 3 
    n_log = 1000
    
    host_data = [
        {
            "_id": i + 1,
            "name": fake.url(),
            "ipaddr": fake.ipv4(),
        } for i in range(n_host)
    ]
    
    logs_data = [
        {
            "time": datetime.datetime.now(),
            "msg": fake.sentence(),
            "host_id": random.randint(1, n_host), 
        } for i in range(n_log)
    ]
    hosts.insert(host_data)
    logs.insert(logs_data)
    
#     pprint(host_data[0])
#     pprint(logs_data[0])
    
def find_last_10_msg():
    """获得一个host上最新的10条logs, 需要使用application-level join。
    """
    st = time.clock() 
    last_10_msg = list(
        logs.find({"host_id": 1}).sort([("time", -1)]).limit(10)
    )
    pprint(last_10_msg)
    print("find last 10 log message for particular host takes %.6f" % (time.clock() - st,))
    
if __name__ == "__main__":
    insert_test_data()
    
    find_last_10_msg()