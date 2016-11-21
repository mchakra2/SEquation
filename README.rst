===============================
SEquation
===============================

.. image:: https://img.shields.io/travis/mchakra2/SEquation.svg
        :target: https://travis-ci.org/mchakra2/SEquation

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

Implementation Details
-----------------------

The user has to provide an input file named **input.txt** which contains the following information:

* potential_energy: In this implementation it is a constant float
* c: Constant integer parameter
* basis_set: 1 if legendre polynomials are to be used as basis set functions or 2 if Fourier series terms are to be used as basis set functions 
* size: The size of the basis set
* domain(optional): if Fourier series is used the user has the option to input the domain which is treated as the period. For legendre polynomials, the domain is set as [-1,1]
* o_file: location of the output file     

The input file must be saved in the **IOFiles** subdirectory. The **IOFiles** subdirecroty already contains an example input file. Please note that the keys identifying the parameters in the input file should not be altered. Default parameter values are coded in the **SEquation.py** file in **SEquation** sub-directory of the package. 


Instructions to run the tests and the program
---------------------------------------------

To run the script, clone the package by typing this in your command line:
  
git clone https://github.com/mchakra2/SEquation.git


Adjust the **input.txt** file in **IOFiles** subdirectory to your liking. To run the SEquation script, make sure you are in the main **SEquation** package directory (but out of the **SEquation** subdirectory!). Type the following:

python ./SEquation/__init__.py

You will find the output file in the location that you have mentioned in **input.txt** file. If you did not specify the name and location of the output file, you will find the **output.txt**  file under subdirectory **IOFiles** (because that is the default output file location!).       

To run the unit tests type the following from the main package directory:

coverage run --source=SEquation/SEquation.py setup.py test

The coverage can be checked by typing:

coverage report -m


Credits
---------

Maghesree Chakraborty - mchakra2@ur.rochester.edu

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
