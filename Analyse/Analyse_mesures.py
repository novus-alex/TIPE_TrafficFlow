import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
from random import gauss
from recuperation_mesures import*
from regression import*
import pandas as pd

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
def max_i2(L):
    i_max=0
    max=L[0]
    for i in range(len(L)):
        if L[i]>=max:
            max=L[i]
            i_max=i
    return i_max

'''On range les liste par ordre croissants selon K'''
K,Q=getdata('all')
M=tri_fusion(K, Q)


'''fontion pour nettoyer les données'''

def analyse(Kf,Qf):
    n=len(Kf)%10
    
    if n!=0:
        Kf=Kf[:-n]
        Qf=Qf[:-n]

    MQ=[]
    MK=[]
    for i in range(len(Kf)//200):
        a=[]
        b=[]
        for j in range(200):
            a.append(Kf[j+i*200])
            b.append(Qf[j+i*200])
            
        da=pd.Series(a,dtype='int64')
        db=pd.Series(b,dtype='int64')
        da.fillna(0)
        db.fillna(0)
        MK.append(np.mean(da))
        MQ.append(np.mean(db))
        '''dmk=pd.Series(MK)
        dmq=pd.Series(MQ)
        dmk.fillna(0)
        dmq.fillna(0)'''



    Kfin=[]
    Qfin=[]
    for i in range(len(Kf)//200):
        A=[]
        B=[]
        for j in range(len(Kf)):
            if Qf[j]>=0.8*MQ[i] and Qf[j]<=1.2*MQ[i]:
                if Kf[j]>=0.9*MK[i] and Kf[j]<=1.1*MK[i]:
                    A.append(Kf[j])
                    Kfin.append(Kf[j])
                    B.append(Qf[j])
                    Qfin.append(Qf[j])

        da=pd.Series(A,dtype='int64')
        db=pd.Series(B,dtype='int64')
        da.fillna(0)
        db.fillna(0)
        MK[i]=np.mean(da)
        MQ[i]=np.mean(db)
        '''dmk=pd.Series(MK)
        dmq=pd.Series(MQ)
        dmk.fillna(0)
        dmq.fillna(0)'''
    return Kfin, Qfin,MK,MQ

'''On étudie la partie fluide, donc avant Q max qui est la capacité de la section (f pour fluide)'''
        
C_i=max_i(M[1])
Kf1,Qf1,MKf,MQf=analyse(M[0][:C_i],M[1][:C_i])

'''On étudie la partie congestionnée, donc après Q max qui est la capacité de la section (c pour congestionnée)'''

C_i=max_i2(M[1])
Kc,Qc,MKc,MQc=analyse(M[0][C_i:],M[1][C_i:])


'''plot'''

plt.plot(K, Q, '+')  
plt.title('Diagramme Fondamental')
plt.xlabel('Concentration (veh/km)')
plt.ylabel('Débit (veh/h)')


'''plot pour partie fluide'''     
        
a,b=np.polyfit(Kf1,Qf1,1)
x=np.linspace(0,max(Kf1),1000)
y=a*x+b
plt.plot(Kf1, Qf1, '+')
plt.plot(MKf, MQf)
plt.plot(x,y)


'''plot pour partie congestionnée'''

a,b=np.polyfit(Kc,Qc,1)
x=np.linspace(max(Kf1),max(Kc),1000)
y=a*x+b
plt.plot(Kc, Qc, '+')
plt.plot(MKc, MQc)
plt.plot(x,y)

plt.show()
''''''


'''
print(len(M[0]))
plt.plot(M[0],M[1],'+')
plt.show()
'''


'''

a,b=np.polyfit(Kf, Qf,1)
Kfin=[]
Qfin=[]
for j in range(1,11):
    Kfin=[]
    Qfin=[]
    for i in range(len(Kf)):
        if Qf[i]>=(1-0.5/j)*(a*Kf[i]+b) and Qf[i]<=(1+0.5/j)*(a*Kf[i]+b):
            Kfin.append(Kf[i])
            Qfin.append(Qf[i])
            a,b=np.polyfit(Kfin, Qfin,1)
x=np.linspace(0,50,1000)
y=a*x+b
print(len(Kfin))
print(a,b)
plt.plot(Kfin, Qfin)
plt.plot(x,y)
plt.show()
'''
