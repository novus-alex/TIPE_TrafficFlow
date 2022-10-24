from math import *
import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt


class Bobine:
    def __init__(self, R, M):
        self.mu = 1.25663706e-6
        self.R = R; self.M = M
        self.z = 0

    def set_z(self, z):
        self.z = z
    
    def B(self, r, theta):
        return 2*self.M*self.mu*cos(theta)/(4*pi*r**3), self.M*self.mu*cos(theta)/(4*pi*r**3)

    def B_cart(self, r, theta):
        B = self.B(r, theta)
        return B[0]*cos(theta) + B[1]*sin(theta)

    def dB_cart(self, r, theta):
        return self.B_cart(sqrt(r**2 + self.z**2), theta)*r


def flux(b, z):
    b.set_z(z)
    ress, err = integrate.dblquad(b.dB_cart, 0, b.R, 0, 2*pi)
    return ress


s = Bobine(0.2, 0.00000001); P = []; Z = []
for i in np.arange(-0.1,0.1, 1/10000):
    P.append(flux(s, i)); Z.append(i)

E = []
for i in range(len(Z)-1):
    E.append(-(P[i+1] - P[i])/(P[i+1] - P[i]))

#plt.plot(Z[0:-1],E)

plt.plot(Z, P)
plt.xlabel('z (m)')
plt.ylabel('flux (Wb)')
plt.title(f'Flux dans une bobine (R={s.R} m)')
plt.show()
