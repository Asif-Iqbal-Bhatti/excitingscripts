#!/usr/bin/python
# -*- coding: utf-8 -*-
#_______________________________________________________________________________

from   sys  import stdin
from   math import sqrt
from   math import factorial
import numpy
import sys
import os

#-------------------------------------------------------------------------------

def fit(order,x,y,npoints,nderiv):
    import math
    b = 99999999
    if (npoints > order): 
       b = numpy.polyfit(x,y,order)[order-nderiv]
       b = math.factorial(nderiv)*b
    return b

def printderiv(etam,bb,nfit,output_file):
    print >> output_file, '%12.8f'%(etam),
    for j in range(0,nfit):
        if (bb[j] != 99999999):
            print >> output_file, '%14.6f'%(bb[j]),
    print >> output_file
    return 

def printnice(etam,bb,nfit,nderiv,orderstep,strainpoints,dc,dl):
    print
    print "###########################################\n"
    print "Fit data-----------------------------------\n"
    print "Deformation code             ==>", dc#'%2i'%(dc)
    print "Deformation label            ==>", dl
    print "Maximum value of the strain  ==>", '%10.8f'%(etam) 
    print "Number of strain values used ==>", '%2i'%(strainpoints),"\n" 
    print "Fit results for the derivative of order", '%3i'%(nderiv),"\n"  
    for j in range(0,nfit):
        order=nderiv+j*orderstep
        if (bb[j] != 99999999):
            print "Polynomial of order", '%2i'%(order), "==>", 
            print '%10.2f'%(bb[j]), "[GPa]"
    print
    return 

def sortstrain(s,e):
    ss=[]
    ee=[]
    ww = [s[i] for i in range(len(s))]
    ww.sort()
    for i in range(len(s)):
        ss.append(s[s.index(ww[i])])
        ee.append(e[s.index(ww[i])])
    return ss, ee

#-------------------------------------------------------------------------------

factor=1.
if (os.path.exists('quantum-espresso') or\
    os.path.exists('vasp')): 
    factor=0.5

if (os.path.exists('planar')): 
    input_planar = open('planar',"r")
    factor *= float(input_planar.readline().strip().split()[0])

startorder=0
if (os.path.exists('startorder')): 
    input_startorder = open('startorder',"r")
    startorder=int(input_startorder.readline().strip().split()[0])

if (str(os.path.exists('INFO-elastic-constants'))=='False'): 
    sys.exit("ERROR: file INFO-elastic-constants not found!\n")
if (str(os.path.exists('energy-vs-strain'))=='False'): 
    sys.exit("ERROR: file energy-vs-strain not found!\n")

with open('INFO-elastic-constants',"r") as input_info:
    for _ in range(3):
        line = input_info.readline()
    volume = float(input_info.readline().strip().split()[6])
    defcod = int(input_info.readline().strip().split()[3])
    deflab = input_info.readline().strip().split()[3]
#-------------------------------------------------------------------------------

maximum_strain = input("\nEnter maximum strain for the interpolation >>>> ")
order_of_derivative = input("\nEnter the order of derivative >>>> ")
if (order_of_derivative < 0): 
    sys.exit("ERROR: Order of derivative must be positive!\n")
print

#-------------------------------------------------------------------------------

orderstep = 1
bohr_radius = 0.529177
joule2hartree = 4.3597482
joule2rydberg = joule2hartree/2.
unitconv = joule2hartree/bohr_radius**3/volume*10.**3*factor

#-------------------------------------------------------------------------------

energy = []
strain = []

#-------------------------------------------------------------------------------

input_energy = open('energy-vs-strain',"r")

while True:
    line = input_energy.readline()
    line = line.strip()
    if len(line) == 0: break
    eta,ene = line.split() 

    if (abs(float(eta)) <= maximum_strain):  
       energy.append(float(ene))
       strain.append(float(eta))

#-------------------------------------------------------------------------------

strain,energy=sortstrain(strain,energy)

#-------------------------------------------------------------------------------

orderlist=[]

for i in range(startorder,startorder+6):
    dumorder=order_of_derivative+orderstep*i
    orderlist.append(dumorder)   

with open('check-energy-derivatives',"w") as output_file:
    n_ini = len(strain)

    while (len(strain) > order_of_derivative and len(strain) > 1): 
        bb = []
        n=len(strain)
        etam=max(strain)
        emin=min(strain)
        etam=max(abs(etam),abs(emin))
        for order in orderlist: 
            cc=fit(order,strain,energy,n,order_of_derivative)
            if (cc != 99999999):
                bb.append(cc*unitconv)
            else:
                bb.append(cc)

        printderiv(etam,bb,6,output_file)
        if (n_ini == len(strain)):
            printnice(etam,bb,6,order_of_derivative,orderstep,n_ini,defcod,deflab)

        if (abs(strain[0]+etam) < 1.e-7): 
            strain.pop(0)
            energy.pop(0)

        if (abs(strain[len(strain)-1]-etam) < 1.e-7): 
            strain.pop()
            energy.pop()

with open('order-of-derivative',"w") as output_file:
    factor=1.
factor=1.
os.system("export PDEFAULT=true; PLOT-checkderiv.py")
os.system("unset PDEFAULT")









