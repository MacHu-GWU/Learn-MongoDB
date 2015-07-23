##encoding=utf-8

from faker import Factory
from pymongo import MongoClient
from bson.code import Code
from angora.GADGET import *
from pprint import pprint as ppt

timer = Timer()
client = MongoClient("localhost", 27017)
db = client.test
article = db.article


def create_test_data():
    fake = Factory.create("en_US")
    data = [{"text": fake.paragraph()} for i in range(10000)]
    article.drop()
    article.insert(data)
    
create_test_data()

def non_map_reduce():
    result = dict()
    for doc in article.find():
        text = doc["text"]
        for word in text.split(" "):
            word = word.lower()
            if word in result:
                result[word] += 1
            else:
                result[word] = 1
    return result

timer.start()
result = non_map_reduce()
timer.timeup()
# for key, value in result.items():
#     print(key, value)

def map_reduce():
    mapper = Code(
        """
        function() {
        var text = this.text;
            if (text) {
                var wordlist = text.toLowerCase().split(" ");
                wordlist.forEach(function(word) {
                    if (word) {
                        emit(word, 1);
                        }
                });
            }
        }
        """    
        )
    
    reducer = Code(
        """
        function(key, values) {
            var count = 0;
            values.forEach(function(v) {
                count += v;
            });
            return count;
        }
        """
        )
    myresults = article.map_reduce(mapper, reducer, "myresults")
#     for doc in myresults.find():
#         print(doc)

timer.start()
map_reduce()
timer.timeup()