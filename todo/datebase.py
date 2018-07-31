# -*- coding: utf-8 -*-
import sqlite3
import os

queries = {
    'CREATE_TABLE': 'CREATE TABLE IF NOT EXISTS {} ({})',
    'SELECT': 'SELECT {} FROM {} WHERE {}',
    'INSERT': 'INSERT INTO {} ({}) VALUES({})',
    'SELECT_ALL': 'SELECT {} FROM {} {}',
    'UPDATE': 'UPDATE {} SET {} WHERE {}',
    'DELETE': 'DELETE FROM {} WHERE {}',
    'DROP_TABLE': 'DROP TABLE {}'
}

class Model(object):
    
    def __init__(self, data_file):
        """
        DB model class, which use to create/execute
        SQL statement and create connection with DB.
        """
        self.db = sqlite3.connect(data_file, check_same_thread=False)
        self.data_file = data_file

    
    def execute(self, query, values=None, commit=False):
        """
        Execute SQL statement.

        Parameters
        ----------
        query : str
            SQL statement
        values : list
            Values of SQL statement
        commit : bool
            Determine if need commit DB

        Returns
        -------
        cursor : sqlite3.Cursor
            An instance of Cursor object
        """
        cursor = self.db.cursor()
        if values:
            cursor.execute(query, list(values))
        else:
            cursor.execute(query)
        if commit:
            self.db.commit()
        return cursor
    
    def create_table(self, table_name, values):
        """
        Execute create table SQL statement.

        Example of SQL statement:
            CREATE TABLE IF NOT EXISTS table_name (
                column1 datetype,
                column2 datetype,
                ...
            )

        Parameters
        ----------
        table_name : str
            Table name
        values : list
            List of every column value.
        """
        query = queries['CREATE_TABLE'].format(table_name, ','.join(values))
        cursor = self.execute(query, commit=True)
        cursor.close()

    def select(self, table_name, **kwargs):
        """
        Execute select SQL statement.

        Example of SQL statement:
            SELECT * FROM table_name;
            WHERE columns1 = ? and columns2 = ? and ..;

        Parameters
        ----------
        table_name : str
            Table name
        """
        conds = ' and '.join(['{}=?'.format(k) for k in kwargs])
        values = [kwargs[k] for k in kwargs]
        query = queries['SELECT'].format('*', table_name, conds)
        return self.execute(query, values)

    def insert(self, table_name, **kwargs):
        """
        Execute insert SQL statement.

        Example of SQL statement:
            INSERT INTO table_name (columns1, column2, ...);
            VALUES (?, ?, ...);

        Parameters
        ----------
        table_name : str
            Table name
        """
        args = ','.join('?' for _ in kwargs)
        parameter = ','.join([k for k in kwargs])
        query = queries['INSERT'].format(table_name, parameter, args)
        values = [kwargs[k] for k in kwargs]
        return self.execute(query, values)
    
    def select_all(self, table_name, option=None):
        """
        Execute select all SQL statement.

        Example of SQL statement:
            SELECT * FROM table_name (order by id);

        Parameters
        ----------
        table_name : str
            Table name
        option :str
            Option statement of select all
        """
        query = queries['SELECT_ALL'].format('*', table_name, option)
        return self.execute(query)
    
    def update_item(self, table_name, set_values, **kwargs):
        """
        Execute update SQL statement.

        Example of SQL statement:
            UPDATE table_name
            SET column1 = ?, column2 = ?, ...
            WHERE columns1 = ? and columns2 = ? and ..;

        Parameters
        ----------
        table_name : str
            Table name
        set_values : dict
            Values need to update.
        """
        updates = ['{}=?'.format(k) for k in set_values]
        update_values = [set_values[k] for k in set_values]
        condition = ['{}=?'.format(k) for k in kwargs]
        condition_values = [kwargs[k] for k in kwargs]

        query = queries['UPDATE'].format(table_name, ', '.join(updates), ' and '.join(condition))
        return self.execute(query, update_values + condition_values)

    def delete_item(self, table_name, **kwargs):
        """
        Execute delete SQL statement.

        Example of SQL statement:
            DELETE FROM table_name;
            WHERE columns1 = ? and columns2 = ? and ..;

        Parameters
        ----------
        table_name : str
            Table name
        """
        condition = ['{}=?'.format(k) for k in kwargs]
        condition_values = [kwargs[k] for k in kwargs]
        query = queries['DELETE'].format(table_name, 'and '.join(condition))
        return self.execute(query, condition_values)

    def drop_table(self, table_name):
        """
        Execute drop table SQL statement.

        Example of SQL statement:
            DROP TABLE table_name;

        Parameters
        ----------
        table_name : str
            Table name
        """
        query = queries['DROP_TABLE'].format(table_name)
        return self.execute(query)

    def close(self, cursor):
        """
        Close cursor of DB

        Parameters
        ----------
        cursor : sqlite3.Cursor
            An instance of Cursor object
        """
        cursor.close()