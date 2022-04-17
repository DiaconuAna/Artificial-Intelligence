# -*- coding: utf-8 -*-


# imports


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATTENTION! the function doesn't check if the path passes trough walls
import time
from datetime import datetime

import matplotlib.pyplot as plot
import numpy as np
import pygame

from Controller.controller import controller
from Domain.Map import Map
from gui import initPyGame, closePyGame, movingDrone
from utils import WHITE


def plotGraph(solutionAverages):
    plot.plot(solutionAverages)
    plot.savefig("solutionAverageFitness.png")


def drawPlot(values):
    print(values)
    arr = np.array(values)
    m = np.mean(arr, axis=0)
    std = np.std(arr, axis=0)
    means = []
    stddev = []
    # for i in range(100):
    means.append(m)
    stddev.append(std)
    plot.plot(means)
    plot.plot(stddev)
    plot.plot(values)
    plot.show()


class UI:
    def __init__(self):
        self.__controller = controller()
        self.__bestIndividuals = []
        # popSize=50, indSize=30, genCount=20, nrIterations=100
        self.__populationSize = 50
        self.__individualSize = 30
        self.__generationNumber = 50
        self.__iterationNumber = 100
        self.__fitnesses = []
        self.__lastFitness = []
        self.__time = 0

    @staticmethod
    def print_menu1():
        print("0. Exit")
        print("1. Map Options")
        print("2. EA Options")

    @staticmethod
    def printMapMenu():
        print("0. Exit")
        print("1. Create random map")
        print("2. Load map")
        print("3. Save map")
        print("4. Visualise map")

    @staticmethod
    def printEAMenu():
        print("0. Exit")
        print("1. Parameters setup")
        print("2. Run the solver")
        print("3. Visualise the statistics")
        print("4. View the drone moving on a path")

    def runMap(self):
        newMap = Map()
        while True:
            self.printMapMenu()
            choice = input("Your option>>> ")

            if choice == "1":
                newMap.randomMap()
                print("Map successfully generated!\n")

            elif choice == "2":
                mapName = input("Enter the map filename: ")
                newMap.loadMap(mapName)
                print("Map successfully loaded!\n")

            elif choice == "3":
                mapName = input("Enter the map filename: ")
                newMap.saveMap(mapName)
                print("Map successfully saved!\n")

            elif choice == "4":
                print(newMap)

            elif choice == "0":
                break

            else:
                print("Invalid command.\n")

        self.__controller.setMap(newMap)

    #   2. EA options:
    #         a. parameters setup
    #         b. run the solver
    #         c. visualise the statistics
    #         d. view the drone moving on a path
    #              function gui.movingDrone(currentMap, path, speed, markseen)
    #              ATTENTION! the function doesn't check if the path passes through walls

    def runEA(self):
        while True:
            self.printEAMenu()
            choice = input("Your option>> ")

            if choice == "1":
                self.__populationSize = input("Population size: ")
                self.__individualSize = input("Number of individuals: ")
                self.__generationNumber = input("Number of generations: ")
                self.__iterationNumber = input("Number of iterations: ")

            elif choice == "2":
                start = time.time()
                bestIndividuals, averages, last_fitness, path = self.__controller.solver(self.__iterationNumber, self.__populationSize,
                                                                     self.__individualSize,
                                                                     self.__generationNumber)
                end = time.time()
                self.__time = end - start
                self.__bestIndividuals = path
                self.__fitnesses = averages
                self.__lastFitness = last_fitness
            elif choice == "3":
                self.logToFile(self.__fitnesses, self.__time)
                print(self.__bestIndividuals)
                drawPlot(self.__lastFitness)
                plotGraph(self.__lastFitness)
            elif choice == "4":
                movingDrone(self.__controller.getMap(), self.__bestIndividuals, 0.2)
            elif choice == "0":
                break

            else:
                print("Invalid command.\n")

    def start(self):
        while True:
            self.print_menu1()
            option = input("Your option: ")

            if option == "1":
                self.runMap()
            elif option == "2":
                self.runEA()
            elif option == "0":
                break
            else:
                print("Invalid command.\n")

    def logToFile(self, solutionAverages, totalTime=0):
        logFile = open("results.txt", "a")
        logFile.write(str(datetime.now()) + "\n")
        logFile.write("Pop.size = %d; Ind.size = %d; Generations = %d; " % (
            self.__populationSize, self.__individualSize, self.__generationNumber))
        logFile.write("Iterations/gen = %d; \n" % (
            self.__iterationNumber))
        logFile.write("Total time: %s\n" % str(totalTime))
        logFile.write("Average of averages: %.3f\n" % np.average(solutionAverages))
        logFile.write("Stdev of averages: %.3f\n" % np.std(solutionAverages))
        logFile.write("\n")
        logFile.close()




if __name__ == "__main__":
    ui = UI()
    ui.start()
