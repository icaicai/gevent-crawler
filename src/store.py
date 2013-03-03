#coding=utf8

from pymongo import MongoClient




class Store(object):
    """docstring for Store"""
    def __init__(self):
        super(Store, self).__init__()
        self._init_db()

    def _init_db(self):
        self._conn = MongoClient(use_greenlets=False, max_pool_size=10)
        self._db = self._conn.dbgoods

    def get_collection(self, name):
        return self._db[name]

store = Store()
