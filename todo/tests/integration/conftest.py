# -*- coding: utf-8 -*-
import pytest
import subprocess

@pytest.fixture(scope='function', autouse=True)
def setup_table():
    """
    Sets up DB data.
    """
    args = ['todo', '--init']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()