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
    
    def __init__(self, text_file)->None:
        self.text_file=text_file
        self.Flow, self.Speed = self.getdata(self)
        self.Conc=self.getK(self)
    
    def getdata(self, text_file):
        Flow_temp=[]
        Speed_temp=[]
        with open(self.text_file,'r') as text:
            for line in text:
                A=line.split( )
                if Tools.isNum(A[0]):
                    if not(Tools.isNum(A[2])):
                        A[2]=0
                    Speed_temp.append(float(A[2]))
                    Flow_temp.append(float(A[1]))
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
    
    

path=r"C:/Users/palme/OneDrive/Bureau/PC/Tipe/Programmes TIPE/Test site/Mesures2"
os.chdir(path)
Q=[]
K=[]
for root,dirs, files in os.walk(path):
    for name in files:
        if name.endswith('.txt'):
            m=Mesure(os.path.join(root,name))
            Q=Q+m.Flow
            K=K+m.Conc

