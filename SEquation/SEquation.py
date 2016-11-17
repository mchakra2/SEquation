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
     #Predefined function
     function=staticmethod(lambda x: x**2+np.sin(x))
     x_points=200#Number of x points spanning the period

     '''def main():
            self.parameters(self.input_f)'''
     
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
   
     #Takes in the psi function as an array
     def legendre_coeffs(self,psi,x):
          self.coeff=np.polynomial.legendre.legfit(x,psi,self.basis_size)

    
     def legendre_hamiltonian_coeffs(self,coefficient_array):
          '''The function takes in the legendre coefficient array and return the modified coefficient array after applying hamilton operator on it.
           The polynomial.legendre.legder(c,m) function takes in the original set of coefficients of legendre polynomials of degree n
          and returns the Legendre series coefficients c differentiated m'''
          new_coeff=np.polynomial.legendre.legder(coefficient_array,2)
          
          new_coeff=np.append(new_coeff,[0,0])#Since taking n degree derivative reduces the number of coefficients by n
          #modifying to obtain final coefficients after hamiltonian operation
          new_coeff=(-self.c)*new_coeff+(self.stat_potential*coefficient_array)
          return(new_coeff)

     def f_coeffs(self,psi,x,n):
          
          c= psi*np.exp(-1j*2*n*np.pi*x/self.period)
          return c.sum()/c.size
     def fourier_hamiltonian_coeffs(self,coeff):
          ''' The function takes in the initial fourier basis set coefficient array (taken as argument coeff) and returns the final basis
          set coefficient array after hamilton operation is completed. Since taking hamiltonian on each basis set function retruns the same function,
          but with different coefficient, the NxN hij matrix (were N is the basis set size) discussed in class will be a diagonal matrix. The modification 
          to the initial coefficient will be : cn'=cn*(c*(2.pi.n/L)^2+Vo) Where cn is the initial coefficient, cn' is the modified coefficient, c is the
          argument parameter taken as input, Vo is the constant potential, L is the period and n is the basis set coefficient index (and runs from 0 to basis set size-1). 
          This expression come from the fact that a function can be represented by a fourier series as the following:
          f(x)= SUM_from_-infinity_to_infinity(cn*exp(i.2.pi.n.x/L))   
          Taking gradient of f(x) will yield a coefficient of -(2.pi.n/L)^2 * cn. According to the definition of Hamiltonian, the coefficient is modified 
          to get the final cn' expression'''
          
          H_matrix=np.zeros((self.basis_size,self.basis_size))
          for i in range(self.basis_size):
               H_matrix[i][i]=(self.c*(2*np.pi*i/self.period)**2)+self.stat_potential
          new_coeff=np.dot(H_matrix,coeff)
          return(new_coeff)
          
               

     def initial_coefficient(self):
          '''This function sets the  basis set coefficient array based on the 
          basis set function chosen'''
                  
          if self.basis_set==1:#For Legendre Polynomials
               '''Since Legendre polynomials can be used only from -1 to 1,
               the period is automatically set as [-1,1].'''
               x=np.linspace(-1,1,self.x_points)
               y=self.function(x)
               self.legendre_coeffs(y,x)
               #print(self.coeff)
               # new_coeff=self.legendre_hamiltonian_coeffs(self.coeff)
               #self.coeff=new_coeff
          elif self.basis_set==2:#For Fourier
               x=np.linspace(0,self.period,self.x_points)
               y=self.function(x)
               self.coeff=np.array([self.f_coeffs(y,x,i) for i in np.arange(0,self.basis_size)])

          else:
               print ("The basis set choice should be either 1 for Lagendre Polynomial or 2 for Fourier ")
               raise ValueError

     
     def hamiltonian_coefficient(self,initial_coeff):
          '''This returns the final basis set coefficient array after applying hamiltonian based on
          the choice of basis set function'''        
          if self.basis_set==1:#For Legendre Polynomials
               '''Since Legendre polynomials can be used only from -1 to 1,
               the period is automatically set as [-1,1].'''
               hamiltonian_coeffs=self.legendre_hamiltonian_coeffs(initial_coeff)

          elif self.basis_set==2:#For Fourier
               hamiltonian_coeffs=self.fourier_hamiltonian_coeffs(initial_coeff)

          else:
               print ("The basis set choice should be either 1 for Lagendre Polynomial or 2 for Fourier ")
               raise ValueError

          return(hamiltonian_coeffs)

     def calculate_energy(self):
          ''' The function calculates energy'''
          new_coeff=self.hamiltonian_coefficient(self.coeff)
          energy=np.dot(self.coeff,new_coeff)
          return(energy)
