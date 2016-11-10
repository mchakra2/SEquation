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
import numpy as np
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
           
       
        self.assertTrue(os.path.exists(self.S.input_f))#Checks if the given input file exists
        flag = os.path.getsize(self.S.input_f)#Checks whether the given input file is empty
        self.assertGreater(flag,0)

    def test_parameters(self):
        self.assertRaises(IOError,self.S.parameters,'random_file_which_should_not_exist.txt')#Checks if error is raised for invalid input file
        self.S.parameters(self.S.input_f)
        self.assertTrue(self.S.basis_set==1 or self.S.basis_set==2)#Check if the choice of basis set is valid

    def test_legendre_coeffs(self):
        x=np.arange(-1,1,0.1)
        function=x
        self.S.legendre_coeffs(function,x)
        self.assertAlmostEqual(self.S.coeff[1],1,3)#The coefficient for the second term in Legendre polynomial should be 1
        for i in range(0,self.S.basis_size+1):
            if i!=1:
               self.assertAlmostEqual(self.S.coeff[i],0,3)#The coefficients for all the terms except the second in Legendre polynomial should be 0

    #To check if taking hamiltonian on existing coefficient gives correct set of modifies coefficients
    def test_hamiltonian_legendre_coeffs(self):
        x=np.arange(-1,1,0.1)
        function=3*(x**2)
        self.S.legendre_coeffs(function,x)
        #print(self.S.coeff)
        new_coeff=self.S.legendre_hamiltonian_coeffs(self.S.coeff)
        #Just to check, modifying coefficient according to the hamiltonian operation
        self.S.coeff[0]=self.S.stat_potential*self.S.coeff[0]+(-self.S.c*6)
        self.S.coeff[2]=self.S.stat_potential*self.S.coeff[2]
        for i in range(0,self.S.basis_size+1):
            #print(self.S.coeff[i],new_coeff[i])
            self.assertAlmostEqual(self.S.coeff[i],new_coeff[i],0,3)#The coefficients of coeff and new_coeff should match
