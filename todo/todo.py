# -*- coding: utf-8 -*-
from .model import Model
import argparse
import sys
from functools import wraps
import os.path as op
from sqlite3 import OperationalError

class RecordIsNotFoundError(Exception):
    """
    Record is not found.
    """
    pass

def check_task_exist(method):
    """
    Decorator for TodoList class methods that check whether exists
    the task.

    Notes:
    ------
    ..note:: This decorator should be used at the method which have
             the index argument. Because we use id of the task to
             check existence.
    """
    @wraps(method)
    def wrapper(self, index, *args):
        check = self.select(table_name = self.table_name, id = index)
        if check.fetchall():
            return method(self, index, *args)
        else:
            raise RecordIsNotFoundError('This id of task not exist.')

    return wrapper

class TodoList(Model):
    """
    Todo List manager
    """
    def __init__(self, data_file):
        """
        Inherit the model class
        """
        values = ['id INTEGER NOT NULL PRIMARY KEY',
                  'context TEXT NOT NULL',
                  'completed boolean NOT NULL']
        super(TodoList, self).__init__(data_file)
        self.table_name = 'todo_list'
        self.create_table(self.table_name, values)
        

    def _get_greatest_id(self):
        """
        Use select all SQL statement
        get greatest id of todo list table.

        Returns
        -------
        id : int
            If todo list is empty return 0,
            else return the max id of todo list.
        """
        cursor = self.select_all(self.table_name, option = 'order by id desc')
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        else:
            return 0

    def show_todo_list_by_status(self, completed):
        """
        Show the tasks using task status.
    
        Parameters
        ----------
        completed : bool
            Completed status of task.

        Returns
        -------
        result : list
            List of task column.
        """
        cursor = self.select(table_name = self.table_name, completed = completed)
        result = cursor.fetchall()
        cursor.close()
        return result 


    def show_todo_list(self):
        """
        Show the all tasks in todo list.

        Returns
        -------
        result : list
            List of task column.
        """
        cursor = self.select_all(table_name = self.table_name)
        result = cursor.fetchall()
        cursor.close()
        return result

    def add_task(self, context):
        """
        Add task to todo list.

        Parameters
        ----------
        context : str
            Context of task
        """
        id = self._get_greatest_id() + 1
        cursor = self.insert(self.table_name, id=id, context=context, completed = False)
        cursor.close()

    @check_task_exist
    def complete_task_by_id(self, index):
        """
        Change the task status using task ID

        Parameters
        ----------
        index : int
            ID of task
        """
        set_values = {'completed': True}
        cursor = self.update_item(table_name = self.table_name,
                                  set_values = set_values,
                                  id=index)
        cursor.close()

    @check_task_exist
    def update_task_by_id(self, index, context):
        """
        Update the task context using task ID

        Parameters
        ----------
        index : int
            ID of task
        context : str
            New context of task
        """
        set_values = {'context': context}
        cursor = self.update_item(table_name = self.table_name,
                                  set_values = set_values,
                                  id=index)
        cursor.close()

    @check_task_exist
    def delete_task_by_id(self, index):
        """
        Delete the task using task ID

        Parameters
        ----------
        index : int
            ID of task
        """
        cursor = self.delete_item(table_name = self.table_name, id=index)
        cursor.close()

    def destory_todo_list(self):
        """
        Drop the todo list table
        """
        cursor = self.drop_table(self.table_name)
        cursor.close()


def subcommand_add(subparsers):
    """
    Create `add` subcommand of todo cli.
    """
    parser_add = subparsers.add_parser('add', help='Add a task to the todo list')
    parser_add.add_argument('add-text', type=str, help='Add a task using this context.')

def subcommand_delete(subparsers):
    """
    Create `delete` subcommand of todo cli.
    """
    parser_delete = subparsers.add_parser('delete', help='Delete a task in the todo list.')
    parser_delete.add_argument('del-task-id', type=int,
                               help='The task id you want to delete.')
                            
def subcommand_update(subparsers):
    """
    Create `update` subcommand of todo cli.
    With two require options `--update-task-id` and `--update-task-text`
    use to update task.
    """
    parser_update = subparsers.add_parser('update', help='Update a task to the todo list.')
    parser_update.add_argument('-i', '--update-task-id', type=int, required=True,
                               help='The task id you want to update.')
    parser_update.add_argument('-t', '--update-task-text', type=str, required=True,
                               help='The context of task you want update.')

def subcommand_show(subparsers):
    """
    Create `show` subcommand of todo cli.
    """
    parser_show = subparsers.add_parser('show', help='Show the todo list.')
    parser_show.add_argument('-c', '--complete', action='store_true', default=False,
                                 help='Show complete task list.')
    parser_show.add_argument('-i', '--incomplete', action='store_true', default=False,
                                 help='Show incomplete task list.')
    parser_show.add_argument('-a', '--all', action='store_true', default=False,
                                 help='Show all tasks.')

def subcommand_complete(subparsers):
    """
    Create `complete` subcommand of todo cli.
    """
    parser_complete = subparsers.add_parser('complete', help='Mark a task as complete.')
    parser_complete.add_argument('complete-task-id', type=int,
                                 help='The task id you want complete.')
    

def parse_args(argv):
    """
    Create command line.

    Parameters
    ----------
    argv : list
        List of command line args
    
    Returns
    -------
    dict_args : dict
        Dictionary of command line args.
    """
    parser = argparse.ArgumentParser(description='Todo list manager')
    subparsers = parser.add_subparsers(help='sub-command of Todo List manager help')

    subcommand_add(subparsers)
    subcommand_delete(subparsers)
    subcommand_update(subparsers)
    subcommand_show(subparsers)
    subcommand_complete(subparsers)

    parser.add_argument('--init',  action='store_true',
		                help='Initialize table of the database.')
    args = parser.parse_args(argv)
    return vars(args)



def execute_sql_by_command(dict_args, todo):
    """
    Depends command line args to execute sql.

    Parameters
    ----------
    dict_args : dict
        Dictionary of command line args.
    todo : TodoList
        Instance of TodoList Class.
    """

    if dict_args['init']:
        todo.destory_todo_list()
        print('Todo list initailized succussfully.')

    elif 'add-text' in dict_args:
        text = dict_args['add-text']
        todo.add_task(text)
        print('Task has been added scucessfully.')
        result = todo.show_todo_list_by_status(completed=False)
        for r in result:
            print(str(r[0]) + ' | ' + str(r[1]))

    elif 'del-task-id' in dict_args:
        id = dict_args['del-task-id']
        todo.delete_task_by_id(id)
        print('Task {} is deleted sucessfully.'.format(dict_args['del-task-id']))

    elif 'update_task_id' in dict_args:
        id = dict_args['update_task_id']
        text = dict_args['update_task_text']
        todo.update_task_by_id(id, text)
        print('The Context of task {} has changed to "{}".'.format(id, text))

    elif 'complete-task-id'in dict_args:
        id = dict_args['complete-task-id']
        todo.complete_task_by_id(index=id)
        print('Task {} complete.'.format(id))

    elif 'complete' in dict_args and dict_args['complete']:
        result = todo.show_todo_list_by_status(completed=True)
        print_and_check_result(result)

    elif 'incomplete' in dict_args and dict_args['incomplete']:
        result = todo.show_todo_list_by_status(completed=False)
        print_and_check_result(result)

    elif 'all' in dict_args and dict_args['all']:
        result = todo.show_todo_list()
        print_and_check_result(result)

def print_and_check_result(result):
    """
    Check the task lines from DB

    Parameters:
    -----------
    result : list
        List of task column.
    """
    if result:
        for r in result:
            print(str(r[0]) + ' | ' + str(r[1]))
    else:
        print('No task exist.')
        
def main():
    """
    Main() function execute todo cli.
    """
    try:
        todo_list = TodoList('sql.data')
        if len(sys.argv[1:]) < 1:
            print('too few arguments.')
        else:
            dict_args = parse_args(sys.argv[1:])
            execute_sql_by_command(dict_args, todo_list)
            todo_list.conn.commit()

    except RecordIsNotFoundError as e:
        todo_list.conn.rollback()
        print(e)


if __name__ == '__main__':
    main()