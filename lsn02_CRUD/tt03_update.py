##encoding=utf-8

"""
Mongodb所支持的数据类型, 以及和python中对象的兼容性测试
string, int, float无需测试
"""

from tt00_connect import client, db, users
from angora.GADGET.pytimer import Timer
from angora.STRING.formatmaster import fmter
from angora.DATA.pk import obj2bytestr, obj2str
from datetime import datetime, date

timer = Timer()