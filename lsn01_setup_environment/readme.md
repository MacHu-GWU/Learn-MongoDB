##下载安装MongoDB

到https://www.mongodb.org/下载windows安装包。 如果安装的是64位版本, 则安装目录默认为:

	C:\Program Files\MongoDB

##启动MongoDB

首先CD到bin目录下:

	C:\Program Files\MongoDB\Server\3.0\bin

在C盘根目录下创建C:\data\db, 之后mongodb的文件则会自动储存在这个目录下。如果你想将文件指定到其他目录下, 启动mongod时加上 --dbpath参数。更多信息请参考详细参数说明([戳这里](http://docs.mongodb.org/manual/reference/program/mongod/#cmdoption--dbpath))。

输入下面的命令启动mongodb服务:

	mongod.exe

然后用户就可以用自带的shell(其实是javascript shell)来操作mongodb了。 当然也可以使用其他客户端软件, 比如python中的pymongo。 输入下面的命令启动mongo shell:

	mongo.exe

##MongoDB基本概念

在MongoDB中最大的概念是database。 相当于SQL中的database。 下一级的概念是collections, 相当于SQL中的table。 再下一级的概念是document, 相当于record。

database有关命令:

显示目前可用的所有database

	show dbs

切换database

	use #database_name

显示当前正在使用的database

	db

collections有关的命令:

显示目前可用的所有collections

	show collections

在collection中进行操作

	db.#collection_name.#method_name(*arguments)