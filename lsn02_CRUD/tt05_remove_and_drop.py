##encoding=utf-8

"""
Mongodb中如何:
    1. 删除document
    2. 删除整个collection
    3. remove和drop的区别
    
    collecion.remove({})很像find(), 会先query找到匹配的内容, 然后一条条删除之
    而collection.drop()则是删除整个collection.
    如过collection有一些metadata, 例如index, 那么remove({})掉所有的document并不会删除index.
    而drop()则会删除掉这些metadata
"""

from tt00_connect import client, db, users
from angora.GADGET.pytimer import Timer
from angora.STRING.formatmaster import fmter
from pprint import pprint as ppt
from datetime import datetime, date

timer = Timer()

timer.start()
users.remove({})
# users.drop()
timer.timeup()

for doc in users.find():
    print(doc)
