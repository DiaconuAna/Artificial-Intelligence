# import the pygame module, so you can use it
import pickle,pygame,sys
from pygame.locals import *
from random import random, randint
import numpy as np


#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


# When there are no more empty squares to visit (the search is at the end, the stack is
# empty) the position of the drone will be set to none ( x = None, y = None).
# => we need a list of visited positions and a visited stack
# convention => unvisited square = -1, visited square = 0

class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = np.zeros((20, 20))
        # 20 x 20 board
        for i in range(0, 20):
            for j in range(0, 20):
                self.visited[i][j] = -1

        self.visitedStack = [(x, y)] #mark the beginning coordinates as visited


    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1




    def getUnvisitedNeighbours(self, detectedMap):
        """
        Find the adjacent EMPTY squares that are not visited
        :param detectedMap:
        :return:
        """
        unvisitedNeighbours = []
        if self.x > 0 and detectedMap.surface[self.x-1][self.y] == 0:
            if self.visited[self.x - 1][self.y] == -1:
                unvisitedNeighbours.append((self.x - 1, self.y))

        if self.x < 19 and detectedMap.surface[self.x + 1][self.y] == 0:
            if self.visited[self.x + 1][self.y] == -1:
                unvisitedNeighbours.append((self.x+1, self.y))

        if self.y > 0 and detectedMap.surface[self.x][self.y - 1] == 0:
            if self.visited[self.x][self.y-1] == -1:
                unvisitedNeighbours.append((self.x, self.y-1))

        if self.y < 19 and detectedMap.surface[self.x][self.y + 1] == 0:
            if self.visited[self.x][self.y + 1] == -1:
                unvisitedNeighbours.append((self.x, self.y+1))

        return unvisitedNeighbours

    # DFS pseudocode
    # DFS(G, u)
    #     u.visited = true
    #     for each v ∈ G.Adj[u]
    #         if v.visited == false
    #             DFS(G,v)
    # init() {
    #     For each u ∈ G
    #         u.visited = false
    #      For each u ∈ G
    #        DFS(G, u)
    # }

    def moveDSF(self, detectedMap):
        # TO DO!
        # rewrite this function in such a way that you perform an automatic
        # mapping with DFS
        # Step 1: check if all of the map has been visited
        # if yes, the values of x and y are set to a default value of None
        # make a list of the unvisited adjacent squares

        print("hello dfs")

        unvisitedNeighbours = self.getUnvisitedNeighbours(detectedMap)
        print("Unvisited neighbours are: ", unvisitedNeighbours)

        # When there are no more empty squares to visit (the search is at the end, the stack is
        # empty) the position of the drone will be set to none ( x = None, y = None).

        if not unvisitedNeighbours:
            if not self.visitedStack:
                self.x = None
                self.y = None
                return False
            coordinates = self.visitedStack.pop()
            self.x = coordinates[0]
            self.y = coordinates[1]
            print(self.x, self.y)
            print("next step>>>")
        else:
            self.visitedStack.append((self.x, self.y)) #u.visited = true
            self.x, self.y = unvisitedNeighbours.pop()  # if v.visited = false
            self.visited[(self.x, self.y)] = 1  # DFS(v)
            return True



    def visitedFlag(self):
        """
        When there are no more empty squares to visit (the search is at the end, the stack is
        empty) the position of the drone will be set to none ( x = None, y = None).

        Check if there are any unvisited locations
        if x is None and y is None the area has been fully visited
        :return:
        """
        print("visit me")
        print(not(self.x is None and self.y is None))
        return not(self.x is None and self.y is None)
