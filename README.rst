===============================
SEquation
===============================


.. image:: https://img.shields.io/pypi/v/SEquation.svg
        :target: https://pypi.python.org/pypi/SEquation

.. image:: https://img.shields.io/travis/mchakra2/SEquation.svg
        :target: https://travis-ci.org/mchakra2/SEquation

.. image:: https://readthedocs.org/projects/SEquation/badge/?version=latest
        :target: https://SEquation.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/mchakra2/SEquation/shield.svg
     :target: https://pyup.io/repos/github/mchakra2/SEquation/
     :alt: Updates


Solving Schrodinger Equation


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


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

