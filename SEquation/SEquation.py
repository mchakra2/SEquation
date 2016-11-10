# -*- coding: utf-8 -*-
import math
import numpy as np
import os
class Schrodinger:
     #default values of parameters
     input_f='./IOFiles/input.txt'#default input file location
     Pot_file='./IOFiles/Pot_Example.txt'
     c=1
     period=2
     basis_size=14
     basis_set=4
     stat_potential=3#Since we were asked to treat potential as constant
     o_file="./IOFiles/output.txt"
     
     
     #Reads the input file and assigns the parameter values
     def parameters(self,in_file):
        if os.path.exists(in_file)!= True:
            print ("The input file path does not exist. Default values will be used")
            raise IOError
        f = open(in_file)
        
        for line in f:

            if "=" in line:
                if line.split("=")[0]=='c':
                    self.c=int(line.split("=")[1])
                elif line.split("=")[0]=='basis_set':
                    self.basis_set=int(line.split("=")[1])
                elif line.split("=")[0]=='size':
                    self.basis_size=int(line.split("=")[1])

                elif line.split("=")[0]=='Pot_file':
                    self.Pot_file=line.split("=")[1].rstrip()

                elif line.split("=")[0]=='o_file':
                    self.o_file=line.split("=")[1].rstrip()
                    '''if os.path.exists(self.o_file)== True:
                        warnings.warn("A file named "+self.o_file +" already exists. Overwriting the file with output")
     data= np.loadtxt(Pot_file)'''
     #Takes in the psi function as an array
     def legendre_coeffs(self,psi,x):
          self.coeff=np.polynomial.legendre.legfit(x,psi,self.basis_size)

     #Takes in the legendre coefficient array and return the modified coefficient array after applying hamilton operator on it
     def legendre_hamiltonian_coeffs(self,coefficient_array):
          new_coeff=np.polynomial.legendre.legder(coefficient_array,2)
          
          new_coeff=np.append(new_coeff,[0,0])#Since taking n degree derivative reduces the number of coefficients by n
          new_coeff=(-self.c)*new_coeff+(self.stat_potential*self.coeff)
          return(new_coeff)

     def f_coeffs(self,psi,x):
          
          c= y*np.exp(-1j*2*n*np.pi*x/self.period)
          return c.sum()/c.size
