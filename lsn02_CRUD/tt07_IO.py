##encoding=utf-8

"""
Mongodb backup, restore:
    http://docs.mongodb.org/manual/reference/program/#binary-import-and-export-tools
    
Mongodb内置了4个工具可以帮助我们备份和恢复数据库:
    1. mongoimport, 将json文件导入数据库, 将纯json数据导入数据库
    2. mongoexport, 将数据库导出为json, 不包括metadata, Index
    3. mongodump, 将数据导出为bson, 并且带metadata, 包括Index
    4. mongorestore, 从bson文件恢复数据库, 包括Index

    具体使用方法是:
    1. mongoimport path
    
    2. mongoexport:
        mongoexport --db dbname --collection collection_name --out path
        这样做会生成一个json文件。请注意如果你将软件安装在了windows下, mongodb会被默认安装到
        windows/program目录下, 这个目录下你不一定会拥有写权限。所以指定一个外部的绝对路径是上策
        
    3. mongodump:
        mongodump --db dbname --collection collection_name --out path
    
    4. mongorestore:
        mongorestore path
"""

