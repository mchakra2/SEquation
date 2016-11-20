===============================
SEquation
===============================


.. image:: https://img.shields.io/pypi/v/SEquation.svg
        :target: https://pypi.python.org/pypi/SEquation

.. image:: https://img.shields.io/travis/mchakra2/SEquation.svg
        :target: https://travis-ci.org/mchakra2/SEquation

.. image:: https://pyup.io/repos/github/mchakra2/SEquation/shield.svg
	:target: https://pyup.io/repos/github/mchakra2/SEquation/
	:alt: Updates
	 
.. image:: https://coveralls.io/repos/github/mchakra2/SEquation/badge.svg?branch=master
	:target: https://coveralls.io/github/mchakra2/SEquation?branch=master


In this project we solve 1-D Schrodinger Equation using two basis sets: Fourier and Legendre Polynomials. The basis set coefficients corresponding to the lowest energy state of the Hamiltonian was calculated using variational principle.


* Free software: MIT license
* Documentation: https://SEquation.readthedocs.io.


Features
--------

* parameters: function to read from the input file
* legendre_coeff: function to calculate the basis set coefficients of as wave function when legendre polynomials of degree=basis set size are the basis set functions
* legendre_hamiltonian_coeffs: function which takes in the initial coefficient array and returns the modified coefficients after H psi operation
* f_coeffs: calculates the basis set coefficients for fourier series basis set
* fourier_hamiltonian_coeffs: function to take in the initial coefficient array and returns the modified coefficients after H psi operation
* initial_coefficient: function to call the appropriate coefficient calculator fuction based on the basis set choice
* hamiltonian_coefficient: function to call the appropriate hamiltonian coefficient calculator fuction based on the basis set choice
* calculate_energy: function to calculate the energy which is equal to <psi|H|psi>/<psi|psi>
* increase_coefficient: function adds a 3% of a coefficient to itself. If the energy decreases after the coefficient modification, it returns 1 to accept the coefficient change
* decrease_coefficient: function subtracts a 3% of a coefficient to itself. If the energy decreases after the coefficient modification, it returns 1 to accept the coefficient change
* apply_variational_principle: This function either adds or subtracts 3% of the coefficient values (based on which operation yields lesser energy) till the minimum energy is reached or the maximum iteration is reached. The idea of convergence is that, when minimum energy is reached adding or subtracting values from the coefficients increases the energy and so the coefficient array is not modified.
* main: It sequentially calls other functions to read input file, to calculate initial coefficients and to apply the variational principle.     

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



