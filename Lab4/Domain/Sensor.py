class Sensor:
    def __init__(self, position, visiblePositions):
        """
        :param position: coordinates
        :param visiblePositions: from readUDMSensors
        """
        self.position = position
        self.__visiblePositions = visiblePositions
        self.__squaresSeenBySensor = [0 for _ in range(6)]  # from 0 o 5
        self.__energy = 0

    def getMaxEnergy(self):
        """
        Get the maximum number of energy the drone uses
        to fill up to see the surrounding squares
        :return:
        """
        for i in range(0, 5):
            if self.__squaresSeenBySensor[i] == self.__squaresSeenBySensor[i+1]:
                return i
        return 5

    def setSensorVisibility(self):
        maxVisibility = self.__visiblePositions[0]

        for i in range(1, 4):
            if self.__visiblePositions[i] > maxVisibility:
                maxVisibility = self.__visiblePositions[i]

        if maxVisibility > 5:
            maxVisibility = 5

        for i in range(0, 6):
            for visible in self.__visiblePositions:
                if visible < i:
                    self.__squaresSeenBySensor[i] += visible
                else:
                    self.__squaresSeenBySensor[i] += i

        #for i in range(0, 6):
        #    if i < maxVisibility:
        #        self.__accessiblePositions[i] = i
        #    else:
        #        self.__accessiblePositions[i] = maxVisibility

    def getSeenSquares(self):
        return self.__squaresSeenBySensor

    def setEnergy(self, newEnergy):
        self.__energy = newEnergy

    def getVisibilePositions(self):
        return self.__visiblePositions

    def toString(self):
        return "Sensor(" + str(self.position) + " )"

    def __str__(self):
        return "Sensor(" + str(self.position) + " sees UP=" + str(self.__visiblePositions[0]) \
               + ",LEFT=" + str(self.__visiblePositions[1]) \
               + ",DOWN=" + str(self.__visiblePositions[2]) \
               + ",RIGHT=" + str(self.__visiblePositions[3]) + ")"
