from math import*
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
R=0.2
nu=10**(-7)
M=0.01

def fonction(r,z):
    return nu*M*2*pi*(r**2+z**2)**(-5/2)*(2*z**2-r**2)
B=[]
for i in range(-100,100):
    ress, err=integrate.quad(fonction,0,R,args=(i*10**(-6)))
    B.append(ress)
X=np.linspace(-100*10**(-6),100*10**(-6),200)

plt.plot(X,B)
plt.show()
