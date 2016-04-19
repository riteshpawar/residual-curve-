# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 10:34:15 2016

@author: Archit Datar
"""
#importing stuff
import pandas as pd
import numpy as np
import scipy.integrate as sci
#import matplotlib.pyplot as plt
import ternary

antoine= pd.read_excel('antoine.xlsm',0,header=26, parse_cols=[1,2,3,4,5,6,7,8])
input_= pd.read_excel('interface.xlsx',0,header=0,parse_cols=[0,1])
conditions= pd.read_excel('interface.xlsx',0,header=1, parse_cols= [7,8,9,10])



x0= input_[[1]]  #initial mole fractions in the still
# generating the dataframe to calculate sat pressure
if np.sum(x0)[0]!= 1:
    print ("The initial mole fractions do not add up to 1. Please recheck" )


for id in range(input_.shape[0]):
    if id==0:
        antoine_coeffs= antoine[antoine['ID']==input_['Compound IDs'][id]][['A','B','C']]
        antoine_df= antoine_coeffs
    else:    
        antoine_coeffs= antoine[antoine['ID']==input_['Compound IDs'][id]][['A','B','C']]
        antoine_df= pd.concat((antoine_df,antoine_coeffs))
       
antoines= np.array(antoine_df)     

T= conditions.iloc[0,1] #C
P= conditions.iloc[0,0] #bar

#calculating sat pressure
psat= 10**(antoines[:,0]-antoines[:,1]/(100+antoines[:,2]))  #mmHg
psat_bar= psat/760*1.013 #bar
print psat_bar

def dist(x,L):
    constt=(psat_bar/P)-1
    dxdl= np.zeros_like(x)
    dxdl= np.dot(np.diag(constt),x/L)
    return dxdl

#specifying initial conditions   
x0= np.array(x0)
x0= np.reshape(x0,(len(x0),))

L_initial= conditions.iloc[0,2] #inital qty
L_final= conditions.iloc[0,3] # final qty
L= np.linspace(L_initial,L_final, 10)

#boom!! integrate
x= sci.odeint(dist,x0,L)

print x

figure,tax=ternary.figure(scale=1.0)
tax.boundary()
tax.gridlines(multiple=10, color="black")
tax.left_axis_label("A component", fontsize=10)
tax.right_axis_label("C component", fontsize=10)
tax.bottom_axis_label("B component", fontsize=20)
tax.set_title("Plotting of residue curve", fontsize=20)
tax.plot(x)

tax.show()
#fig= plt.figure()
#ax1= fig.add_subplot(111)
#ax1.plot(L[0:5],x[0:5,:])
#ax1.legend(['a','b','c'])