from setuptools import setup

setup(
	name='todocli',
	version='1',
	py_modules=['todo.todo', 'todo.datebase'],
	entry_points={
		'console_scripts': [
			'todo = todo.todo:main'
		]
	},
	test_suite='tests',

	author='k-fang',
	author_email='k-fang@com',
	description='A command line todo list manager',
	keywords='command line todo list',
	url='https://todo'
)