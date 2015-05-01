##encoding=utf-8

from angora.SQLITE import *
from pymongo import MongoClient
from datetime import datetime
client = MongoClient('localhost', 27017)
db = client.test

metadata = MetaData()
engine = Sqlite3Engine(r"C:\HSH\Workspace\py33\py33_projects\AVRabbit\av.db")
metadata.reflect(engine)
av = metadata.tables["av"]

pipeline = list()
for row in engine.select_row(Select(av.all)):
    row = row.to_dict()
    row["_id"] = row["uuid"]
    del row["uuid"]
    row["artists"] = list(row["artists"])
    row["tags"] = list(row["tags"])
    try:
        row["release_date"] = datetime.combine(row["release_date"], datetime.min.time())
    except:
        pass
    pipeline.append(row)
db.av.insert(pipeline)

query = {"avid": {"$regex": r"IPZ-*"}}
query = {
         "$and": [
                  {"tags": {"$elemMatch": {"$eq": "单体作品"}}}, 
                  {"tags": {"$elemMatch": {"$eq": "女教师"}}},
                  ]
         }
results = list(db.av.find(query))

for doc in results:
    print(doc["tags"])
print(len(results))