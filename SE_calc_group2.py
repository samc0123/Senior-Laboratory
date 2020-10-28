import numpy as np
import matplotlib as mat

# Boiler constants
hfb=554.595
hgb=2722.57
hfgb=2167.98

# Calorimeter
hgc=2690.01125

# Dryness fraction
xfrac=(hgc-hfb)/hfgb # Cal-Boil/Boil
print("Dryness factor is: "+str(xfrac))

# Heat energy flow in steam leaving the boiler 
mdot=0.00166
mh1=mdot*hgc #kW
print ("mh1= "+str(mh1))

# Heat energy flow for 'sensible heat' 
mhw=mdot*hfb #kW
print("mhw= "+ str(mhw))

# Find Q2
Q1=4460 # power input at first, watts
Q2=Q1+mhw*1000-mh1*1000 # watts
print("Q2= "+str(Q2))

# Find the boiler efficiency 
numnb=(mdot)*(hgc-hfb)
nb=numnb/(Q1/1000)
print("nb= "+str(nb))

# Total Power
WillInt=63.5 # from the excel intercept
W1=56 #Power of the motor
Wtot=W1+WillInt # watts
print("Wtot= "+str(Wtot))

# Get Q5
mdotc=0.033 #cooling water flow rate
coolTIn=31 # cooling water inlet
coolTOut=55.6 # cooling water outlet
Q5=mdotc*4.18*(coolTOut-coolTIn)*1000 # watts
print("Q5= "+ str(Q5))

# Get mh3
hfConOut=146.626 # at outlet temp of 35 centigrade
mh3=mdot*hfConOut
print("mh3= "+str(mh3))

# Get Q3+Q4
Q34=(Q1-Q2-Q5-W1+mhw*1000-mh3*1000)
print("Q34= "+str(Q34))

# Overall efficiency
nthDen=Q1+mhw*1000-mh3*1000 # watts
nth=W1/nthDen 
print("nth= "+str(nth))

# Energy balance
W1b=Q1-Q2-Q34-Q5+mhw*1000-mh3*1000 # watts
print("W1= "+str(W1)+" and the balance value is: "+str(W1b))
