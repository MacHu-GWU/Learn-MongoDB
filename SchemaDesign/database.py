#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import pymongo

client = MongoClient("localhost", 27017)
test = client.__getattr__("test")