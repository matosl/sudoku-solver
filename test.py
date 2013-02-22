#!/usr/bin/python
import sys
import math
from sudoku import SudokuBoard

class WritableObject:
    def __init__(self):
        self.content = ""
    def write(self, string):
        self.content = self.content + string

boardObj = SudokuBoard('medium.txt')

output = WritableObject()
boardObj.printBoard()

boardObj.runBFS()
#boardObj.runDFS()
#boardObj.runModifiedBFS()
#boardObj.runModifiedDFS()

while True :
    boardObj = SudokuBoard('medium.txt')
    boardObj.runSimulatedAnnealing(10000, .85)

print out

