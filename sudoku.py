#!/usr/bin/python
import sys
import Queue
import copy
import random
import math

class SudokuBoard:
    def __init__(self, filename) :
        self.board = self.parseBoard(filename)
        self.constraints = self.__computeConstraintSets()
        self.pointDict = self.__computePointDict()

    def parseBoard(self, filename) :
        """This function should take as input the name of a file containing a
        sudoku board and return a list of lists of integers, where each
        internal list corresponds to one row of the board."""
        fileptr = open(filename)
        li = [[int(item) for item in list(elem.replace("*","0")[0: len(elem)-1])]
        for elem in fileptr]
       
        return li

    def printBoard(self) :
        """This function should print a representation of self.board to stdout"""
        rowcount = 1
        string = ''
        val = ''
        for row in self.board :
            string = ''
            val = ''
            elemcount = 1
            for elem in row :
                val = str(elem)
                if elem == 0:
                    val = '*'
                if elemcount == 3 or elemcount == 6 :
                    val = val + '  |  '
                elif elemcount != 9 :
                    val = val + ' '
                string = string + val
                elemcount = elemcount + 1
            print string
            if rowcount == 3 or rowcount == 6 :
                print '-------+---------+-------'
            rowcount = rowcount + 1
                    
    def __computeConstraintSets(self) :
        """This function should return a list of sets of 2-tuples. Each tuple
        should indicate a board location."""
        srow = [set([(elem, item) for item in range(0,9)]) for elem in range(0,9)]
        scol = [set([(item, elem) for item in range(0,9)]) for elem in range(0,9)]
        sblk = [set([(elem, x+(item*3)) for x in range(0,3)] + [(elem+1,
        y+(item*3)) for y in range(0,3)] + [(elem+2, z+(item*3)) for z
        in range(0,3)]) for elem in range(0,7,3)
        for item in range(0,3)]
        s = srow + scol + sblk
        
        return s
        
    def __computePointDict(self) :
        """This function should return a dictionary mapping each board location
        to a list of the constraints it's involed in."""
        d = {}
        for x in range(0,9) :
            for y in range(0,9) :
                d[(x,y)] = [elem for elem in self.constraints if (x,y) in elem]

        return d

    def getConstraintSets(self, location) :
        """This function should take as input a board location and return
        the self.pointDict entry associated with that location."""
        return self.pointDict[location]

    def computeUnusedNums(self, constraint) :
        """This function should take as input a constraint and return a set
        of integers. The integers should be all those numbers 1-9 that
        don't occur in any of the constraint's board locations."""
        nums = set()
        allnums = set(range(1,10))
        for item in constraint :
            num = self.board[item[0]][item[1]]
            if num != 0 :
                nums.add(num)
        unused = allnums - nums
        
        return unused
    
    def isSolved(self) :
        """This function should return true if the board is valid and
        complete and false otherwise. That is, if each constraint region
        contains all the numbers 1-9, it should return true. Else, it
        should return false."""
        for item in self.constraints :
            if self.computeUnusedNums(item) != set() :
                return False 
        return True
    
    def runBFS(self) :
        runtime = 0 # number of times successor f(x) was called
        space = 1 # maximum queue length over the run of the entire alg
        
        node = copy.deepcopy(self.board)
        if self.isSolved() :
            return True
        frontier = Queue.Queue()
        frontier.put(copy.deepcopy(node))

        while True :
            node = copy.deepcopy(frontier.get())
            self.board = copy.deepcopy(node)
            self.__computeConstraintSets()
            self.__computePointDict()
            
            if self.isSolved() :
                print "Run-time complexity = " + str(runtime)
                print "Space complexity = " + str(space) + "\n"
                return self.printBoard()

            indices = [(node.index(item), item.index(0)) for item in
            node if item.count(0) > 0]
            
            if indices : #if list is not empty
                [frontier.put(copy.deepcopy(self.__generateSuccessor(item,
                indices[0], node))) for item in range(1,10)]
                runtime = runtime + 9
            space = max(space, frontier.qsize())
            
    def __generateSuccessor(self, number, index, board) :
        successor = copy.deepcopy(board)
        successor[index[0]][index[1]] = number
        return successor
       
    def runDFS(self) :
        runtime = 0 # number of times successor f(x) was called
        space = 1 # maximum queue length over the run of the entire alg
        
        node = copy.deepcopy(self.board)
        if self.isSolved() :
            return True
        frontier = Queue.LifoQueue()
        frontier.put(copy.deepcopy(node))

        while True :
            node = copy.deepcopy(frontier.get())
            self.board = copy.deepcopy(node)
            self.__computeConstraintSets()
            self.__computePointDict()
            
            if self.isSolved() :
                print "Run-time complexity = " + str(runtime)
                print "Space complexity = " + str(space) + "\n"
                return self.printBoard()

            indices = [(node.index(item), item.index(0)) for item in
            node if item.count(0) > 0]
            
            if indices : #if list is not empty
                [frontier.put(copy.deepcopy(self.__generateSuccessor(item,
                indices[0], node))) for item in range(1,10)]
                runtime = runtime + 9
            space = max(space, frontier.qsize())
    
    def __isValidSuccessor(self) :
        for i in range(0,9) :
            for j in range (0,9) :
                num = self.board[i][j]
                if num != 0 :
                    constraintsli = self.getConstraintSets((i,j))
                    constraints = constraintsli[0] | constraintsli[1] | constraintsli[2]
                    isValid = [False for pos in constraints if self.board[pos[0]][pos[1]]
                               == num and pos != (i,j)]
                    if False in isValid :
                        return False
        return True
                
    def runModifiedDFS(self) :
        runtime = 0 # number of times successor f(x) was called
        space = 1 # maximum queue length over the run of the entire alg
        
        node = copy.deepcopy(self.board)
        if self.isSolved() :
            return True
        frontier = Queue.LifoQueue()
        frontier.put(copy.deepcopy(node))

        while True :
            node = copy.deepcopy(frontier.get())
            self.board = copy.deepcopy(node)

            if self.__isValidSuccessor() :
                if self.isSolved() :
                    print "Run-time complexity = " + str(runtime)
                    print "Space complexity = " + str(space) + "\n"
                    return self.printBoard()
                    
                indices = [(node.index(item), item.index(0)) for item in
                node if item.count(0) > 0]
                
                if indices : #if list is not empty
                    [frontier.put(copy.deepcopy(self.__generateSuccessor(item,
                    indices[0], node))) for item in range(1,10)]
                    runtime = runtime + 9
                
                space = max(space, frontier.qsize())
                
    def runModifiedBFS(self) :
        runtime = 0 # number of times successor f(x) was called
        space = 1 # maximum queue length over the run of the entire alg
        
        node = copy.deepcopy(self.board)
        if self.isSolved() :
            return True
        frontier = Queue.Queue()
        frontier.put(copy.deepcopy(node))

        while True :
            node = copy.deepcopy(frontier.get())
            self.board = copy.deepcopy(node)

            if self.__isValidSuccessor() :
                if self.isSolved() :
                    print "Run-time complexity = " + str(runtime)
                    print "Space complexity = " + str(space) + "\n"
                    return self.printBoard()

                indices = [(node.index(item), item.index(0)) for item in
                node if item.count(0) > 0]
                
                if indices : #if list is not empty
                    [frontier.put(copy.deepcopy(self.__generateSuccessor(item,
                    indices[0], node))) for item in range(1,10)]
                    runtime = runtime + 9
                space = max(space, frontier.qsize())

    def __calculateCost(self) :
        cost = 0
        li = [(0,0),(4,1),(8,2),(1,3),(5,4),(6,5),(2,6),(3,7),(7,8)]
        for pos in li :
            constraints = self.getConstraintSets(pos)
            cost = cost + len(self.computeUnusedNums(constraints[0])) + len(self.computeUnusedNums(constraints[1]))+ len(self.computeUnusedNums(constraints[2]))
        return cost

    def runSimulatedAnnealing(self, T, seed) :
        curr_p = seed #initialize p(0)
        prev_p = seed
        a_uphill = 0
        r_uphill = 0
        downhill = 0
        iterations = 0

        # fill in board only following column constraints
        constraints = [set([(0,i),(1, i), (2, i), (3, i), (4, i), (5, i), (6,
        i), (7, i), (8, i)]) for i in range(0,9)]
        nonfixed = copy.deepcopy(constraints)
        
        for col in constraints :
            unused = list(self.computeUnusedNums(col))[:]
            for pos in col :
                if self.board[pos[0]][pos[1]] == 0 :
                    num = random.choice(unused)
                    self.board[pos[0]][pos[1]] = num
                    unused.remove(num)
                else :
                    nonfixed[constraints.index(col)].remove(pos)
                    
        if self.isSolved() :
            return True

        bestBoard = copy.deepcopy(self.board)
        currBoard = copy.deepcopy(self.board)
        prevCost = self.__calculateCost()
        currCost = self.__calculateCost()
        
        while T : # perform loop as long as T > 0
            prevBoard = copy.deepcopy(self.board)

            seq  = list(random.choice(nonfixed))
            while len(seq) <= 1 :
                seq  = list(random.choice(nonfixed))
            pos1 = random.choice(seq)
            pos2 = random.choice(seq)

            while pos2 == pos1 :
                pos2 = random.choice(seq)
                
            self.__swapSquares(pos1, pos2, currBoard)

            self.board = copy.deepcopy(currBoard)
            currCost = self.__calculateCost()
            
            if currCost < prevCost :
                bestBoard = copy.deepcopy(currBoard)
                prevCost = currCost
                downhill = downhill + 1
            else :
                q = random.random()
                if q > curr_p :
                    # revert to previous board
                    currBoard = copy.deepcopy(prevBoard)
                    self.Board = copy.deepcopy(currBoard)
                    r_uphill = r_uphill + 1
                else :
                    prevCost = currCost
                    a_uphill = a_uphill + 1
                    
            curr_p = 0.99 * prev_p    
            prev_p = curr_p
            
            T = T - 1
            iterations = iterations + 1

            if self.isSolved() :
                print "Seed Value = " + str(seed)
                print "Iterations = " + str(iterations)
                print "Downhill Moves = " + str(downhill)
                print "Lowest Cost Found = 0"
                print "Rejected Uphill Moves = " + str(r_uphill)
                print "Accepted Uphill Moves = " + str(a_uphill)
                print "Sudoku Puzzle Solved = True"
                return self.printBoard()

        self.board = copy.deepcopy(bestBoard)
        print "Seed Value = " + str(seed)
        print "Downhill Moves = " + str(downhill)
        print "Iterations = " + str(iterations)
        print "Lowest Cost Found = " + str(self.__calculateCost())
        print "Rejected Uphill Moves = " + str(r_uphill)
        print "Accepted Uphill Moves = " + str(a_uphill)
        print "Sudoku Puzzle Solved = False"
        return self.printBoard()

    def __swapSquares(self, (r1, c1), (r2,c2), board) :
        num1 = board[r1][c1]
        num2 = board[r2][c2]

        board[r1][c1] = num2
        board[r2][c2] = num1
