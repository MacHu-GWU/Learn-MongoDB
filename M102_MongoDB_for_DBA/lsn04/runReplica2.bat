cd C:\Program Files\MongoDB\Server\3.0\bin
mongod --port 27002 --replSet abc --dbpath D:\data\db2 --logpath D:\data\log.2 --logappend --oplogSize 50 --smallfiles
pause