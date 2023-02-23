import queue
import random
from operator import attrgetter

import numpy.random
import pygame

from Domain.Ant import Ant
from Domain.Sensor import Sensor
from Domain.Map import Map

NUMBER_OF_ANTS = 3
ALPHA = 0.75  # pheromone exponential weight
BETA = 2  # pheromone heuristic weight
RHO = 0.5  # pheromone evaporation rate
SENSORS_POSITIONS = [[1, 6], [2, 8], [3, 11], [6, 4]]


def checkIfSensorsDifferent(sensor1, sensor2):
    """
    Checks if two sensors are different
    :param sensor1:
    :param sensor2:
    :return:
    """
    # print("s1 - s2: ", sensor1.position[0], sensor2.position[0], sensor1.position[1], sensor2.position[1])
    # print("x: ", sensor1.position[0] != sensor2.position[0])
    # print("y: ", sensor1.position[1] != sensor2.position[1])

    # print(sensor1.position[0] != sensor2.position[0] or sensor1.position[1] != sensor2.position[1])
    return sensor1.position[0] != sensor2.position[0] or sensor1.position[1] != sensor2.position[1]


class controller:
    def __init__(self, k=4, energy=20):
        """
        numberSensors = number of sensors
        sensorPositions = the position of sensors in the map
        sensors = the list of sensors
        sensorPath - the path between 2 sensors and its cost
                   - the path consists of the edges between the 2 sensors and its cost is the length
        pathPheromone - the quantity of pheromones on a path
        ants - the ants from the colony
        energy - energy of the drone
        :param k:
        """
        self.__map = Map()
        self.__map.randomMap()
        self.__numberSensors = k
        self.__sensorsPositions = []  # list of sensors
        self.__sensors = []
        self.__sensorPath = dict()
        self.__pathPheromone = dict()
        self.__ants = []
        self.__energy = energy

        self.generateSensors()
        print(self.__sensorsPositions)
        print(self.__map)

    def determineSensorVisibility(self):
        """
        Determine for each sensor the number of squares
        that can be seen
        :return:
        """
        for sensor in self.__sensorsPositions:
            visiblePositions = self.__map.readUDMSensors(sensor[0], sensor[1])
            newSensor = Sensor(sensor, visiblePositions)
            newSensor.setSensorVisibility()
            self.__sensors.append(newSensor)

    @staticmethod
    def manhattanDistance(x1, x2, y1, y2):
        """
        Chosen heuristic function
        computes the sum of the absolute values of the difference between x1 and x2,
        and y1 and y2, respectively
        :param x1: current cell x coordinate
        :param x2: goal x coordinate
        :param y1: current cell y coordinate
        :param y2: goal y coordinate
        :return:
        """
        return abs(x1 - x2) + abs(y1 - y2)

    def searchGreedy(self, initialX, initialY, finalX, finalY):
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]
        """
        :param mapM:
        :param droneD:
        :param initialX:
        :param initialY:
        :param finalX:
        :param finalY:
        :return:
        """
        # initialX = self._drone.getXCoordinate()
        # initialY = self._drone.getYCoordinate()

        previous = dict()
        previous[(initialX, initialY)] = (None, None)
        found = False
        visited = []
        toVisit = [(initialX, initialY)]

        while len(toVisit) > 0 and not found:

            if not toVisit:  # toVisit is empty
                return False, []

            node = toVisit.pop(0)

            x = node[0]
            y = node[1]
            # print("hey ", x, y)

            visited.append(node)

            if x == finalX and y == finalY:
                found = True
            else:
                aux = self.getGreedyUnvisitedNeighbours(x, y, finalX, finalY, visited)
                # print("aux= ", aux)
                if aux:
                    toVisit.append(aux[0])
                # toVisit.sort(key=lambda z: self.manhattanDistance(z[0], finalX, z[1], finalY))

        return visited

    def getGreedyUnvisitedNeighbours(self, x1, y1, x2, y2, visited):

        initialArr = self.map.getValidNeighbors(x1, y1)
        finalArr = []
        if visited:
            for child in initialArr:
                if child not in visited:
                    finalArr.append(child)
        else:
            finalArr = initialArr
        finalArr = sorted(finalArr, key=lambda a: self.manhattanDistance(a[0], x2, a[1], y2))
        # print("final arr = ", finalArr)
        return finalArr

    def buildPath(self, previous, finalX, finalY):
        path = [(finalX, finalY)]
        coord = previous[(finalX, finalY)]
        while coord != (None, None):
            path.append(coord)
            coord = previous[coord]
        path.reverse()
        return path

    def searchAStar(self, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]

        previous = dict()
        previous[(initialX, initialY)] = (None, None)
        found = False
        visited = []

        g = dict()
        g[(initialX, initialY)] = 0

        value = self.manhattanDistance(initialX, finalX, initialY, finalY) + g[(initialX, initialY)]
        toVisit = [(initialX, initialY)]

        while len(toVisit) > 0 and not found:

            if len(toVisit) == 0:  # toVisit is empty
                return self.buildPath(previous, finalX, finalY)

            node = toVisit.pop(0)

            x = node[0]
            y = node[1]
            # print("hey ", x, y)

            visited.append(node)

            if x == finalX and y == finalY:
                # print("final: ", x, y)
                found = True
            else:
                aux = self.getAStarUnvisitedNeighbours(x, y, finalX, finalY, visited)

                if aux:
                    for z in aux:
                        # value = g[z] + self.manhattanDistance(finalX, z[0], finalY, z[1])
                        previous[z] = node
                        if z not in toVisit:
                            toVisit.append(z)
                            g[z] = g[node] + 1
                        else:
                            if g[z] > g[node] + 1:
                                g[z] = g[node] + 1
                toVisit = sorted(toVisit, key=lambda a: g[a] + self.manhattanDistance(a[0], finalX, a[1], finalY))

        if found:
            return self.buildPath(previous, finalX, finalY)
        else:
            # print("visited = ", visited)
            return []

    def getAStarUnvisitedNeighbours(self, x1, y1, x2, y2, visited):

        initialArr = self.__map.getValidNeighbors(x1, y1)
        finalArr = []
        if visited:
            for child in initialArr:
                if child not in visited:
                    finalArr.append(child)
        else:
            finalArr = initialArr

        return finalArr

    def minimumDistanceBetweenPairs(self):
        """
        We determine the minimum distance between each pair of sensors
        :return:
        """
        self.determineSensorVisibility()

        for sensor1 in self.__sensors:
            for sensor2 in self.__sensors:
                # print("\n***********\n")
                # print("sensor 1 - sensor 2 ", sensor1, sensor2)
                if checkIfSensorsDifferent(sensor1, sensor2):
                    # the minimum path between sensor1 and sensor2
                    path = self.searchAStar(sensor1.position[0], sensor1.position[1], sensor2.position[0],
                                            sensor2.position[1])
                    # print("path for: (", sensor1.position[0], sensor1.position[1], ")-(", sensor2.position[0],
                    # sensor2.position[1], ") = ", path)
                    self.__sensorPath[(sensor1, sensor2)] = path
                    self.__pathPheromone[(sensor1, sensor2)] = 1

    def initializeAnt(self):
        """
         m ants are randomly placed in n city-nodes (m ≤ n)
        :return:
        """
        self.__ants.clear()
        sensorsCopy = self.__sensors

        for _ in range(NUMBER_OF_ANTS):
            index = random.randint(0, self.__numberSensors - 1)
            randomSensor = sensorsCopy[index]
            self.__ants.append(Ant(randomSensor))

    def initialize(self):
        """
        Determine the minimum path between each pair of sensors
        and give each ant a random starting position
        :return:
        """
        self.minimumDistanceBetweenPairs()

        for sensor in self.__sensors:
            print(sensor, sensor.getSeenSquares())
        self.initializeAnt()

    def getSensorsToVisit(self, ant):
        """
        Find the sensors an ant has yet to visit from
        the current sensor the ant is on
        :param ant:
        :return:
        """
        sensorsToVisit = []

        # print("To visit for Ant on ", ant.getCurrentSensor())

        for pair in self.__sensorPath.keys():
            #   print(pair[0], pair[1])
            if pair[0] == ant.getCurrentSensor() and pair[1] not in ant.getVisited():
                sensorsToVisit.append(pair[1])
        return sensorsToVisit

    def toVisitSensorsSum(self, ant):
        """
        For the chosen ant, we compute part of the probability of transition from
        the current sensor to another unvisited one
        the sum between the current sensor and each unvisited sensor
        :param ant:
        :return:
        """
        toVisitSensors = self.getSensorsToVisit(ant)

        sum = 0

        for sensorToVisit in toVisitSensors:
            currentIntensity = self.__pathPheromone[(ant.getCurrentSensor(), sensorToVisit)] ** ALPHA
            if len(self.__sensorPath[(ant.getCurrentSensor(), sensorToVisit)]) == 0:
                currentVisibility = 1
            else:
                currentVisibility = 1 / len(self.__sensorPath[(ant.getCurrentSensor(), sensorToVisit)]) ** BETA

            sum += currentIntensity * currentVisibility

        return sum

    def chooseNextSensor(self, ant):
        """
        Choose the sensor most suited for the ant based on the current sensor of the ant
        :param ant:
        :return:
        """

        sensorsToVisit = self.getSensorsToVisit(ant)

        # print("Ant ", ant.getVisited(), "has to visit: ", sensorsToVisit)

        if len(sensorsToVisit) == 0:
            return -1

        # we make a list of probabilities for selecting the next sensor from the unvisited sensors list

        selectionProbability = []

        for sensor in sensorsToVisit:
            # compute the selection probability
            pheromoneIntensity = self.__pathPheromone[(ant.getCurrentSensor(), sensor)]

            if len(self.__sensorPath[(ant.getCurrentSensor(), sensor)]) == 0:
                visibility = 1
            else:
                visibility = 1 / len(self.__sensorPath[(ant.getCurrentSensor(), sensor)])

                # the larger the distance, the smaller the visibility
            totalSum = self.toVisitSensorsSum(ant)

            probability = pheromoneIntensity ** ALPHA * visibility ** BETA / totalSum

            selectionProbability.append(probability)

        # we return the next sensor based on its probability
        return numpy.random.choice(sensorsToVisit, 1, p=selectionProbability).item(0)

    def generateSensors(self):

        self.__sensorsPositions.clear()

        for s in range(self.__numberSensors):
            posX, posY = random.randint(0, 19), random.randint(0, 19)

            # print("1.", posX, posY, self.__map.surface[posX][posY])

            while self.__map.surface[posX][posY] != 0 or posX == 0 or posY == 0:
                posX, posY = random.randint(0, 19), random.randint(0, 19)
                # print("try: ", posX, posY, self.__map.surface[posX][posY])

            self.__sensorsPositions.append([posX, posY])

    def getSensorPositions(self):
        return self.__sensorsPositions

    def iteration(self):
        over = False

        while not over:

            # choose next sensor for each ant
            for ant in self.__ants:
                if len(ant.getVisited()) == len(self.__sensors):
                    over = True
                else:
                    nextSensor = self.chooseNextSensor(ant)
                    # print("next sensor for ant: ", ant.getCurrentSensor(), "is: ", nextSensor)
                    ant.markVisited(nextSensor)

                    # change locally the pheromone trail based on the last element

                    pheromoneIntensity = (1 - RHO) * self.__pathPheromone[
                        (ant.getCurrentSensor(), nextSensor)] + RHO * (
                                                 1 / len(self.__sensorPath[(ant.getCurrentSensor(), nextSensor)]))

                    ant.antPheromones[(ant.getCurrentSensor(), nextSensor)] = pheromoneIntensity
                    ant.totalPheromones += pheromoneIntensity

                    # change the current sensor in ant
                    ant.setCurrentSensor(nextSensor)

    def updatePheromoneTrail(self):
        """
        change the pheromone trail on the paths traverse by all ants
        :return:
        """

        for edge in self.__sensorPath.keys():
            edgePheromoneTotal = 0

            for ant in self.__ants:
                try:
                    unitQuantity = ant.antPheromones[edge] / len(self.__sensorPath[edge])
                    edgePheromoneTotal += unitQuantity
                except KeyError:
                    continue

            # compute the intensity of pheromone trail as a sum of old pheromone evaporation
            # and the new deposited pheromone - rho - evaporation coefficient

            self.__pathPheromone[edge] = (1 - RHO) * self.__pathPheromone[edge] + edgePheromoneTotal

    def getBestAnt(self):
        max = -1
        maxAnt = None

        for ant in self.__ants:
            if ant.totalPheromones > max:
                max = ant.totalPheromones
                maxAnt = ant

        return maxAnt

    def run(self, iterationNumber):
        """
        While iteration < iterationNumber
            1. initialize
            2. f
        :param iterationNumber:
        :return:
        """

        for _ in range(iterationNumber):
            self.initialize()
            self.iteration()
            self.updatePheromoneTrail()

            bestAnt = self.getBestAnt()
            finalPath = []
            sensorPath = []

            # return the solution identified by the best ant
            for edge in bestAnt.antPheromones.keys():
                sensorPath.append(edge[0])
                print("best ant edge = ", edge[0], edge[1])
                print(self.__sensorPath[edge])
                for step in self.__sensorPath[edge]:
                    finalPath.append(step)

            # to append the last sensor the drone visits
            for s in self.__sensors:
                if s not in sensorPath:
                    sensorPath.append(s)

            print("we visit the sensors as: ")
            for s in sensorPath:
                print(s.toString())
            return finalPath, self.powerSensors(sensorPath)
            # return list(dict.fromkeys(finalPath))

    def powerSensors(self, sensorPath):
        """
        Charge the sensors from the final path with energy
        such that we get the maxim total area surveilled surrounding them
        :param sensorPath:
        :return:
        """

        sensorPath.sort(key=lambda s: (s.getSeenSquares()[-1] / s.getMaxEnergy()))

        energyDistribution = [0 for _ in sensorPath]

        if self.__energy < 0:
            return energyDistribution
        else:
            i = 0
            while i < len(sensorPath) and self.__energy > 0:
                currentSensorEnergy = sensorPath[i].getMaxEnergy()

                if self.__energy > currentSensorEnergy:
                    self.__energy -= currentSensorEnergy
                    energyDistribution[i] = currentSensorEnergy
                else:
                    energyDistribution[i] = self.__energy
                    self.__energy = 0
                i += 1
            return energyDistribution

    @staticmethod
    def mapWithDrone(mapImage):
        drone = pygame.image.load("utils/drona.png")
        mapImage.blit(drone, (0, 0))
        return mapImage

    @property
    def map(self):
        return self.__map
