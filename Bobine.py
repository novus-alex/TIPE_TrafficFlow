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


class Tools:
    def zDict(m, M, p):
        Z, s = {}, 0
        for i in np.arange(m, M, p):
            Z[round(i, len([_ for _ in str(p)]))] = s; s += 1
        return Z


def flux(b, z):
    b.set_z(z)
    ress, err = integrate.dblquad(b.dB_cart, 0, b.R, 0, 2*pi)
    return ress

def getSpeed(e, fp, Z, z):
    return -e[Z.get(z)]/fp[Z.get(z)]

Zr = Tools.zDict(-0.1, 0.1, 0.001)
Zrange = list(Zr.keys())
s = Bobine(0.2, 0.00000001); P = []; Z = []
for i in Zrange:
    P.append(flux(s, i)); Z.append(i)

E = []
for i in range(len(Z)-1):
    E.append((P[i+1] - P[i])/(Z[i+1] - Z[i]))

print(getSpeed([1e-11 for i in range(len(Zrange))], E, Zr, 0.05))

plt.plot(Z[0:-1],E)
plt.xlabel('z (m)')
plt.ylabel('e (V)')
plt.title(f'FEM dans une bobine (R={s.R} m)')
plt.show()
