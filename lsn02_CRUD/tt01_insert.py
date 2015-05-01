##encoding=utf-8

"""
基本的insert语法。insert性能初探
"""

from tt00_connect import client, db, users
from angora.GADGET.pytimer import Timer
from angora.STRING.formatmaster import fmter
from datetime import datetime, date

timer = Timer()

def basic_insert_syntax():
    """
    db.collection.insert(one_document) or db.collections.insert(list_of_documents)
    BUT!
        if any document in list_of_documents has _id conflict with existing document,
        then that would be failed. you should use the following code:
        
        for document in list_of_documents:
            try:
                db.collection.insert(document)
            except:
                pass
    """
    documents1 = [
        {"name": "Bill Gates", "lastname": "Bill", "firstname": "Gates",
         "profile": {"year": 1955, "money": 700}},
        {"name": "Steve Jobs", "lastname": "Steve", "firstname": "Jobs",
         "profile": {"year": 1955, "money": 69}},
        {"name": "Elon Musk", "lastname": "Elon", "firstname": "Musk",
         "profile": {"year": 1971, "money": 103}},
        ]
    documents2 = [
        {"_id": 100, "name": "Obama", "nation": "USA", "money": None},
        {"_id": 101, "name": "Churchill", "nation": "Egnland", "money": None},
        {"_id": 101, "name": "Bin laden", "nation": "Pakistan", "money": None}, # 有重复
        ]
 
    users.insert(documents1) # list of dict 一口气插入, 其中当然不能有_id重复
    for doc in documents2: # 用 for loop 一个个插入
        try:
            users.insert(doc)
        except Exception as e:
            print(e)
            
    for doc in users.find():
        print(type(doc), doc) # 默认返回字典, 并非有序字典
            
# basic_insert_syntax()

def reserved_key_id():
    """如果用户不指定_id, 则系统会自动创建一个_id。问题是对于同样内容的文档, 自动生成的_id会不会
    重复呢?
    结论:
        对于内存中不同的对象, mongodb是不会生成重复的_id的。但是如果是同样的对象, 则会生成重复的_id
        test1:
            每一个doc其实是生成了一个新字典。而每次生成了新字典的时候python就将变量名doc绑定
            到新字典上。由于旧字典没有被reference, 那么系统就会自动垃圾回收释放内存了。所以每一次
            doc其实是内存中不同的对象。所以_id不会冲突。
        test2:
            我们生成了一个document的列表。里面每一个元素在内存中其实是不同的。所以_id也不会冲突
        test3:
            我们重复调用了test2中的列表。由于里面每一个元素在内存中的地址是一样的, 所以生成了同样
            的_id, 造成了冲突。
    """
    # test 1
    for i in range(10):
        doc = {"text": "abcdefg"}
        users.insert(doc)
    print(users.find().count())
    
    list_of_documents = [{"text": "abcdefg"} for i in range(10)]
    
    # test 2
    users.insert(list_of_documents)
    print(users.find().count())
    
    # test 3
    for doc in list_of_documents:
        users.insert(doc)
        print(users.find().count())
    
# reserved_key_id()

def bulk_insert():
    """测试bulk insert和一个个insert的性能区别:
    结论:
        Bulk insert的速度要远远快于一条条insert
        
    注: Bulk insert支持生成器模式。
    """
    list_of_documents1 = [{"name": fmter.tpl.randstr(8)} for i in range(1000)]
    def document_generator():
        for doc in list_of_documents1:
            yield doc
    
    timer.start()
    users.insert(document_generator())
    timer.timeup()

    list_of_documents2 = [{"name": fmter.tpl.randstr(8)} for i in range(1000)]
    timer.start()
    for doc in list_of_documents2:
        users.insert(doc)
    timer.timeup()
    
    print(users.find().count())
    
# bulk_insert()