import numpy as np
import random as rn

class Microbial:
    def __init__(self,popSize,noteValue,mProb,valueList):
        """
        popSize (int): número de genomas que existen en la población
        noteValue (fraction): el valor mínimo de nota que puede existir dentro de la melodía de 4 compases
        mProb (float): probabilidad de mutación
        valueList (list): lista de valores binarios que se utilizan para determinar la "adecuación"
        """
        self.popSize = popSize
        self.mProb = mProb
        self.len = int(4/noteValue) #esto se hace para asegurar que el genoma tiene el número correcto de genes para crear 4 compases de música (ej, si 1/2 de nota es el valor mínimo de nota, entonces habrían 4/(1/2) de genes.
        self.valueList = valueList
        self.bestFit = 0
        self.bestGenome = None
        self.pop = np.zeros((self.popSize,self.len))
        for i in range(self.popSize):
            for j in range(self.len):
                self.pop[i][j] = rn.randint(0,14)
                #0 denota un silencio, 1-12 denota las 12 notas en la escala cromática comenzando en C(Do), con 13 denota C una octava hacia arriba y 14 denota la duración extendida de una nota cuando ocurre después de una nota en el orden del genoma.

    def tournament(self,function):
        a,b = self.pop[rn.choice(range(self.popSize))], self.pop[rn.choice(range(self.popSize))] #asigna un genoma aleatorio de la población a "a" y "b"
        if function(a,self.valueList) > function(b,self.valueList): #valores fitness para el genoma a y b son comparados
            winner,loser = a,b
        else:
            winner,loser = b,a
        if function(winner,self.valueList) >= self.bestFit:
            self.bestFit = function(winner,self.valueList) 
            self.bestGenome = winner
        self.mutate(loser)
        return self.bestFit

    def mutate(self,l):
        for i in range(self.len):
            if rn.random() < self.mProb:
                #los genes son mutados añadiendo o restando un 1
                if l[i] == 0:
                    l[i] += 1
                elif l[i] == 14:
                    l[i] -= 1
                else:
                    l[i] = rn.choice([l[i]-1,l[i]+1])
