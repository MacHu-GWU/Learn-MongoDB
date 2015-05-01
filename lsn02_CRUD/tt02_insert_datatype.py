##encoding=utf-8

"""
Mongodb所支持的数据类型, 以及和python中对象的兼容性测试
string, int, float无需测试
"""

from tt00_connect import client, db, users
from angora.GADGET.pytimer import Timer
from angora.STRING.formatmaster import fmter
from angora.DATA.pk import obj2bytestr, obj2str
from datetime import datetime, date

timer = Timer()

def can_key_be_other_than_string():
    """json file cannot have key other than string. So you cannot use integer as a key, even it
    is valid in python dictionary.
    In addition, choose key string wisely can save space.
    """
    document = {1: "a"}
    users.insert(document)
    for doc in users.find():
        print(doc)

# can_key_be_other_than_string()

def date_and_datetime_type():
    """
    mongodb doesn't support date object and only accept datetime. you have to convert
    date to datetime using datetime.combine(date_object, datetime.min.time()) to
    normalize to midnight.
    """
    document = {"create_datetime": datetime.now(), 
                "create_date": datetime.combine(date.today(), datetime.min.time())}
    users.insert(document)
    for doc in users.find():
        print(doc)
        
# date_and_datetime_type()

def boolean_and_none_type():
    """{key: None} means key == None or key is not existing
    """
    documents = [{"is_valid": True}, {"is_valid": False}, {"is_valid": None}]
    users.insert(documents)
    
    fmter.tpl._straightline("is_valid == True", 100)
    for doc in users.find({"is_valid": True}):
        print(doc)
        
    fmter.tpl._straightline("is_valid == False", 100)
    for doc in users.find({"is_valid": False}):
        print(doc)
        
    fmter.tpl._straightline("is_valid is null", 100)
    for doc in users.find({"is_valid": None}):
        print(doc)

    fmter.tpl._straightline("is_valid not null", 100)
    for doc in users.find({"is_valid": {"$ne": None}}):
        print(doc)
        
# boolean_and_none_type()

def bytes_type():
    """mongodb support bytes, which means you can use pickle to dump anything into mongodb.
    But! Don't forget the maximum BSON document size is 16 megabytes
    """
    documents = [
        {"pickle": "hello world".encode("utf-8")},
        {"pickle": obj2bytestr(set([1,2,3]))},
        ] 
    users.insert(documents)
    
    for doc in users.find():
        print(doc)
        
# bytes_type()

def list_and_set_type():
    documents = [
        {"list": [1,2,3]},
        {"set": set([1,2,3])}, # this cannot be done
        ]
    
    users.insert(documents)
    
    for doc in users.find():
        print(doc)
        
# list_and_set_type()