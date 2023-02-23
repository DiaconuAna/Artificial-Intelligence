# -*- coding: utf-8 -*-


# imports
import pygame

from gui import *
from controller import *

class UI:
    def __init__(self, controller):
        self.__controller = controller
        self.__path = []
        self.__iterations = []
        self.__sensorPositions = controller.getSensorPositions()
        self.__energyDistribution = []

    @staticmethod
    def moveDrona(mapImage, x, y):
        drona = pygame.image.load("fs.png")
        mapImage.blit(drona, (y * 20, x * 20))
        return mapImage

    def image(self):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(LIGHTPURPLE)
        imagine.fill(LIGHTBLUE)
        for i in range(20):
            for j in range(20):
                if self.__controller.map.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
        sensorBrick = pygame.Surface((20, 20))
        sensorBrick.fill(TURQUOISE)
        for sensorPosition in self.__sensorPositions:
            imagine.blit(sensorBrick, (sensorPosition[1] * 20, sensorPosition[0] * 20))

        return imagine

    def run(self):
        #self.__controller.map.randomMap()

        #print(self.__controller.map)

        pygame.init()

        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        startTime = time.time()

        # pass k as the number of sensors
        # to do add iteration number
        self.__path, self.__energyDistribution = self.__controller.run(1)

        print("\n ACO path   " + self.__path.__str__() +
              "\n ACO path-find  : %s seconds\n" % (time.time() - startTime))

        print("Energy distribution among the sensors: ", self.__energyDistribution)

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(WHITE)

        # define a variable to control the main loop
        running = True

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            if self.__path.__len__() > 0:
                dronePosition = self.__path.pop(0)
                time.sleep(0.5)

                screen.blit((self.moveDrona(self.image(), dronePosition[0], dronePosition[1])), (0, 0))
                pygame.display.flip()

        pygame.quit()
