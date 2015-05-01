##encoding=utf-8

"""
Mongodb中update语句基础入门
"""

from tt00_connect import client, db, users
from angora.GADGET.pytimer import Timer
from angora.STRING.formatmaster import fmter
from pprint import pprint as ppt
from datetime import datetime, date

timer = Timer()

def unset():
    """移除掉某一个key, 请使用"$unset"
    """
    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 1})[0])
    
    users.update({"_id": 1}, {"$unset": {"profile": 1}})
    
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 1})[0])
    
# unset()

##################
# array operator #
##################
"""Notice, all $operator is case sensitive
"""

def push():
    """在右边添加一项, 相当于list.append(item)
    """
    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 1})[0])
    
    users.update({"_id": 1}, {"$push": {"skillset": "data visualization"}})
    
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 1})[0])
    
# push()

def pop():
    """在右边取出一项, 相当于list.pop()
    """
    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 1})[0])
    
    users.update({"_id": 1}, {"$pop": {"skillset": 1}})
    
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 1})[0])
    
# pop()

def pushAll():
    """在右边加上多项, 相当于 list = list + another_list
    """
    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 1})[0])
    
    users.update({"_id": 1}, {"$pushAll": {"skillset": ["data visualization", "R"]}})
    
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 1})[0])
    
# pushAll()

def pull():
    """删除所有的某项, 相当于 for i in list, if i == pull_item, list.remove(i)
    """
    users.update({"_id": 1}, {"$push": {"skillset": "python"}}) # 先加一个python, 故意添加重复项
    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 1})[0])
    
    users.update({"_id": 1}, {"$pull": {"skillset": "python"}})
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 1})[0]) # 把所有的python, 包括重复项都删除了
    
# pull()

def pullall():
    """删除多项, 相当于 for i in list, if i in [item1, item2, ...], list.remove(i)
    """
    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 1})[0])
    
    users.update({"_id": 1}, {"$pullAll": {"skillset": ["python", "cSharp", "R"]}})
    
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 1})[0])
    
# pullall()

def addToSet():
    """将array当成set来执行set.add(item)操作
    """
    users.update({"_id": 1}, {"$push": {"skillset": "python"}}) # 先加一个python, 故意添加重复项
    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 1})[0])
    
    users.update({"_id": 1}, {"$addToSet": {"skillset": "R"}}) 
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 1})[0]) # 只会在添加的时候将其当成set处理, 并不会把array自动转化为set
    
# addToSet()

"""multi-update
"""

def multiUpdate():
#     users.update({}, {"name": "obama"}) # only one document are updated
    users.update({}, {"$set": {"name": "obama"}}, multi=True) # all document matching where clause are updated
    for doc in users.find():
        ppt(doc)

# multiUpdate()