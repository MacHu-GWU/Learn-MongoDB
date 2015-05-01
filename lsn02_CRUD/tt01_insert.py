##encoding=utf-8

"""
基本的insert语法
"""
from tt00_connect import client, db, users
from angora.GADGET.pytimer import Timer
from angora.STRING.formatmaster import fmter

timer = Timer()
users.remove({})

documents1 = [
    {"name": "Bill Gates", "lastname": "Bill", "firstname": "Gates",
     "profile": {"year": 1955, "money": 700}},
    {"name": "Steve Jobs", "lastname": "Steve", "firstname": "Jobs",
     "profile": {"year": 1955, "money": 69}},
    {"name": "Elon Musk", "lastname": "Elon", "firstname": "Musk",
     "profile": {"year": 1971, "money": 103}},
    ]
documents2 = [
    {"name": "Obama", "nation": "USA", "money": None},
    {"name": "Churchill", "nation": "Egnland", "money": None},
    {"name": "Bin laden", "nation": "Pakistan", "money": None},
    ]

users.insert(documents1) # list of dict 一口气插入, 其中当然不能有_id重复
for doc in documents2: # 用 for loop 一个个插入
    users.insert(doc)
    
users.insert({"_id": 1, "value": "apple"})
try:
    users.insert({"_id": 1, "value": "orange"})
except Exception as e: # 部
    print(e)
for doc in users.find():
    print(doc)

"""关于一口气插入和分次插入的性能区别:
mongo在为插入的对象创建

"""
# documents3 = [{"name": fmter.tpl.randstr(1)} for i in range(1000000)]
# timer.start()
# users.insert(documents3)
# timer.timeup()

# documents4 = [{"name": fmter.tpl.randstr(1)} for i in range(1000000)]
# timer.start()
# for doc in documents4:
#     users.insert(doc)
# timer.timeup()