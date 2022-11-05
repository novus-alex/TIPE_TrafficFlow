import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import csv
import numpy as np
from random import gauss


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

    @staticmethod
    def plotStyle():
        tdir = 'in'
        plt.rcParams['xtick.direction'] = tdir
        plt.rcParams['ytick.direction'] = tdir


class Regression:
    '''
    Classe de la regression linéaire
    On fait ici une regresison de type U(X) = a*X + b
    '''

    def __init__(self, X, Y, ordre=1, N=1000) -> None:
        self.N = N
        Tools.plotStyle()
        self.X, self.U, = np.array(X), np.array(Y)
        self.X_fit, self.U_fit = self.regression(ordre)
        self.ordre = ordre
        

    

    def regression(self, ordre=1):
        '''
        Regression linéaire, elle renvoie un modèle du type U(X) = a*X + b
        '''

        self.scal = np.polyfit(self.X, self.U, ordre)
        x_fit = np.linspace(min(self.X), max(self.X), 100)
        U_fit = np.array([self.scal[-1] for _ in x_fit])
        for d in range(1, ordre + 1):
            U_fit += self.scal[ordre-d]*x_fit**d
        
        return x_fit, U_fit

    

    def plotData(self):
        '''
        Fonction pour crée le graphe, on affiche la regression, la bande de confiance et les incertitudes de chaques points
        
        '''

        fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
        
        ax[0].plot(self.X_fit, self.U_fit, "r", lw=1, label="Regression linéaire")

        ax[0].set_xlabel("X")
        ax[0].set_ylabel("U(X)")
        ax[0].legend()
        ax[0].grid()

        U_fit_X = np.array([self.scal[-1] for _ in self.X])
        for d in range(1, self.ordre + 1):
            U_fit_X += self.scal[self.ordre-d]*self.X**d

        ax[1].plot(self.X, [0 for _ in self.X], "--k", lw=1)
        ax[1].set_xlabel("X")
        ax[1].set_ylabel("Uexp(X)-U(X)")
        
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()

    
