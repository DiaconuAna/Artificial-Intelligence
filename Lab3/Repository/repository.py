# -*- coding: utf-8 -*-

import pickle
from Domain.Drone import Drone
from domain import *
from random import *
from utils import *
import numpy as np


class repository():
    def __init__(self):
        self.__populations = []
        self.__dmap = Map()
        self.__drone = Drone(randint(0, 19), randint(0, 19))

    def createPopulation(self, args):
        # args = [populationSize, individualSize] -- you can add more args    
        self.__populations.append(Population(self.__drone, self.__dmap))

    # TO DO : add the other components for the repository: 
    #    load and save from file, etc

    def getPopulation(self):
        return self.__populations

    def getIndividualsForPopulation(self):
        return self.__populations.getIndividuals()

    def addPopulation(self, population):
        self.__populations.append(population)

    def setPopulation(self, population):
        self.__populations[-1] = population

    def getMap(self):
        return self.__dmap

    def getDrone(self):
        return self.__drone

    def setMap(self, newMap):
        self.__dmap = newMap

    def getBestPath(self):
        return self.__populations[-1].getBestIndividualPath()
