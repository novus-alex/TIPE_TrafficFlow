import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
from random import gauss
from recuperation_mesures import*

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
M=tri_fusion(K, Q)
K1=M[0]
Q1=M[1]
