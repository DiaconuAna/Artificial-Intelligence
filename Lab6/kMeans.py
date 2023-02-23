import csv
import random

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from tqdm import trange
import matplotlib.pyplot as plt


# Complete the code in k-means.py in order to identify 2 clusters and plot them. (did it for 4 clusters)

def getStats(initialPoints, computedPoints, k):
    stat = [dict() for _ in range(k)]
    for point in initialPoints:
        if initialPoints[point] not in stat[computedPoints[point]]:
            stat[computedPoints[point]][initialPoints[point]] = 0
        stat[computedPoints[point]][initialPoints[point]] += 1
    return stat

def EuclideanDist(x, y):
    # The distance we need to get the nearest centroid
    #print("x = ",x)
    #print("y = ",y)
    return (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2


def nearestCentroid(centroids, point):
    # Find the nearest centroid for a point.
    # We want to take the centroid such that: dist between the point and the centroid is minimum
    minCentroid = centroids[0]
    for centroid in centroids[1:]:
        if EuclideanDist(centroid, point) < EuclideanDist(minCentroid, point):
            minCentroid = centroid
    return minCentroid


def computeNewCentroid(clusters, k):
    """
    New centroid cj = mean of all points xi assigned to cluster j

    :param clusters: key value pairs where the key is the point and the value is the cluster of the point
    :param k: number of clusters
    :return:
    """
    centroids = [[0, 0] for i in range(k)]
    PointsPerCentroid = [0 for _ in range(k)]

    for point in clusters:
        # add the point to the count of points in centroid
        PointsPerCentroid[clusters[point]] += 1
        centroid = centroids[clusters[point]]
        centroid[0] += point[0]
        centroid[1] += point[1]

    newCentroid = []
    #print("centroids = ", centroids)

    for i, centroid in enumerate(centroids):
        if PointsPerCentroid[i] > 0:
            newCX = centroid[0]/PointsPerCentroid[i]
            newCY = centroid[1]/PointsPerCentroid[i]
            newCentroid.append((newCX, newCY))
        else:
            randomPoint = random.choice(clusters.keys())
            #print("Point = ", randomPoint)
            newCentroid.append(randomPoint)

    return newCentroid


def KMeans(x, k, no_of_iterations):
    #cid = np.random.choice(len(x), k, replace=False)

    #print("cid = ", cid)
    # choose random k centroids
    centroids = []
    for index in range(k):
        c = random.choice(x)
        centroids.append((c[0], c[1]))

    #centroids = x[cid, :]
    print("centroids = ", centroids)

    # distance between centroids and all the data points
    #distances = cdist(x, centroids, 'euclidean')
    #print("distances: ", distances)

    # Centroid with the minimum distance
    #minCentroid = nearestCentroid(centroids, x)

    solution = dict() # dictionary of clusters and their corresponding points

    for i in range(no_of_iterations):
        # for each point xi find the nearest centroid cj
        for p in x:
            centroid = nearestCentroid(centroids, p)
            solution[(p[0], p[1])] = centroids.index(centroid)
        if i != no_of_iterations-1:
            centroids = computeNewCentroid(solution, k)

    return solution, centroids


def readPoints():
    pointsLabel = dict()
    points = []
    with open('dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print("Row = ", row[1], row[2])
            if row[1] != 'val1' and row[2] != 'val2':
                pointsLabel[((float(row[1]), float(row[2])))] = row[0]
                points.append(((float(row[1]), float(row[2]))))
            # Complete appending point (row1, row2) to points list
    return pointsLabel, points


if __name__ == "__main__":
    # load data
    dataDict, data = readPoints()
    # Use skikit learns PCA s
    pca = PCA(2)

    # transform the data aka fit the model with X and apply the dimensionality reduction on X
    #df = pca.fit_transform(data)

    points, centroids = KMeans(data, 4, 1500)
    stats = getStats(dataDict, points, 4)
    accuracy = sum([max(stat.values()) for stat in stats]) / len(data)
    print(stats)
    print("Accuracy: ", accuracy)

    colors = ["wheat", "violet", "silver", "powderblue"]

    for point in points:
        plt.scatter(point[0], point[1], color=colors[points[point]])
    for point in centroids:
        plt.scatter(point[0], point[1], color="black")
    plt.show()

