class Ant:
    def __init__(self, initialSensor):
        self.__currentSensor = initialSensor
        self.__visited = [initialSensor]  # each ant begins by visiting the initialSensor
        self.antPheromones = dict()
        self.totalPheromones = 0

    def getCurrentSensor(self):
        return self.__currentSensor

    def setCurrentSensor(self, sensor):
        self.__currentSensor = sensor

    def markVisited(self, sensor):
        self.__visited.append(sensor)

    def getVisited(self):
        return self.__visited
