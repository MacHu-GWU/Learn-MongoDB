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

#############
# In python #
#############

def absolute_update():
    """collection.update()语法分两部分, 第一部分是定位到需要修改的document, 第二部分是对值
    进行设定。
    注意:
        使用 "$set": {key: value} 只会对key的部分进行修改, 如果使用:
        users.update({"_id": 1}, {"name": "obama"}), 则会将整个文档替换成 {"name": "obama"}
    """
    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 1})[0])
    ppt(users.find({"_id": 2})[0])
    users.update({"_id": 1}, {"$set": {"name": "obama", # update name field
                                       "profile.enthnicity": "african american"}}) # access child
    users.update({"name": "michael"}, {"age": 100}) # replace whole document, only keep _id
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 1})[0])
    ppt(users.find({"_id": 2})[0])

# absolute_update()

def update_without_set():
    """若不使用collection.update(query, {"$set": {key: value}), 而使用:
        collection.update(query, new_document)
    则会将所有定位到的document替换成, new_document
    """
    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 1})[0])
    users.update({"_id": 1}, {"_id": 1}) # replace the whole document with the new one
    
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 1})[0])
    
# update_without_set()

def relative_update():
    """在Sql中有 set column_name = column_name + 1 这种相对更新的方法。在mongodb中我们的做法是:
        1. 使用$inc, $mul等操作符: http://docs.mongodb.org/manual/reference/operator/update-field/
        2. 首先find()找到document, 然后修改document对象, 最后再collection.save(document)保存改动。
    """
    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 1})[0])  
    doc = users.find_one({"_id": 1}) # find the document
    doc["age"] += 30 # do some change to the document
    users.save(doc) # save changes into collections
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 1})[0])

    fmter.tpl._straightline("before", 100)
    ppt(users.find({"_id": 2})[0])  
    users.update({"_id": 2}, {"$inc": {"age": 30}})
    fmter.tpl._straightline("after", 100)
    ppt(users.find({"_id": 2})[0])
    
# relative_update()

def upsert_example():
    """upsert的意思是: 首先尝试update, 如果找不到该文档, 则insert改文档
    """
    users.update({"name": "obama"}, {"$set": {"name": "obama"}}, upsert=True)
    fmter.tpl._straightline("after", 100)
    for doc in users.find({"name": "obama"}):
        ppt(doc)
        
# upsert_example()

def insept_example():
    """insept的意思是: 首先尝试insert, 如果面临着_id重复问题, 则update
    该逻辑可以用upsert实现。注: 有时候document是没有包含_id项的
    """
    doc = {"_id": 1, "name": "obama", "new_field": 999}
    try:
        users.insert(doc)
    except:
        _id = doc["_id"]
        del doc["_id"]
        users.update({"_id": _id}, {"$set": doc}, upsert=True)

    ppt(users.find({"name": "obama"})[0])
        
# insept_example()