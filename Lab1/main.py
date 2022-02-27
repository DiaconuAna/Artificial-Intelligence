# import the pygame module, so you can use it
import pickle, pygame, sys
from pygame.locals import *
from random import random, randint
import numpy as np

# Creating some colors
from Environment import Environment
from DMap import DMap
from Drone import Drone
from Service import Service

BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


def main():
    # we create the environment
    # e = Environment() #TODO: move to service
    # e.loadEnvironment("test2.map") #TODO: move to service
    # print(str(e))

    # we create the map TODO: move to service
    # m = DMap()

    s = Service()

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("fs.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration")

    # we position the drone somewhere in the area
    # x = randint(0, 19) #TODO: move to service
    # y = randint(0, 19) #TODO: move to service

    # cream drona
    # d = Drone(x, y) #TODO: move to service

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800, 400))
    screen.fill(WHITE)
    # screen.blit(e.image(), (0, 0))
    screen.blit(s.environmentImage(), (0, 0))

    soundObj = pygame.mixer.Sound('D://Uni documents//Sem4//AI//Lab1//peergynt.mp3')
    soundObj.play()

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        # event handling, gets all event from the event queue
        print("enter dfs ?")
        for event in pygame.event.get():
            print("YES")
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        if s.visitedFlag():  # TODO: move to service
            s.moveDSF()  # TODO: move to service
            if s.visitedFlag():
                s.markDetectedWalls()  # TODO: move to service
                screen.blit(s.image(), (400, 0))  # TODO: move to service - m.image
            else:
                running = False
            pygame.display.flip()
            pygame.time.delay(50)
        else:
            running = False

        # d.moveDSF(m)

        print("bye")
        # m.markDetectedWalls(e, d.x, d.y)
        # screen.blit(m.image(d.x, d.y), (400, 0))
        # pygame.display.flip()
        # pygame.time.delay(1000)

    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
