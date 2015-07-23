cd C:\Program Files\MongoDB\Server\3.0\bin
mongod --port 27001 --replSet abc --dbpath D:\data\db1 --logpath D:\data\log.1 --logappend --oplogSize 50 --smallfiles
pause