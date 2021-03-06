# -*- coding: utf-8 -*-
import math
import numpy as np
import os
from copy import deepcopy


class Schrodinger:
     #default values of parameters
     input_f='./IOFiles/input.txt'#default input file location
     Pot_file='./IOFiles/Pot_Example.txt'
     c=1
     period=2
     change=0.03
     basis_size=14
     basis_set=4
     stat_potential=3#Since we were asked to treat potential as constant
     o_file="./IOFiles/output.txt"
     #Predefined function
     function=staticmethod(lambda x: x**2+np.sin(x))
     x_points=200#Number of x points spanning the period or domain

     def main(self):
          self.parameters(self.input_f)
          self.initial_coefficient()
          f=open(self.o_file,"w")#Writing into output file
          f.write("For the first version of the project:\n The function used is psi= x^2+sin(x).\n The basis set coefficients are:%s\n"%self.coeff)
          hcoeffs=self.hamiltonian_coefficient(self.coeff)
          f.write("Modified coefficients after evaluating the Hamiltonian operator on the given wavefunction:\n %s\n"%hcoeffs)
          self.apply_variational_principle()
          f.write("The final set of coefficients corresponding to minimum energy:\n %s\n"%self.coeff)
          f.close()

          
          
     
     #Reads the input file and assigns the parameter values
     def parameters(self,in_file):
        if os.path.exists(in_file)!= True:
            print ("The input file path does not exist. Default values will be used")
            raise IOError
        f = open(in_file)
        
        for line in f:

            if "=" in line and (not line.startswith( '#' )):
                if line.split("=")[0]=='c':
                    self.c=int(line.split("=")[1])
                elif line.split("=")[0]=='basis_set':
                    self.basis_set=int(line.split("=")[1])
                elif line.split("=")[0]=='size':
                    self.basis_size=int(line.split("=")[1])

                elif line.split("=")[0]=='domain':
                    self.period=float(line.split("=")[1])          

                elif line.split("=")[0]=='potential_energy':
                    self.stat_potential=float(line.split("=")[1])

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

     def calculate_energy(self,coeff):
          ''' The function calculates energy'''
          new_coeff=self.hamiltonian_coefficient(coeff)
          energy=np.dot(np.conj(coeff),new_coeff)/np.dot(np.conj(coeff),coeff)
          #We normalize <psi|H|psi> by dividing it with <psi|psi>
          return(energy)

     def increase_coefficient(self,coeff_array,i):
          '''This function takes in the coefficient array and an index value. 
          The element of the array at the given index is increased. If energy with 
          the new coefficients is less than that using the original coefficients, the function
          returns 1.'''
          initial_energy=self.calculate_energy(coeff_array)

          coeff_array[i]+=self.change*coeff_array[i]
          final_energy=self.calculate_energy(coeff_array)

          if final_energy<initial_energy:
               return(1)
          return(0)

     def decrease_coefficient(self,coeff_array,i):
          '''This function takes in the coefficient array and an index value. 
          The element of the array at the given index is decreased by change*value of itself. If energy with 
          the new coefficients is less than that using the original coefficients, the function
          returns 1.'''
          initial_energy=self.calculate_energy(coeff_array)
          
          coeff_array[i]-=self.change*coeff_array[i]
          final_energy=self.calculate_energy(coeff_array)
          
          if final_energy<initial_energy:
               return(1)
          return(0)
               

     def apply_variational_principle(self):
          '''This function applies the variational principle to get to the minimum energy.
          In this function the energy is minimized with respect to each basis set coefficient.
          The check_energy variable saves the energy before every change in the coefficients.'''
          iteration=0
          self.convergence=0
          self.coeff.astype(float)
          while iteration<=100000 and self.convergence!=1:
               add_call=0#Keeps track of the number of times increase_coefficient is called
               subtract_call=0#Keeps track of the number of times decrease_coefficient is called
               for i in range(0,len(self.coeff)):
                  
                    if self.increase_coefficient(deepcopy(self.coeff),i)==1:
 
                         check_energy=self.calculate_energy(self.coeff)

                         self.coeff[i]+=self.change*self.coeff[i]
                         add_call+=1
                    elif self.decrease_coefficient(deepcopy(self.coeff),i)==1:
  
                         check_energy=self.calculate_energy(self.coeff)
                         self.coeff[i]-=self.change*self.coeff[i]
                         subtract_call+=1

               '''When either increasing or decreasing coefficients values increases energy, 
               we say that we have found the coefficients that give us lowest energy'''
               if add_call==0 and subtract_call==0:
                    self.convergence=1
               #print(iteration)
               iteration+=1

          '''The returned value should be less than 0 as the final coeff array should correspond to the
          lowest energy'''
          return(self.calculate_energy(self.coeff)-check_energy)
      
          
