from random import *

from numpy.random.mtrand import rand

from utils import *
import numpy as np


# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation
# a gene represents a direction which the drone can choose
# int representation
# indexes variations - up, left, right, down
# v = [[-1, 0], [1, 0], [0, 1], [0, -1]]
# 0 - up
# 1 - left
# 2 - right
# 3 - down

class Gene():
    def __init__(self):
        self.__direction = randint(0, 3)

    @property
    def getDirection(self):
        return self.__direction
