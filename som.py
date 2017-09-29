"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
import random
import math
import sys

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 10
HEIGHT = 10

# Dimentions of the grid
N = 40
 
# This sets the margin between each cell
MARGIN = 1

START_LEARN_RATE = 0.1
 

class Node:
    def __init__(self, row, column):
        self.weights = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        self.row = row
        self.column = column

    def calculateDistance(self, weights):
        distance = 0;

        for i in range(len(self.weights)):
            distance += (self.weights[i] - weights[i]) ** 2;
 
        return math.sqrt(distance)

    def adjustWeights(self, bmnWeights, learningRate, influence):
        for i in range(len(self.weights)):
            self.weights[i] += learningRate * influence * (bmnWeights[i] - self.weights[i])

class Som:
    def __init__(self):
        self.grid = []
        self.initGrid()

    def initGrid(self):
        for row in range(N):
            self.grid.append([])
            for column in range(N):
                self.grid[row].append(Node(row, column))  # Append a cell

    def forEachNode(self, l):
        for row in range(N):
            for column in range(N):
                l(row, column, self.grid[row][column])

    def findBestMatchingNode(self, weights):
        winner = None
        lowestDistance = sys.float_info.max;

        for row in range(N):
            for column in range(N):
                distance = self.grid[row][column].calculateDistance(weights)

                if distance < lowestDistance:
                    lowestDistance = distance
                    winner = self.grid[row][column]

        return winner

    def calculateDistanceBwNodes(self, nodeA, nodeB):
        tmp = (nodeA.row - nodeB.row) ** 2 + (nodeA.column - nodeB.column) ** 2
        return math.sqrt(tmp)

    def calculateRadius(self, itearation, timeConstant):
        return N / 2 * math.exp( -itearation / timeConstant)

    def calculateTimeConstant(self, numOfIterations):
        return numOfIterations / math.log(N / 2)

    def calculateLearningRate(self, itearation, numOfIterations):
        return START_LEARN_RATE * math.exp(-itearation / numOfIterations)

    def calculateInfluence(self, distanceToBMN, radius):
        return math.exp(-(distanceToBMN ** 2) / (2 * radius ** 2));

    def learn(self, inputs, totalIterations, afterIterationCallback):
        timeConstant = self.calculateTimeConstant(totalIterations)
        learningRate = START_LEARN_RATE

        for i in range(totalIterations):
            input = random.choice(inputs)

            bmn = self.findBestMatchingNode(input)
            radius = self.calculateRadius(i, timeConstant)

            self.forEachNode(self.processNode(bmn, radius, learningRate))

            learningRate = self.calculateLearningRate(i, totalIterations)
            afterIterationCallback()

    def processNode(self, bmn, radius, learningRate):
        def process(row, column, node):
            distance = self.calculateDistanceBwNodes(bmn, node)

            if distance < radius:
                influence = self.calculateInfluence(distance, radius)
                node.adjustWeights(bmn.weights, learningRate, influence)

        return process


inputs = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 100, 100), (255, 255, 0)]

 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [(WIDTH + MARGIN) * N + MARGIN, (HEIGHT + MARGIN) * N + MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    def printGrid():
        som.forEachNode(lambda row, column, node: pygame.draw.rect(screen,
                             node.weights,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT]))
        # Limit to 2 frames per second
        clock.tick(50)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    som = Som()
    som.learn(inputs, 500, printGrid)
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

