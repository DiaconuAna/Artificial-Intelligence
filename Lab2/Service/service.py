import queue
from random import randint
from Domain.drone import Drone
from Domain.map import Map


class Service():
    def __init__(self, drone, map):
        self._dmap = map
        self._drone = drone
        print("DRONE: ", self._drone.x, self._drone.y)

    def loadMap(self):
        self._dmap.loadMap("Resources/test1.map")

    def randomMap(self):
        self._dmap.randomMap()

    def getMapImage(self):
        return self._dmap.image()

    def getDrone(self):
        return self._drone

    def getStartPosition(self):
        return self._drone.getXCoordinate(), self._drone.getYCoordinate()

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
        print("Initial X:", initialX)
        print("Initial Y:", initialY)

        print("Final X:", finalX)
        print("Final Y:", finalY)

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
                print("bye")
                return False, []

            node = toVisit.pop(0)

            print("surface = ", self._dmap.surface[node[0]][node[1]])
            print("node = ", node)

            x = node[0]
            y = node[1]
            # print("hey ", x, y)

            visited.append(node)
            print("visited = ", visited)

            if x == finalX and y == finalY:
                print("final: ", x, y)
                found = True
            else:
                aux = self.getAStarUnvisitedNeighbours(x, y, finalX, finalY, visited)
                # print("aux= ", aux)
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
                print("ToVisit: ", toVisit)

        if found:
            return True, self.buildPath(previous, finalX, finalY)
        else:
            return False, []

    def getAStarUnvisitedNeighbours(self, x1, y1, x2, y2, visited):

        print("Get AStar for: ", x2, y2)
        initialArr = self.getNeighbours(x1, y1)
        finalArr = []
        print("neighbours of: ", x1, y1, "are: ", initialArr)
        if visited:
            for child in initialArr:
                if child not in visited:
                    finalArr.append(child)
            print("unvisited neighbours of: ", x1, y1, "are: ", finalArr)
        else:
            finalArr = initialArr

        print("final arr = ", finalArr)
        return finalArr

    def searchGreedy(self, initialX, initialY, finalX, finalY):
        # TO DO
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

        print("Initial X:", initialX)
        print("Initial Y:", initialY)

        print("Final X:", finalX)
        print("Final Y:", finalY)

        previous = dict()
        previous[(initialX, initialY)] = (None, None)
        found = False
        visited = []
        toVisit = [(initialX, initialY)]

        while len(toVisit) > 0 and not found:

            if not toVisit:  # toVisit is empty
                print("bye")
                return False, []

            node = toVisit.pop(0)
            print("node = ", node)

            x = node[0]
            y = node[1]
            # print("hey ", x, y)

            visited.append(node)
            print("visited = ", visited)

            if x == finalX and y == finalY:
                print("final: ", x, y)
                found = True
            else:
                aux = self.getGreedyUnvisitedNeighbours(x, y, finalX, finalY, visited)
                # print("aux= ", aux)
                if aux:
                    toVisit.append(aux[0])
                # toVisit.sort(key=lambda z: self.manhattanDistance(z[0], finalX, z[1], finalY))

        print("wrong final: ", x, y)
        return True, visited

    def getGreedyUnvisitedNeighbours(self, x1, y1, x2, y2, visited):

        print("Get greedy for: ", x2, y2)
        initialArr = self.getNeighbours(x1, y1)
        finalArr = []
        print("neighbours of: ", x1, y1, "are: ", initialArr)
        if visited:
            for child in initialArr:
                if child not in visited:
                    finalArr.append(child)
            print("unvisited neighbours of: ", x1, y1, "are: ", finalArr)
        else:
            finalArr = initialArr
        finalArr = sorted(finalArr, key=lambda a: self.manhattanDistance(a[0], x2, a[1], y2))
        # print("final arr = ", finalArr)
        return finalArr

    def getNeighbours(self, x, y):
        """
        Gets the empty squares that are neighbours of (x,y) coordinate
        :param x:
        :param y:
        :return: array of valid coordinates
        """
        arr = []

        # up
        if self._dmap.checkValidCoordinate((x - 1, y)):
            arr.append((x - 1, y))

        # down
        if self._dmap.checkValidCoordinate((x + 1, y)):
            arr.append((x + 1, y))

        # left
        if self._dmap.checkValidCoordinate((x, y - 1)):
            arr.append((x, y - 1))

        # right
        if self._dmap.checkValidCoordinate((x, y + 1)):
            arr.append((x, y + 1))

        return arr

    def getMap(self):
        return self._dmap

    @staticmethod
    def dummysearch():
        # example of some path in test1.map from [5,7] to [7,11]
        return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]
