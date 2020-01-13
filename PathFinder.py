from collections import deque
import sys, pygame
pygame.init()

class Point:

    def __init__(self, coordinates=(0,0)):
        self.coordinates = coordinates #(x, y) tuple format
        self.path = False
        self.foundFrom = None
        self.searched = False
        self.active = True

    def deactivate(self):
        if self.path == False:
            self.active = False

class PathManager:

    directions = [
        [0,-1],
        [1,0],
        [0,1],
        [-1,0]
    ]

    

    def __init__(self, size):
        self.size = size
        self.grid = [[0 for i in range(size)] for j in range(size)]
        self.startPoint = None
        self.endPoint = None
        self.path = None
        self.queue = deque()
        self.isSearching = True

        for x in range(0, size):
            for y in range(0, size):
                self.grid[x][y] = Point((x,y))

    def setStartPoint(self, startCoord):
        if 0 <= startCoord[0] < self.size and 0 <= startCoord[1] < self.size:
            self.startPoint = startCoord
            self.grid[startCoord[0]][startCoord[1]].path = True
            return True
        else:
            return False

    def setEndPoint(self, endCoord):
        if 0 <= endCoord[0] < self.size and 0 <= endCoord[1] < self.size and endCoord != self.startPoint:
            self.endPoint = endCoord
            self.grid[endCoord[0]][endCoord[1]].path = True
            return True
        else:
            return False

    def deactivatePoint(self, coords):
        if coords != self.startPoint and coords != self.endPoint:
            if 0 <= coords[0] < self.size and 0 <= coords[1] < self.size:
                self.grid[coords[0]][coords[1]].deactivate()
                return True
            else:
                return False

    def findPath(self):
        self.queue.append(self.startPoint)
        while (len(self.queue) > 0 and self.isSearching == True):
            searchCenter = self.queue.popleft()
            self.haltIfEndFound(searchCenter)
            self.exploreNeighbours(searchCenter)

        self.reversePath()

    def haltIfEndFound(self, searchCenter):
        if searchCenter == self.endPoint:
            self.isSearching = False

    def exploreNeighbours(self, searchCenter):

        for direction in self.directions:
            explorationCoordinates = (direction[0] + searchCenter[0], direction[1] + searchCenter[1])
            
            if 0 <= explorationCoordinates[0] < self.size and 0 <= explorationCoordinates[1] < self.size:
                searchPoint = self.grid[explorationCoordinates[0]][explorationCoordinates[1]]
                if searchPoint.active == True and searchPoint.searched == False:
                    self.queue.append(explorationCoordinates)
                    searchPoint.foundFrom = searchCenter
                    searchPoint.searched = True

    def reversePath(self):
        currentPoint = self.endPoint
        while currentPoint != self.startPoint:
            self.grid[currentPoint[0]][currentPoint[1]].path = True
            if self.grid[currentPoint[0]][currentPoint[1]].foundFrom != None:
                currentPoint = self.grid[currentPoint[0]][currentPoint[1]].foundFrom
            else:
                currentPoint = self.startPoint
        self.grid[currentPoint[0]][currentPoint[1]].path = True