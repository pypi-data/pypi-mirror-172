#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from .sqlite_help import sqliteDB


class tmpDB():

    def __init__(self, dbname=":memory:"):
        """
        初始化函数，创建数据库连接
        :param dbnmae: 传入数据库名称或数据库文件路径，eg: test.db 或 :memory:
        """
        if not os.path.exists(dbname) or dbname == ":memory:":
            self.db = sqliteDB(
                dbname, ['CREATE TABLE tmp (key TEXT NOT NULL,value TEXT NOT NULL);'])
        else:
            self.db = sqliteDB(dbname)

    def get(self, key):
        result = self.db.get("select value from tmp where key=?", [key, ])
        if len(result) == 0:
            return
        else:
            return result[0][0]

    def set(self, key, value):
        result = self.db.get("select value from tmp where key=?", [key, ])
        if len(result) == 0:
            return self.db.set('INSERT INTO tmp (key,value) VALUES (?,?)', [key, value])
        else:
            return self.db.set('UPDATE tmp set value = ? where key=?', [value, key])

    def remove(self, key):
        return self.db.set("DELETE from tmp where key=?", [key, ])


if __name__ == '__main__':
    pass
    db = tmpDB()
    db.set('a', 'a')
    db.set('a', 'b')
    db.set('c', 'c')
    print(db.get('a'))
    print(db.get('b'))
    print(db.get('c'))
    db.remove('c')
    print(db.get('c'))
