# -*- coding: utf-8 -*-

from random import *

from Domain.Drone import Drone
from Domain.Map import Map
from utils import *
import numpy as np
from Domain.Individual import Individual


class Population():
    def __init__(self, drone, droneMap, populationSize=10, individualSize=20):
        self.__dmap = droneMap
        self.__drone = droneMap
        self.__populationSize = populationSize
        self.__v = [Individual(drone, droneMap, individualSize) for _ in
                    range(populationSize)]  # individuals in a population

    def evaluate(self):
        # evaluates the population
        for x in self.__v:
            x.fitness()

    def selection(self, k=2):
        """
        perform a selection of k individuals from the population
        and returns that selection
        ranking selection based on the fitness function
        :param k:
        :return:
        """
        array = sorted(self.__v, key=lambda x: x.getFitness(), reverse=True)
        #print("Array= ")
        newarr = array[:k]
        #for x in newarr:
        #    print(x.toString(), end = "; ")
        return newarr

    def getIndividuals(self):
        return self.__v

    def setIndividuals(self, newV):
        self.__v = newV
        self.__populationSize = len(newV)

    def addIndividual(self, individual):
        self.__v.append(individual)

    def getBestIndividualPath(self):
        return self.selection(1)[0].computePath()
