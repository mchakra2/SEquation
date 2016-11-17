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
from unittest.mock import MagicMock


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
        '''
        The basis set size for legendre polynomials indicates the degree of the legendre polynomial to be used as basis set.
        Hence the total number of coefficients in the coefficient vector will be basis_set size+1 (e.g: basis set size=1 means 
        Legendre polynomial of degree 0, which is just the constant 1. So, we will have single coefficient for the constant 1)
        '''
        self.assertEqual(self.S.basis_size+1,len(self.S.coeff))
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
        self.assertEqual(self.S.basis_size+1,len(new_coeff))
        #Just to check, modifying coefficient according to the hamiltonian operation
        self.S.coeff[0]=self.S.stat_potential*self.S.coeff[0]+(-self.S.c*6)
        self.S.coeff[2]=self.S.stat_potential*self.S.coeff[2]
        for i in range(0,self.S.basis_size+1):
            #print(self.S.coeff[i],new_coeff[i])
            self.assertAlmostEqual(self.S.coeff[i],new_coeff[i],0,3)#The coefficients of coeff and new_coeff should match

    
    def test_fourier_hamiltonian_coeffs(self):
        '''Checks if the modified coefficients after applying hamiltonian agree
        to those calculated manually'''
        self.S.period=2
        self.S.basis_size=4
        self.S.coeff=np.array([1,1,1,1])#Assigning some random coefficient
        new_coeff=self.S.fourier_hamiltonian_coeffs(self.S.coeff)
        for i in range(self.S.basis_size):
            check_coefficient=((self.S.c*(2*np.pi*i/self.S.period)**2)+self.S.stat_potential)*self.S.coeff[i]
            self.assertEqual(check_coefficient,new_coeff[i])

    def test_initial_coefficient(self):
        #Checks if error is raised for invalid argument for function basis_set_selection
        self.S.basis_set=0
        self.assertRaises(ValueError,self.S.initial_coefficient)
        '''With basis_set=1, we check if the size of the coefficient array is same as that which we would expect
        while using legendre polynomials as basis set, i.e. basis_size+1'''
        self.S.basis_set=1
        self.S.initial_coefficient()
        self.assertEqual(len(self.S.coeff),self.S.basis_size+1)
        '''With basis_set=2, we check if the size of the coefficient array is same as that which we would expect
        while using Fourier series as basis set'''
        self.S.basis_set=2
        self.S.initial_coefficient()
        self.assertEqual(len(self.S.coeff),self.S.basis_size)

    
        
    def test_hamiltonian_coefficient_raises_error(self):
        #Checks if error is raised for invalid argument for function basis_set_selection
        self.S.basis_set=0
        self.S.basis_size=3
        initial_coefficients=np.ones(self.S.basis_size)
        self.assertRaises(ValueError,self.S.hamiltonian_coefficient,initial_coefficients)


    def test_calculate_energy(self):
        self.S.basis_size=2
        self.S.period=2
        '''Checks if energy returned for fourier series basis set equals
        the energy manually calculated with the given parameters'''
        self.S.basis_set=2
        self.S.coeff=np.ones(self.S.basis_size)
        self.assertEqual(self.S.calculate_energy(),6+np.pi**2)
        '''Checks if energy returned for legendre basis set equals
        the energy that we expect with the given parameters'''
        self.S.basis_set=1
        self.S.coeff=np.ones(self.S.basis_size+1)
        result=self.S.legendre_hamiltonian_coeffs(self.S.coeff)
        self.assertEqual(self.S.calculate_energy(),result.sum())


class Test_with_mocks(unittest.TestCase):
    def setUp(self):
        self.mocks=SEquation.Schrodinger()

    def test_mock_hamiltonian_coefficient(self):
        '''This function checks whether hamiltonian_coefficient 
        calls appropriate function based on basis set choice'''
        self.mocks.basis_set=1
        self.mocks.basis_size=3
        #With basis_set=1, we check if function legendre_hamiltonian_coeffs is called using mock
        check_coefficients=np.ones(self.mocks.basis_size+1)
        self.mocks.legendre_hamiltonian_coeffs=MagicMock()
        self.mocks.hamiltonian_coefficient(check_coefficients)
        self.mocks.legendre_hamiltonian_coeffs.assert_called_once_with(check_coefficients)
        
        #With basis_set=2, we check if function fourier_hamiltonian_coeffs is called using mock
        initial_coefficients=np.ones(self.mocks.basis_size)
        self.mocks.basis_set=2
        self.mocks.fourier_hamiltonian_coeffs=MagicMock()
        self.mocks.hamiltonian_coefficient(initial_coefficients)
        self.mocks.fourier_hamiltonian_coeffs.assert_called_once_with(initial_coefficients)
