# -*- coding: utf-8 -*-

from random import *
from utils import *
import numpy as np


class Drone():
    def __init__(self, x, y, battery=20):
        self.__x = x
        self.__y = y
        self.__battery = battery

    def getBattery(self):
        return self.__battery

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y


