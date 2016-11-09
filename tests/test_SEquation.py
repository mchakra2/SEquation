#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_SEquation
----------------------------------

Tests for `SEquation` module.
"""


import sys
import os
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from SEquation import SEquation
from SEquation import cli



class TestSequation(unittest.TestCase):

    def setUp(self):
        self.S=SEquation.Schrodinger()

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'SEquation.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    
    def test_input_file_exists(self):
           
        #self.assertRaises(IOError,self.p.parameters,'random_file_which_should_not_exist.txt')#Checks if error is raised for invalid input file
        self.assertTrue(os.path.exists(self.S.input_f))#Checks if the given input file exists
        flag = os.path.getsize(self.S.input_f)
        self.assertGreater(flag,0)
