from math import*
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

class Tools:
    '''
    Outils pour la creation de la regression linéaire
    '''

    @staticmethod
    def isNum(a):
        '''
        Fonction pour detecter si une chaîne de charactère est un nombre
        
        '''
        
        try:
            float(a)
        except ValueError:
            return False
        return True

class Mesure:
    '''classe pour un relever'''
    
    def __init__(self, csv_file,station_id)->None:
        self.csv_file=csv_file
        self.station_id=station_id
        self.Flow, self.Speed= self.getdata(self)
        self.Conc=self.getK(self)
    
    def getdata(self, csv_file):
        Flow_temp=[]
        Speed_temp=[]
        with open(self.csv_file,'r') as table:
            L=(self.station_id).split(',')
            if len(L)==1:
                for line in table:
                    A=line.split(';')
                    if self.station_id=='all':
                        if Tools.isNum(A[3]):
                            Speed_temp.append(float(A[4]))
                            Flow_temp.append(float(A[3]))
                    elif A[0]==self.station_id:
                        if Tools.isNum(A[3]):
                            Speed_temp.append(float(A[4]))
                            Flow_temp.append(float(A[3]))
            elif len(L)>=2:
                for line in table:
                    A=line.split(';')
                    if A[0] in L:
                        if Tools.isNum(A[3]):
                            Speed_temp.append(float(A[4]))
                            Flow_temp.append(float(A[3]))   
        return Flow_temp, Speed_temp

    def getK(self,Speed):
        Index=[]
        Conc_temp=[]
        for i in range(len(self.Flow)):
            if self.Speed[i]==0:
                Index.append(i)
            else:
                Conc_temp.append(float(self.Flow[i]/self.Speed[i]))
        for j in range(len(Index)):
            del(self.Flow[Index[-1]])
            del(self.Speed[Index[-1]])
            Index.pop()       
        return Conc_temp
    
    

path=r"C:/Users/palme/OneDrive/Bureau/PC/Tipe/Programmes TIPE/Test site/Test_Dataset"
os.chdir(path)
def getdata(stations:str):
    Q=[]
    K=[]
    for root,dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.csv'):
                m=Mesure(os.path.join(root,name),stations)
                Q=Q+m.Flow
                K=K+m.Conc
    return K,Q


'''

print(name)
print(type(name))
Q=[]
K=[]
for i in range(len(M)):
    Q=Q+M[i].Flow
    K=K+M[i].Conc
plt.plot(K,Q,'+')
plt.show()
'''
