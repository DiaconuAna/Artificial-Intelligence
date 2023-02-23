# -*- coding: utf-8 -*-
import pickle
from random import *
from utils import *
import numpy as np


class Map():
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def getSurface(self):
        return self.surface

    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1

    def __str__(self):
        string =""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def readUDMSensors(self, x, y):
        readings = [0, 0, 0, 0]
        # UP
        xf = x - 1
        while (xf >= 0) and (self.surface[xf][y] == 0):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while (xf < self.n) and (self.surface[xf][y] == 0):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while (yf < self.m) and (self.surface[x][yf] == 0):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while (yf >= 0) and (self.surface[x][yf] == 0):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1

        return readings

    def getValidNeighbors(self, givenX, givenY):
        neighbors = list()

        if givenX-1 > 0 and self.surface[givenX-1][givenY] != 1:
            neighbors.append((givenX-1, givenY))
        if givenX+1 < 20 and self.surface[givenX+1][givenY] != 1:
            neighbors.append((givenX+1, givenY))
        if givenY-1 > 0 and self.surface[givenX][givenY-1] != 1:
            neighbors.append((givenX, givenY-1))
        if givenY+1 < 20 and self.surface[givenX][givenY+1] != 1:
            neighbors.append((givenX, givenY+1))

        return neighbors

    def checkValidCoordinate(self, node):
        """
        Checks if a set of coordinates is valid
        i.e. is not a brick or outside the map
        :param node:
        :return:
        """
        x = node[0]
        y = node[1]

        if x < 0 or y < 0:
            return False
        if x >= self.n or y >= self.m:
            return False
        if self.surface[x][y] != 0:
            return False

        return True

    def saveEnvironment(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadEnvironment(self, numfile):
        with open(numfile, "rb") as f:
            print(f)
            dummy = pickle.load(f)
            self.n = dummy.__n
            self.m = dummy.__m
            self.surface = dummy.surface
            f.close()

