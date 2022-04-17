# -*- coding: utf-8 -*-
from copy import copy
from random import *

from Domain.Gene import Gene
from Domain.Map import Map
from utils import *
import numpy as np
from Domain import *
import random as rand


class Individual():
    def __init__(self, drone, drone_map, size=0):
        self.__size = size
        self.__x = [rand.randint(0, 3) for i in range(self.__size)]
        self.__drone = drone
        self.__dmap = drone_map
        self.__visited = []
        self.__f = None

    def toString(self):
        print("the chromosomes are: ", end = " ")
        for x in self.__x:
            print(x, end = "-")
        print()

    def getVisited(self):
        return self.__visited

    def getChromosome(self):
        return self.__x

    def getFitness(self):
        self.fitness()
        return self.__f

    def readUDMSensors(self, x, y):
        """
        The sensors detect the number of unvisited squares from the current position of the drone
        :param x:
        :param y:
        :return: readings - the unvisited squares the sensors detect from the current position of the drone
        """
        readings = 0  # number of squares the sensors of the drone discover
        temp_map = copy(self.__dmap.getSurface())

        # UP
        xf = x - 1
        while (xf >= 0) and (temp_map[xf][y] != 1):
            if (xf, y) not in self.__visited:
                readings = readings + 1
                self.__visited.append((xf, y))
            xf = xf - 1
        # DOWN
        xf = x + 1
        while (xf < self.__dmap.n) and (temp_map[xf][y] != 1):
            if (xf, y) not in self.__visited:
                readings = readings + 1
                self.__visited.append((xf, y))
            xf = xf + 1
        # LEFT
        yf = y + 1
        while (yf < self.__dmap.m) and (temp_map[x][yf] != 1):
            if (x, yf) not in self.__visited:
                readings = readings + 1
                self.__visited.append((x, yf))
            yf = yf + 1
        # RIGHT
        yf = y - 1
        while (yf >= 0) and (temp_map[x][yf] != 1):
            if (x, yf) not in self.__visited:
                readings = readings + 1
                self.__visited.append((x, yf))
            yf = yf - 1

        return readings, temp_map

    def fitness(self):
        """
        Get the drone current position and see how many unvisited squares
        its sensors can detect in all directions (until a wall is hit)
        For each gene in the individual, until the battery depletes, move the drone in the corresponding
        condition and compute the fitness for each visited square
        The value of the fitness function is the cumulated values of each visited square
        :return:
        """
        # compute the fitness for the individual
        # and save it in self.__f

        totalFitness = 0
        self.__visited = []
        totalFitness, tempMap = self.readUDMSensors(self.__drone.getX(), self.__drone.getY())
        droneCoordinates = [self.__drone.getX(), self.__drone.getY()]
        totalMoves = 0

        for gene in self.__x:
            totalMoves += 1

            # get the direction represented by the gene from the index variation
            direction = v[gene]
            newX = droneCoordinates[0] + direction[0]
            newY = droneCoordinates[1] + direction[1]

            if self.validCoordinate(newX, newY):
                fitness, tempMap = self.readUDMSensors(newX, newY)
                totalFitness += fitness
            else:
                totalFitness -= 10

            droneCoordinates = [newX, newY]

            if self.__drone.getBattery() == totalMoves:
                break

        if newX == self.__drone.getX() and newY == self.__drone.getY():
            totalFitness += 500
        self.__f = totalFitness

    def computePath(self):
        path = []
        droneCoordinates = [self.__drone.getX(), self.__drone.getY()]
        totalMoves = 0

        for gene in self.__x:
            totalMoves += 1

            # get the direction represented by the gene from the index variation
            direction = v[gene]
            newX = droneCoordinates[0] + direction[0]
            newY = droneCoordinates[1] + direction[1]

            if self.validCoordinate(newX, newY):
                path.append([newX, newY])
            else:
                break

            droneCoordinates = [newX, newY]

            if self.__drone.getBattery() == totalMoves:
                break

        print("path= ", path)
        return path

    def mutate(self, mutateProbability=0.04):
        if random() < mutateProbability:
            index = randint(0, self.__size - 1)
            self.__x[index] = randint(0, 3)
            # perform a mutation with respect to the representation - random resetting mutation

    def crossover(self, otherParent, crossoverProbability=0.8):
        offspring1, offspring2 = Individual(self.__drone, self.__dmap, self.__size), Individual(self.__drone,
                                                                                                self.__dmap,
                                                                                                self.__size)
        if random() < crossoverProbability:
            cut = randint(0, self.__size)
            offspring1.__x = self.__x[:cut] + otherParent.__x[cut:]
            offspring2.__x = otherParent.__x[:cut] + self.__x[cut:]
            # perform the crossover between the self and the otherParent
            # used N-cutting point crossover

        return offspring1, offspring2

    def validCoordinate(self, x, y):
        return self.__dmap.checkValidCoordinate((x, y))
