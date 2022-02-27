from random import randint

from DMap import DMap
from Drone import Drone
from Environment import Environment


class Service:
    def __init__(self):
        self._environment = Environment()
        self._environment.loadEnvironment("test2.map")

        self._dmap = DMap()

        x = randint(0, 19)
        y = randint(0, 19)

        self._drone = Drone(x, y)

    def visitedFlag(self):
        return self._drone.visitedFlag()

    def moveDSF(self, ):
        return self._drone.moveDSF(self._dmap)

    def markDetectedWalls(self):
        return self._dmap.markDetectedWalls(self._environment, self._drone.x, self._drone.y)

    def image(self):
        return self._dmap.image(self._drone.x, self._drone.y)

    def environmentImage(self):
        return self._environment.image()