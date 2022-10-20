from math import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

R=0.2
nu=10**(-7)
M=0.0001
V = 1

def fonction(r,z):
    return nu*M*r*(2*z**2 - r**2)*(r**2 + z**2)**(-5/2)/2

B=[]
for i in np.arange(-1,1, 2/2000):
    ress, err=integrate.quad(fonction,0,R,i*10**(-6))
    B.append(ress)
X=np.linspace(-10,10,2000)

E = []
for i in range(len(X)-1):
    E.append(-V*(B[i+1] - B[i])/(X[i+1] - X[i]))

plt.plot(X[0:-1],E)
plt.show()
