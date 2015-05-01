##encoding=utf-8

"""
from tt00_connect import client, db, users
"""

from pymongo import MongoClient
from datetime import datetime, date

client = MongoClient('localhost', 27017)
db = client.test
users = db.users
users.remove({})
documents = [
    {"_id": 1, "name": "sanhe", "age": 27, "height": 178.3, "enroll_date": datetime(2014, 10, 13),
     "title": "Data Scientist",
     "skillset": ["python", "machinelearning", "cSharp", "database", "modeling"],
     "profile": {"eye_color": "black", "enthnicity": "asian", "hobby": "photograph"},
     "projects": ["HVAC performance alert", "Setpoint ranking"],},

    {"_id": 2, "name": "michael", "age": 28, "height": 185.4, "enroll_date": datetime(2011, 7, 5),
     "title": "Senior Reseacher",
     "skillset": ["excel", "modeling", "cSharp", "mechanical engineer"],
     "profile": {"eye_color": "brown", "enthnicity": "american", "favorite color": "black"},
     "Marital status": 0,},
             
    {"_id": 3, "name": "rama", "age": 32, "height": 171.7, "enroll_date": datetime(2013, 1, 6),
     "title": "Software Engineer",
     "skillset": ["cSharp", "software development", "web development"],
     "profile": {"eye_color": "black", "enthnicity": "indian", "sport": "pool"},
     "Marital status": 1,},
    ]
users.insert(documents)

if __name__ == "__main__":
    print(client.database_names()) # 打印所有的databases
    print(db.collection_names()) # 打印所有的collections