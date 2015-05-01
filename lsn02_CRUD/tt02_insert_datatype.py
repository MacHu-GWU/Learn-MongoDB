from tt00_connect import client, db, users
from angora.GADGET.pytimer import Timer
from angora.STRING.formatmaster import fmter
from datetime import datetime, date

timer = Timer()
users.remove({})

"""
mongodb doesn't support date object and only accept datetime. you have to convert
date to datetime using datetime.combine(date_object, datetime.min.time()) to
normalize to midnight.
"""

document = {"create_datetime": datetime.now(), 
            "release_date": datetime.combine(date.today(), datetime.min.time())}
users.insert(document)

for doc in users.find():
    print(doc)