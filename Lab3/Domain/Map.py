# -*- coding: utf-8 -*-
import pickle
from random import *

import pygame

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

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def image(self,  colour=BLUE, background=WHITE):
        # creates the image of a map

        imagine = pygame.Surface((self.n * 20, self.m * 20))
        brick = pygame.Surface((20, 20))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine

