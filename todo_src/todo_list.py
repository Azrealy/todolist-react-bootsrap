# -*- coding: utf-8 -*-
from datebase import Model

class Todo(Model):
    def __init__(self, data_file):
        values = ['id int NOT NULL',
               'context TEXT NOT NULL',
               'completed boolean NOT NULL',
               'PRIMARY KEY(id)']
        super(Todo, self).__init__(data_file)
        self.table_name = 'todo_list'
        self.destory_table()
        self.create_table(self.table_name, val)
    
    def add(self, id, text):
        self.close(self.insert(self.table_name, id, text, False))
    
    def show(self):
        cursor = self.select_all(self.table_name)
        result = cursor.fetchall()
        for r in result:
            print(r)
        cursor.close()
        
    def update(self, index, context, completed=False):
        set_values = {'context': context, 'completed': completed}
        cursor = self.update_item(table_name = self.table_name, set_values = set_values, id=index)
        cursor.close()
        
    def delete(self, index):
        cursor = self.delete_item(table_name = self.table_name, id=index)
        print(cursor)
        cursor.close()
        
    def destory_table(self):
        cursor = self.drop_table(self.table_name)
        cursor.close()