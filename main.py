#Final Programming Project
#This script uses the Microbial class to create melodies and then create MIDI files from them, along with plotting fitness values
#Robert Kellems
#Reference: https://pypi.org/project/MIDIUtil/

import matplotlib.pyplot as plt
from ga import Microbial
from midiutil import MIDIFile

def main(valueList,fitnessFunc,melNum,steps,noteValue,mutProb,fileName):
    """
    valueList (list): list containing values used in fitness function; either note values, interval values, or list of lists containing both
    fitnessFunc (function): the fitness function used for "tournament" method
    melNum (int): number of melodies to be created
    steps (int): number of times "tournament" method is called
    noteValue (fraction): value used as argument for "noteValue" parameter (minimum note value)
    mutProb (float): value used as argument for "mProb" parameter (probability of mutation)
    fileName (str): filename for MIDI to be created
    """
    for i in range(melNum):
        myMicro = Microbial(100,noteValue,mutProb,valueList)
        fitList = []
        for j in range(steps):
            myMicro.tournament(fitnessFunc)
            fitList += [myMicro.bestFit]
        plt.plot(fitList,label=str(i+1))
        
        print(str(i+1) + ': ' + str(myMicro.bestGenome) + ' ' + str(myMicro.bestFit))
        createMidi(myMicro.bestGenome,fileName+str(i+1))

    createPlot()

def noteFitness(genome,valueList):
    """
    valueList contains either a 1 or 0 for each of the possible genes in a genome. The fitness value is the sum of 
    the corresponding binary values for each gene in genome. In other words, fitness is determined by which notes
    appear within the melody.
    """
    fitness = 0
    for gene in genome:
        fitness += valueList[int(gene)]
    return fitness

def intervalFitness(genome,valueList):
    """
    valueList contains either a 1 or 0 for each of the possible differences of a gene and the gene directly following 
    it (the interval). The fitness value is the sum of the corresponding binary values for the difference between each 
    gene in genome and the gene directly following it. In other words, fitness is determined by the intervals between
    each note within the melody.
    """
    fitness = 0
    for i in range(len(genome)-1):
        interval = abs(genome[i]-genome[i+1])
        fitness += valueList[int(interval)]
    return fitness

def bothFitness(genome,valueList):
    """
    This function simply combines noteFitness and intervalFitness. valueList is a list containing two lists: valueList[0]
    contains the values for the "noteFitness" section of the function, and valueList[1] contains the values for the 
    "intervalFitness" part of the function.
    """
    fitness = 0
    for gene in genome:
        fitness += valueList[0][int(gene)]
    for i in range(len(genome)-1):
        interval = abs(genome[i]-genome[i+1])
        fitness += valueList[1][int(interval)]
    return fitness

def createMidi(genome,fileName):
    """
    Creates and saves MIDI files from the melodies created in main().
    """
    myMidi = MIDIFile(1)
    myMidi.addTempo(0,0,170)
    time = 0
    for i,value in enumerate(genome):
        if value in range(1,14):
            j = 1
            try:
                while genome[i+j] == 14: #for each occurence of 14 after a note, the duration of said note increases by the minimum note value
                    j += 1
            except IndexError:
                pass
                                #pitch value     #starting point              #duration         
            myMidi.addNote(0, 0, int(value+59), (time + i)*(16/len(genome)), j*(16/len(genome)), 100)

    with open("Desktop/Q320/FinalProject/" + fileName + ".mid", "wb") as output_file:
        myMidi.writeFile(output_file)

def createPlot():
    """
    Creates a plot of the best fitness over every tournament for each melody.
    """
    plt.title("Fitness over time")
    plt.xlabel("Time")
    plt.ylabel("Best fitness")
    plt.legend()
    plt.show()

main([1,1,0,0,0,1,0,0,1,0,0,0,0,1,1],noteFitness,5,50000,1/4,0.1,'majorKeyQuarter')
main([1,1,0,0,1,0,0,0,1,1,0,1,0,0,1],noteFitness,5,50000,1/4,0.1,'minorKeyQuarter')
main([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],intervalFitness,5,50000,1/2,0.1,'oneNote')
main([[0,1,0,0,0,0,0,0,0,0,0,0,0,1,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,0,1]],bothFitness,3,100000,1/2,0.1,'majorCloseInt')