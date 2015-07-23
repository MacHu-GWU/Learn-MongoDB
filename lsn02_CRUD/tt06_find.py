##encoding=utf-8

"""
Mongodb中如何query. http://docs.mongodb.org/manual/reference/operator/query/
"""

from tt00_connect import client, db, users
from angora.GADGET.pytimer import Timer
from angora.STRING.formatmaster import fmter
from pprint import pprint as ppt
from datetime import datetime, date
import re

timer = Timer()

# comparison operator: $gt, $gte, $lt, $lte, $ne, $eq = {key: value}
fmter.tpl._straightline("""users.find({"age": {"$gt": 30}})""", 150)
ppt(list(
    users.find({"age": {"$gt": 30}})
    ))

fmter.tpl._straightline("""users.find({"age": {"$lt": 30}})""", 150)
ppt(list(
    users.find({"age": {"$lt": 30}})
    ))

# compare datetime, in java script shell, the command to create a datetime object is:
# db.test.insert({"Time" : new ISODate("2012-01-11T03:34:54Z") });
fmter.tpl._straightline("""users.find({"enroll_date": {"$gt": datetime(2014, 6, 1)}}""", 150)
ppt(list(
    users.find({"enroll_date": {"$gt": datetime(2014, 6, 1)}})
    ))

# $in, $nin, in and not in
fmter.tpl._straightline("""users.find({"age": {"$lt": 30}})""", 100)
ppt(list(
    users.find({"age": {"$lt": 30}})
    ))

fmter.tpl._straightline("""users.find({"title": {"$in": ["HR", "Software Engineer"]}})""", 150)
ppt(list(
    users.find({"title": {"$in": ["HR", "Software Engineer"]}})
    ))

fmter.tpl._straightline("""users.find({"title": {"$nin": ["HR", "Software Engineer"]}})""", 150)
ppt(list(
    users.find({"title": {"$nin": ["HR", "Software Engineer"]}})
    ))

# $and, $or, $not, $nor
fmter.tpl._straightline("""users.find({"$and": [{"age": {"$gt": 20}}, {"enroll_date": {"$lt": datetime(2013, 1, 1)}}]})""", 150)
ppt(list(
    users.find({"$and": [{"age": {"$gt": 20}}, {"enroll_date": {"$lt": datetime(2013, 1, 1)}}]})
    ))

# $regex
fmter.tpl._straightline("""users.find({"name": {"$regex": pattern}})""", 150)
ppt(list(
#     users.find({"name": {"$regex": "^Anh", "$options": "i"}})
    users.find({"name": {"$regex": re.compile(r"san*"), "$options": "i"}})
    ))