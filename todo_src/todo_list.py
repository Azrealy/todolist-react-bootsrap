# -*- coding: utf-8 -*-
from datebase import Model
import argparse
import sys

class Todo(Model):
    def __init__(self, data_file):
        values = ['id int NOT NULL',
                'context TEXT NOT NULL',
                'completed boolean NOT NULL',
                'PRIMARY KEY(id)']
        super(Todo, self).__init__(data_file)
        self.table_name = 'todo_list'
        self.create_table(self.table_name, values)
    
    def add(self, id, text):
        cursor = self.insert(self.table_name, id, text, False)
        cursor.close()
    
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


if __name__ == '__main__':
    todo = Todo('sql.data')
    id = sys.argv[1]
    text = sys.argv[2]
    print(id, text)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'integers', metavar='int', type=int, choices=range(10),
         nargs='+', help='an integer in the range 0..9')
    parser.add_argument(
        '--sum', dest='accumulate', action='store_const', const=todo.add(id,text),
        default=max, help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))