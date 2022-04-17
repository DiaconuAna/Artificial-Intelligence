import random

import numpy as np

from Domain.Population import Population
from Repository.repository import repository


class controller():
    def __init__(self):
        self.__repo = repository()

    def getMap(self):
        return self.__repo.getMap()

    def getDrone(self):
        return self.__repo.getDrone()

    def setMap(self, newMap):
        self.__repo.setMap(newMap)

    def iteration(self, population):
        # args - list of parameters needed to run one iteration
        # an iteration: -- using generational algorithm
        # selection of the parents - select 2 parents based on the fitness function
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        # print("selection in run: *****")

        individuals = population.getIndividuals()

        i1 = random.randint(0, len(individuals) - 1)
        i2 = random.randint(0, len(individuals) - 1)

        while i1 == i2:
            i2 = random.randint(0, len(individuals) - 1)

        parent1 = individuals[i1]
        parent2 = individuals[i2]

        offspring1, offspring2 = parent1.crossover(parent2)

        offspring1.mutate()
        offspring2.mutate()

        # select the survivors
        # print("offspring1: ", offspring1.toString())
        # print("offspring2: ", offspring2.toString())

        #if offspring1.getFitness() > offspring2.getFitness():
        population.addIndividual(offspring1)
        population.addIndividual(offspring2)

    def run(self, iterationNumber, populationSize, individualSize, generationNumber, randomSeed):
        # args - list of parameters needed in order to run the algorithm

        # until stop condition
        #    perform an iteration
        #    save the information need it for the statistics

        # return the results and the info for statistics

        random.seed(randomSeed)

        population = Population(self.__repo.getDrone(), self.__repo.getMap(), populationSize, individualSize)
        self.__repo.addPopulation(population)

        bestIndividual = None
        avgValue = 0
        fitnessPopulation = []
        lastPopulationFitness = []

        for generation in range(generationNumber):
            for iteration in range(iterationNumber):
                self.iteration(population)

            # schimbul de generatii
            population.setIndividuals(population.selection(populationSize))
            self.__repo.setPopulation(population)  # update the last population

            fitnessPopulation = []

            for i in population.getIndividuals():
                #print("fitness is: ", i.getFitness())
                fitnessPopulation.append(i.getFitness())
            #print("fitness pop: ", fitnessPopulation)
            bestIndividual = population.selection(1)[0]  # select the best individual of the current population
            avgValue = np.average(fitnessPopulation)

            if randomSeed == 29:
                lastPopulationFitness.append(avgValue)
                print("fitness: ", avgValue)

        return bestIndividual, avgValue, lastPopulationFitness

    def solver(self, iterationNumber, populationSize, individualSize, generationNumber):
        # args - list of parameters needed in order to run the solver

        # create the population,
        # run the algorithm
        # return the results and the statistics

        bestIndividuals = []
        avgValues = []
        lastFitness = []

        print(" seed - final generation fitness - best individual fitness")
        for i in range(30):  # set it to 30
            best1, avg1, lastFitness = self.run(iterationNumber, populationSize, individualSize, generationNumber, i)
            print(i, " ", avg1, " ", best1.getFitness())
            bestIndividuals.append(best1)
            avgValues.append(avg1)

        bestIndividuals = self.__repo.getBestPath()

        return bestIndividuals, avgValues, lastFitness, self.__repo.getBestPath()

    # In order to validate your algorithm you have to make at least 30 different runs with
    # different seeds for the random numbers generator and compute the average and standard
    # deviation of the fitnesses for the detected solutions on these runs
