##encoding=utf-8

from tt00_connect import client, db, users
from angora.STRING.formatmaster import fmter
from pprint import pprint as ppt
import pymongo

def find_one():
    """instead of return a cursor object, find_one() returns one document. so when you look up
    document by it's _id (_id field is always unique), use find_one() method.
    """
    fmter.tpl._straightline("one document", 100)
    result = users.find_one({})
    print(type(result))
    ppt(result)
    
    fmter.tpl._straightline("none result", 100)
    result = users.find_one({"_id": 100})
    print(type(result))
    ppt(result)
    
# find_one()

def dot_notation():
    """because document can be nested, so you can use field.sub_field.subfield. ... to access
    children fields
    """
    ppt(list(
        users.find({"profile.enthnicity": "asian"})
        ))
    
# dot_notation()

def sort():
    """notice, in mongo java script shell, we use: sort({"field1", 1, "field2", -1}), 1 means asc,
    -1 means des
    """
    ppt(list(
        users.find().sort("profile.enthnicity", pymongo.ASCENDING)
        ))
    
# sort()

def skip_and_limit():
    """跳过前n个, 只返回n条
    """
    ppt(list(
        users.find().skip(1).limit(1)
        ))

# skip_and_limit()