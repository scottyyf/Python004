#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: mysql_test.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import pymysql.cursors

dbinfo = {
    'host': '192.168.4.245',
    'port': 3306,
    'user': 'root',
    'password': 'my-secret-pw',
    'db': 'mysql'
    }

sql = ['select * from users']
# sql = ["INSERT INTO users (email, password) VALUES (%s, %s)"]
# data = [('webmaster@python.org', 'test' + str(i)) for i in range(11, 30)]

result = []


class ConnDB:
    def __init__(self, dbinfo: dict, sql: list):
        self.host = dbinfo.get('host', 'localhost')
        self.port = dbinfo.get('port')
        self.pw = dbinfo.get('password')
        self.db = dbinfo.get('db')
        self.user = dbinfo.get('user')
        self.sqls = sql

    def run(self):
        conn = pymysql.connect(host=self.host,
                               user=self.user,
                               password=self.pw,
                               database=self.db,
                               port=self.port,
                               bind_address='192.168.4.175',
                               read_timeout=20,
                               write_timeout=20,
                               connect_timeout=8,
                               charset='utf8mb4',
                               )
        cur = conn.cursor()
        try:
            for cmd in self.sqls:
                print(f'get info count: {cur.mogrify(cmd)}')
                cur.execute(cmd)
                # cur.executemany(cmd, data)
                result.append(cur.fetchone())

            cur.close()
            conn.commit()
        except ValueError:
            print('xxx')
            conn.rollback()
            pass

        if conn.open:
            conn.close()

        # conn.ping(True)
        # print(conn.open)
        print(result)

        # excutemany TODO


if __name__ == '__main__':
    conn_db = ConnDB(dbinfo, sql)
    conn_db.run()
