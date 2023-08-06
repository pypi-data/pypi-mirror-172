#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pymysql


class mysqlDB():

    def __init__(self, host='127.0.0.1', port=3306, user='root', password='root', database='test', charset='utf8'):
        """
        初始化函数，创建数据库连接
        """
        self.conn = pymysql.connect(host=host, port=int(
            port), user=user, password=password, database=database, charset=charset)
        self.cursor = self.conn.cursor()

    def set(self, sql, data=[], many=False):
        """
        数据库的插入、修改、删除函数
        :param sql: 传入的SQL语句 eg:INSERT INTO tablename (name) VALUES (%s) / DELETE from tablename where name=%s / UPDATE tablename set name = %s where name=%s
        :param data: 传入对应数据，many=False:[a,b,c,d] many=True:[[a,b,c,d],[a,b,c,d],[a,b,c,d]]
        :param many: 传入批量数据，many=False
        :return: 返回操作数据库状态 eg: True or False
        """
        try:
            if many:
                self.cursor.executemany(sql, data)
            else:
                self.cursor.execute(sql, data)
            i = self.conn.affected_rows()
        except Exception:
            print('fail,sql:{}'.format(sql))
            return False
        finally:
            self.conn.commit()
        if i > 0:
            return True
        else:
            return False

    def get(self, sql, data=[]):
        """
        数据库的查询函数
        :param sql: 传入的SQL语句,eg:select * from tablename where name=%s
        :param data: 传入查询参数,eg: [name,]
        :return : 返回查询结果 eg: [(a,b,)]
        """
        self.cursor.execute(sql, data)
        results = self.cursor.fetchall()
        return results

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.close()
