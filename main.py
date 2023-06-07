import matplotlib.pyplot as plt
from ga import Microbial
from midiutil import MIDIFile

def main(valueList,fitnessFunc,melNum,steps,noteValue,mutProb,fileName):
    """
    valueList (list): lista conteniente de valores usados en la función fitness (adecuación); tanto notas, valores de intervalos o una lista de listas conteniendo ambas
    fitnessFunc (function): la función de adecuación es usada para el método "torneo" 
    melNum (int): numero de melodías a crear
    steps (int): número de veces para realizar el "torneo" mutaciones
    noteValue (fraction): valor usado como argumento del parámetro "noteValue" (valor mínimo de nota)
    mutProb (float): valor usado como argumento de "mProb" (probabilidad de mutación)
    fileName (str): nombre del archivo MIDI a crear
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
    
    print("\n")
    createPlot()

def noteFitness(genome,valueList):
    """
    valueList contiene tanto un 1 o 0 para cada posible gen en el genoma. El valor fitness(aptitud) es la suma de los 
    valores binarios correspondientes para cada gen en el genoma. En otras palabras, el fitness (aptitud) es determinado por 
    cuales notas aparecen dentro de la melodía.
    """
    
    fitness = 0
    for gene in genome:
        fitness += valueList[int(gene)]
    return fitness

def intervalFitness(genome,valueList):
    """
    valueList contiene un 1 o un 0 para cada una de las posibles diferencias de un gen y el gen que sigue directamente
    eso (el intervalo). El valor de aptitud es la suma de los valores binarios correspondientes para la diferencia entre cada
    gen en el genoma y el gen que le sigue directamente. En otras palabras, la aptitud está determinada por los intervalos entre
    cada nota dentro de la melodía.
    """
    fitness = 0
    for i in range(len(genome)-1):
        interval = abs(genome[i]-genome[i+1])
        fitness += valueList[int(interval)]
    return fitness

def bothFitness(genome,valueList):
    """
    Esta función simplemente combina noteFitness e intervalFitness. valueList es una lista que contiene dos listas: valueList[0]
    contiene los valores para la sección "noteFitness" de la función, y valueList[1] contiene los valores para la
    "intervalFitness" parte de la función.
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
    Crea y guarda el archivo MIDI de las melodías que se crearon en la función main()
    """

    myMidi = MIDIFile(1)
    myMidi.addTempo(0,0,160)
    time = 0
    for i,value in enumerate(genome):
        if value in range(1,14):
            j = 1
            try:
                while genome[i+j] == 14: #para cada ocurrencia de un 14 después de una nota, la duración de dicha nota aumenta por el valor mínimo
                    j += 1
            except IndexError:
                pass
                            #pitch value (valor de tono)  #punto de comienzo      #duracion         
            myMidi.addNote(0, 0, int(value+59), (time + i)*(16/len(genome)), j*(16/len(genome)), 100)

    with open("./MID/" + fileName + ".mid", "wb") as output_file:
        myMidi.writeFile(output_file)

def createPlot():
    """
    Crea una gráfica de los mas aptos sobre cada torneo(mutación) hecha para cada melodía
    """
    plt.title("Fitness sobre el tiempo")
    plt.xlabel("Tiempo")
    plt.ylabel("Mas Apto")
    plt.legend()
    plt.show()


main([1,0,0,1,1,1,0,0,1,0,0,0,0,1,1],noteFitness,2,50000,1/4,0.1,'primerGenoma')

main([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],intervalFitness,2,50000,1/2,0.1,'segundoGenoma')

main([[0,1,0,0,0,0,0,0,0,0,0,0,0,1,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,0,1]],bothFitness,2,100000,1/2,0.1,'tercerGenoma')