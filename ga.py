#Final Programming Project
#This file contains the Microbial class used in main.py
#Robert Kellems
#Based on Microbial class first used in Project 3

import numpy as np
import random as rn

class Microbial:
    def __init__(self,popSize,noteValue,mProb,valueList):
        """
        popSize (int): number of genomes to exist in the population
        noteValue (fraction): the minimum note value that can exist within the 4 bar melody
        mProb (float): determines the probability for mutation
        valueList (list): list of binary values that are used for determining fitness
        """
        self.popSize = popSize
        self.mProb = mProb
        self.len = int(4/noteValue) #this is done to ensure that the genome has the right number of genes to create 4 bars of music (e.g. if 1/2 note is the minimum note value, then there should be 4/(1/2) genes).
        self.valueList = valueList
        self.bestFit = 0
        self.bestGenome = None
        self.pop = np.zeros((self.popSize,self.len))
        for i in range(self.popSize):
            for j in range(self.len):
                self.pop[i][j] = rn.randint(0,14)
                #0 denotes a rest, 1-12 denote all 12 notes in the chromatic scale starting at C, with 13 denoting C an octave up, and 14 denoting extended duration of a note when it occurs after a note in the order of the genome.

    def tournament(self,function):
        a,b = self.pop[rn.choice(range(self.popSize))], self.pop[rn.choice(range(self.popSize))] #assigns random genomes from the population to "a" and "b"
        if function(a,self.valueList) > function(b,self.valueList): #fitness values for a and b are compared
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
                #genes are mutated by adding or subtracting 1
                if l[i] == 0:
                    l[i] += 1
                elif l[i] == 14:
                    l[i] -= 1
                else:
                    l[i] = rn.choice([l[i]-1,l[i]+1])
