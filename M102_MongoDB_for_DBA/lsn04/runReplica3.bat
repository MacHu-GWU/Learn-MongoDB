cd C:\Program Files\MongoDB\Server\3.0\bin
mongod --port 27003 --replSet abc --dbpath D:\data\db3 --logpath D:\data\log.3 --logappend --oplogSize 50 --smallfiles
pause