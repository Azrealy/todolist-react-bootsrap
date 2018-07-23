# -*- coding: utf-8 -*-
import psycopg2
# % DB_NAME=test DB_USER_NAME=testuser DB_USER_PASS=testpass yarn db-init

with psycopg2.connect(database='postgres', user='postgres') as con:
    with con.cursor() as cur:
        with open('init_table.sql', 'r') as sqldata:
            cur.execute(sqldata.read())
            cur.execute("SELECT * FROM  todo_list;")
            for i in cur.fetchall():
                print(i)