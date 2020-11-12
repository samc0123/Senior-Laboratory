# Samuel Chernov
# Momentum Deficit Lab 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.pyplot import show, plot
import csv
import os
import scipy.integrate as spi
from scipy.integrate import quad

# Interpolator Function
def interp2(volG,voltbl,presTbl):
    p=0 # Pressure Counter
    presInterp=np.zeros(len(volG))
    for i in volG :
        presInterp[p]=np.interp(i,vA,presA)
        p+=1
    avgP=np.average(presInterp)
    avgV=np.average(volG)
    return [avgP,avgV]


# Import Data Files 
pre = os.path.dirname(os.path.realpath(__file__))
fname = 'FreeStream-3.txt'
path = os.path.join(pre, fname)
f1=pd.read_csv(path,sep='\t')
time1=list(f1['time'])
Y1=list(f1['Y']) 

fname='WithCylinder-3.txt'
path = os.path.join(pre, fname)
f2=pd.read_csv(path,sep='\t')
time2=list(f2['time'])
Y2=list(f2['Y'])

fname='PresCal.txt'
path = os.path.join(pre, fname)
f3=pd.read_csv(path,sep='\t')
pres=list(f3['Pres'])
v=list(f3['V'])


# -------- PART 2----------------------# 
# ----Calibration Curve: Free-Stream-----
volA=np.array(Y1)
presA=np.array(pres)
vA=np.array(v)

# Interpolate
pts=int(len(volA)/200)
calPltP=np.zeros(pts)
calPltV=np.zeros(pts)
for i in range(pts):
    iFinal=200*(i+1)
    iInit=200*i
    volG=volA[iInit:iFinal]
    tempPlt=interp2(volG,vA,presA)
    calPltP[i]=tempPlt[0]
    calPltV[i]=tempPlt[1]
    


# Plotting
fit=np.polyfit(calPltV,calPltP,1)
fnFit=np.poly1d(fit)

v_new=np.linspace(min(calPltV),max(calPltV),50)
pres_new=fnFit(v_new)


plt.plot(calPltV,calPltP,'x',v_new,pres_new)
plt.text(1,0,str(fnFit))
plt.xlabel('Voltage')
plt.ylabel('Pressure')
plt.title('Free Stream Calibration Curve')
plt.show()
print(str(fnFit))

#--------------------------------------------------#
# ------- Calibration Curve: With Cylinder------
volB=np.array(Y2)
presA=np.array(pres)
vA=np.array(v)

# Interpolate
pts=int(len(volB)/200)
calPltPb=np.zeros(pts)
calPltVb=np.zeros(pts)
for i in range(pts):
    iFinal=200*(i+1)
    iInit=200*i
    volG=volB[iInit:iFinal]
    tempPlt=interp2(volG,vA,presA)
    calPltPb[i]=tempPlt[0]
    calPltVb[i]=tempPlt[1]
    


# Plotting
fitb=np.polyfit(calPltVb,calPltPb,1)
fnFitb=np.poly1d(fitb)

v_new_b=np.linspace(min(calPltVb),max(calPltVb),50)
pres_new_b=fnFit(v_new_b)

plt.plot(calPltVb,calPltPb,'x',v_new_b,pres_new_b)
plt.text(1,0,str(fnFit))
plt.xlabel('Voltage')
plt.ylabel('Pressure')
plt.title('Cylinder Calibration Curve')
plt.show()
print(str(fnFitb))

#------------------END PART 2---------------------------#

#--------------------PART 3-----------------------------# 

# Fit the Eqn from the chart
airPts=[400,770,1230,1520,1600,1720,2000,2130]
gaPts=[0.01,0.05,0.1,0.15,0.17,0.2,0.27,0.3]

charFit=np.polyfit(gaPts,airPts,2)
charFn=np.poly1d(charFit)


# Get the values from the fitted chart 
veloF=charFn(calPltP)
veloC=charFn(calPltPb)

# Plot the velocity vs. L 
L=np.linspace(0,4,21)
plt.plot(L,veloF)
plt.title('Free Stream Velocity vs. Pitot Location')
plt.xlabel('L')
plt.ylabel('Velocity (ft/min)')
plt.show()

plt.plot(L,veloC)
plt.title('Cylinder Velocity vs. Pitot Location')
plt.xlabel('L')
plt.ylabel('Velocity (ft/min)')
plt.show()

# Calculation of the drag force
rho=0.00237 # Imperial
w=0.5/12 # ft, cylinder width
U1=np.average(veloF)
print(U1)
dy=0.2/12 # ft
drag=0
force=np.zeros(len(veloC-1))
for i in range(len(veloF)-1):
    uppVelo=veloC[i+1]
    lowVelo=veloC[i]
    force[i]=((uppVelo*(U1-uppVelo))-(lowVelo*(U1-lowVelo)))*rho*w
    drag+=((uppVelo*(U1-uppVelo))-(lowVelo*(U1-lowVelo)))
drag*=rho*w*-1
print(drag)
#----------------------------------------------------#

#-------------- PART 4-------------------------------#

# Calculate the drag coefficient 
A=np.pi*(w/2)**2
den=0.5*rho*A*U1*U1
Cd=drag/den
print(str(Cd))
#---------------------------------------------------#

#----------------PART 5-----------------------------#

# Literature Drag Force
vLit=0.3
#---------------------------------------------------#

#--------------PART 6------------------------------#

# Air properties 
kVis=1.472*10**-4*60
reA=U1*w/kVis
print(reA)

# Water Properties
watftSec=2*5280/60
kVisW=1.455*10**-5*60
reW=watftSec*w/kVisW
print("ReW=: "+str(reW))

rhoW=1.9402
tempDen=0.5*rhoW*w*watftSec*watftSec
Fl=Cd*tempDen
print("Force/Length=: "+str(Fl))
#--------------------------------------------------#

#-------------------PART 7-------------------------#

# Calculate error using RMS
eVeloC=np.zeros(len(veloC)-1)
eF=np.zeros(len(veloC)-1)
eTot=0
eVeloF=U1*0.01
for i in range(len(eVeloC-1)):
    # Calculate the subtraction error
    eVeloC[i]=0.01*veloC[i]
    eIn=np.sqrt(eVeloC[i]**2+eVeloF**2)

    # Calculate the error of multiplication
    term1e=(eIn/(U1-veloC[i]))**2
    term2e=(eVeloC[i]/veloC[i])**2
    eF[i]=np.sqrt(term1e+term2e)*force[i]

    # Root Sum Square the Force errors
    eTot+=eF[i]**2
errorF=np.sqrt(eTot)/21
print("Error in Drag Force=: "+str(errorF))

#-----------------------------------------------#
#--------------PART 8---------------------------# 
errorCd=np.sqrt((errorF/drag)**2+(eVeloF/U1)**2)/21
print("Cd error=: "+str(errorCd))