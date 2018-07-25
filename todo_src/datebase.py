# -*- coding: utf-8 -*-
import sqlite3

queries = {
    'CREATE_TABLE': 'CREATE TABLE IF NOT EXISTS {} ({})',
    'INSERT': 'INSERT INTO {} VALUES({})',
    'SELECT_ALL': 'SELECT {} FROM {}',
    'UPDATE': 'UPDATE {} SET {} WHERE {}',
    'DELETE': 'DELETE FROM {} WHERE {}',
    'DROP_TABLE': 'DROP TABLE {}'
}


class Model(object):
    
    def __init__(self, data_file):
        self.db = sqlite3.connect(data_file, check_same_thread=False)
        self.data_file = data_file

    
    def execute(self, query, values=None, commit=False):
        cursor = self.db.cursor()
        if values:
            print(list(values))
            cursor.execute(query, list(values))
        else:
            cursor.execute(query)
        if commit:
            self.db.commit()
        return cursor
    
    def create_table(self, table_name, values):
        query = queries['CREATE_TABLE'].format(table_name, ','.join(values))
        print(query)
        cursor = self.execute(query, commit=True)
        cursor.close()
        
    def insert(self, table_name, *args):
        query = queries['INSERT'].format(table_name, ','.join('?' for _ in args))
        print(args)
        print(query)
        return self.execute(query, args, commit=True)
    
    def select_all(self, table_name):
        query = queries['SELECT_ALL'].format('*', table_name)
        print(query)
        return self.execute(query)
    
    def update_item(self, table_name, set_values, **kwargs):
        updates = ['{}=?'.format(k) for k in set_values]
        update_values = [set_values[k] for k in set_values]
        condition = ['{}=?'.format(k) for k in kwargs]
        condition_values = [kwargs[k] for k in kwargs]

        query = queries['UPDATE'].format(table_name, ', '.join(updates), ' and '.join(condition))
        print(query)
        return self.execute(query, update_values + condition_values, commit=True)

    def delete_item(self, table_name, **kwargs):
        condition = ['{}=?'.format(k) for k in kwargs]
        condition_values = [kwargs[k] for k in kwargs]
        query = queries['DELETE'].format(table_name, 'and '.join(condition))
        print(query)
        return self.execute(query, condition_values, commit=True)

    def drop_table(self, table_name):
        query = queries['DROP_TABLE'].format(table_name)
        print(query)
        return self.execute(query)
        
    def disconnect(self):
        self.db.close()

    def close(self, cursor):
        cursor.close()