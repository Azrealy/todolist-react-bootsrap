# -*- coding: utf-8 -*-
from datebase import Model
import argparse
import sys
import os.path as op
from sqlite3 import OperationalError

class TodoError(Exception):
    """
    Authentication failed
    """
    pass


class Todo(Model):
    def __init__(self, data_file):
        values = ['id INTEGER PRIMARY KEY AUTOINCREMENT',
                'context TEXT NOT NULL',
                'completed boolean NOT NULL']
        super(Todo, self).__init__(data_file)
        
        self.table_name = 'todo_list'
        try:
            self.show()
        except OperationalError:
            self.create_table(self.table_name, values)
    
    def add(self, text):
        cursor = self.insert(self.table_name, context=text, completed = False)
        cursor.close()
    
    def show(self):
        cursor = self.select_all(self.table_name)
        result = cursor.fetchall()
        cursor.close()
        return result
        
    def update(self, index, context=None, completed=False):
        check = self.select(table_name = self.table_name, id = index)
        if check.fetchall():
            if context:
                set_values = {'context': context, 'completed': completed}
            else:
                set_values = {'completed': completed}
            cursor = self.update_item(table_name = self.table_name,
                                      set_values = set_values,
                                      id=index)
            cursor.close()
        else:
            raise TodoError('This id of task not exist.')

    def delete(self, index):
        check = self.select(table_name = self.table_name, id = index)
        if check.fetchall():
            cursor = self.delete_item(table_name = self.table_name, id=index)
            cursor.close()
        else:
            raise TodoError('This id of task not exist.')

    def destory_table(self):
        cursor = self.drop_table(self.table_name)
        print('Todo list initailized succussfully.')
        cursor.close()
        
    def visibility(self, completed):
        check = self.select(table_name = self.table_name, completed = completed)
        result = check.fetchall()
        if result:
            for r in result:
                print(str(r[0]) + ' | ' + str(r[1]))
        else:
            print('No {} task exist.'.format('completed' if completed else 'incompleted')) 


def parse_args_aa(argv):
    print(argv)
    parser = argparse.ArgumentParser(description='Todo list manager')
    parser.add_argument('--show', action='store_true', default=False,
		help="Show the all task.")
    # Defined a sub-commands parsers
    subparsers = parser.add_subparsers(help='sub-command of Todo List manager help')
    # Create sub-comand od 'add'.
    parser_add = subparsers.add_parser('add', help='Add a task to the todo list')
    parser_add.add_argument('context', type=str, help='Add a task using this context.')

    parser.add_argument('-d', '--delete', type=int,
		help='Delete a task from database using its ID.')
    parser.add_argument('-c', '--complete', type=int,
		help='Mark a task as complete using its ID')
    parser.add_argument('-u', '--update', nargs='*',
		help='Update [context] value of task using its ID.')
    parser.add_argument('--init',  action='store_true',
		help='Initialize table of the database.')
    parser.add_argument('-v', '--visibility', choices=['completed', 'incompleted'],
        help='Choice the visibility to show the task: "completed", "incompleted".')
    args = parser.parse_args(argv)
    return vars(args)

def dispatch(dict_args, todo):

    print(dict_args)
    for k in dict_args:
        if k == 'init' and dict_args[k]:
            todo.destory_table()
        if k == 'context' and dict_args[k]:
            print('Task has been added scucessfully.')
            todo.add(dict_args[k])
        if k == 'delete' and dict_args[k]:
            todo.delete(dict_args[k])
            print('<{}> task is deleted sucessfully.'.format(dict_args[k]))
        if k == 'complete' and dict_args[k]:
            print('Task <{}> complete.'.format(dict_args[k]))
            todo.update(index=dict_args[k], completed=True)
        if k == 'update' and dict_args[k]:
            if len(dict_args[k]) < 2:
                raise TodoError('Agurments too short.')
            if len(dict_args[k]) >= 3 and dict_args[k][2] == 'True':
                todo.update(dict_args[k][0],
                            dict_args[k][1],
                            bool(dict_args[k][2]))
            else:
                todo.update(dict_args[k][0], dict_args[k][1])
            print('The Context of <{}> task has changed to "{}".'.format(dict_args[k][0], dict_args[k][1]))

    for k in dict_args:
        if k == 'visibility' and dict_args[k]:
            if dict_args[k] == 'completed':
                todo.visibility(True)
            elif dict_args[k] == 'incompleted':
                todo.visibility(False)

        if k == 'show' and dict_args[k]:
            result = todo.show()
            if result:
                for r in result:
                    print(str(r[0]) + ' | ' + str(r[1]))
            else:
                print('No task has been added.')
        
def main():
    try:
        todo = Todo('sql.data')
        dict_args = parse_args_aa(sys.argv[1:])
        dispatch(dict_args, todo)
        todo.db.commit()

    except TodoError as e:
        todo.db.rollback()
        print(e)


if __name__ == '__main__':
    main()