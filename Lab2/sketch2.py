# import the pygame module, so you can use it
import pickle, pygame, time
from pygame.locals import *
from random import random, randint
import numpy as np
from Domain.map import Map
from Domain.drone import Drone
from Resources import *
from Service import *

# Creating some colors
from Service.service import Service

LIGHTBLUE = (204, 229, 255)
LIGHTPURPLE = (204, 153, 255)
BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


def displayWithPath(image, path):
    mark = pygame.Surface((20, 20))
    mark.fill(GREEN)
    for move in path:
        image.blit(mark, (move[1] * 20, move[0] * 20))

    return image


def displayGreedyPath(image, path):
    print("Displaying greedy ... ")
    mark = pygame.Surface((20, 20))
    mark.fill(WHITE)
    for move in path:
        image.blit(mark, (move[1] * 20, move[0] * 20))

    return image

def displayAStarPath(image, path2):
    print("Displaying A Star ... ")
    mark = pygame.Surface((20, 20))
    mark.fill(GOLD)
    for move in path2:
        image.blit(mark, (move[1] * 20, move[0] * 20))

    return image


def displayBothPath(image, path1, path2):
    mark = pygame.Surface((20, 20))
    mark.fill(WHITE)
    for move in path1:
        image.blit(mark, (move[1] * 20, move[0] * 20))

    mark.fill(GOLD)
    for move in path2:
        image.blit(mark, (move[1] * 20, move[0] * 20))

    return image


def markEnd(image, x1, y1, x2, y2):
    print("Marking start and end...")
    mark = pygame.Surface((20, 20))
    mark.fill(GREEN)
    image.blit(mark, (y1 * 20, x1 * 20))
    mark.fill(BLACK)
    image.blit(mark, (y2 * 20, x2 * 20))

    return image


# define a main function
def main():
    # we create the map
    m = Map()
    # m.randomMap()
    # m.saveMap("test2.map")
    # m.loadMap("Resources/test1.map")

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("Resources/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    # create drona
    d = Drone(x, y)

    serv = Service(d, m)
    serv.loadMap()


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
            if event.type == KEYDOWN:

                finalX = randint(0, 19)
                finalY = randint(0, 19)

                while not serv.getMap().checkValidCoordinate([finalX, finalY]):
                    finalX = randint(0, 19)
                    finalY = randint(0, 19)

                initialX, initialY = serv.getStartPosition()
                print("Start position: ", initialX, initialY)
                print("End position: ", finalX, finalY)

                startGreedy = time.time()
                found1, path1 = serv.searchGreedy(initialX, initialY, finalX, finalY)
                endGreedy = time.time()
                startAStar = time.time()
                found2, path2 = serv.searchAStar(initialX, initialY, finalX, finalY)
                endAStar = time.time()
                print("Greedy took", endGreedy - startGreedy, "seconds")
                print("A Star took", endAStar - startAStar, "seconds")
                if found1 and found2:
                    print("Greedy path = ", path1)
                    print("AStar path = ", path2)
                    screen.blit(markEnd(serv.getMapImage(), initialX, initialY, finalX, finalY), (0, 0))
                    pygame.display.flip()
                    time.sleep(1)
                    # pygame.time.delay(1000)
                    screen.blit(displayGreedyPath(serv.getMapImage(), path1), (0, 0))
                    #screen.blit(displayBothPath(serv.getMapImage(), path1, path2),(0,0))
                    pygame.display.flip()
                    pygame.time.delay(5000)
                    screen.blit(serv.getDrone().mapWithDrone(serv.getMapImage()), (0, 0))
                    pygame.display.flip()
                    screen.blit(displayAStarPath(serv.getMapImage(), path2), (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(5000)
                # d.move(serv._dmap)  this call will be erased

        screen.blit(serv.getDrone().mapWithDrone(serv.getMapImage()), (0, 0))
        pygame.display.flip()

    # screen.blit(displayWithPath(serv.getMapImage(), path), (0, 0))

    # pygame.display.flip()
    # time.sleep(5)
    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
