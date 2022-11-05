import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
from random import gauss
from recuperation_mesures import*
from regression import*

def fusion(T,P):
    L=[]
    M=[]
    i1=0 ; i2=0
    n1=len(T[0]) ; n2=len(P[0])
    for i in range(n1+n2):
        if i2==n2 or i1<n1 and T[0][i1]<=P[0][i2]:
            L.append(T[0][i1])
            M.append(T[1][i1])
            i1+=1
        else:
            L.append(P[0][i2])
            M.append(P[1][i2])
            i2+=1
    return [L,M]

def tri_fusion(L,M):
    n=len(L)
    m=len(L)//2
    if n<=1:
        return [L[:],M[:]]
    else:
        return fusion(tri_fusion(L[:m],M[:m]),tri_fusion(L[m:],M[m:]))

def max_i(L):
    i_max=0
    max=L[0]
    for i in range(len(L)):
        if L[i]>max:
            max=L[i]
            i_max=i
    return i_max


'''On range les liste par ordre croissants selon K'''
M=tri_fusion(K, Q)
K1=M[0][:-2]
Q1=M[1][:-2]

'''On étudie la partie fluide, donc avant Q max qui est la capacité de la section (f pour fluide)'''
C_i=max_i(Q1)
Kf=K1[:C_i]
Qf=Q1[:C_i]

n=len(Kf)%10

if n!=0:
    Kf=Kf[:-n]
    Qf=Qf[:-n]
MQ=[]
MK=[]
for i in range(len(Kf)//20):
    a=0
    b=0
    for j in range(20):
        a+=Kf[j+i*20]
        b+=Qf[j+i*20]
    MK.append(a/20)
    MQ.append(b/20)
Kfin=[]
Qfin=[]
for i in range(len(Kf)//20):
    A=[]
    B=[]
    for j in range(len(Kf)):
        if Qf[j]>=0.8*MQ[i] and Qf[j]<=1.2*MQ[i]:
            if Kf[j]>=0.9*MK[i] and Kf[j]<=1.1*MK[i]:
                A.append(Kf[j])
                Kfin.append(Kf[j])
                B.append(Qf[j])
                Qfin.append(Qf[j])
    MK[i]=np.mean(A)
    MQ[i]=np.mean(B)           
 
plt.plot(Kf, Qf, '+')   
plt.plot(MK, MQ)
plt.plot(Kfin, Qfin, '+')
plt.show()
