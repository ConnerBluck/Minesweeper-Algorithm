import numpy as np
import random
import operator

class AI2():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):   

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows" 
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare
        self.centerSquare = safeSquare
        self.listOfBombs = set()
        self.unsatisfied = dict() # dictionary of unsatisfied numbers showing on the board and their coordinates
        self.offLimits = [] # known bombs, known non-bombs
        self.center_unsatisfied = 0
        self.square = None
        self.last_bomb = -1

    def open_square_format(self, squareToOpen):
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    # return the square (r, c) you want to open based on the given boardState
    # the boardState will contain the value (0-8 inclusive) of the square, or -1 if that square is unopened
    # an AI example that returns a random square (r, c) that you want to open
    # TODO: implement a better algorithm
    def performAI(self, boardState):
        print(boardState)

        # find all the unopened squares, excluding known bombs and known non-bombs
        unopenedSquares = []
        for row in range(self.numRows):
            for col in range(self.numCols):
                if ((boardState[row][col] == -1) and ((row, col) not in self.offLimits)):
                    unopenedSquares.append((row, col))
                if ((boardState[row][col] == 9)):
                    self.listOfBombs.add((row,col))

        # add last bomb to list of bombs before returning - potentially unnecessary attempt to fix a bug
        if (self.last_bomb != -1 and boardState[self.last_bomb[0]][self.last_bomb[1]] == 9):
            self.listOfBombs.add(self.last_bomb)

        # return final list unless we still have to go through the last square to be opened
        if self.center_unsatisfied != 1 and (len(self.listOfBombs) + len(unopenedSquares)) == self.numBombs:
            # If the number of found bombs + unopened squares is equal to the number of bombs, all remaining squares must be bombs, and we can submit our answer
            print(f"List of bombs is {list(self.listOfBombs) + unopenedSquares}")
            return self.submit_final_answer_format(list(self.listOfBombs) + unopenedSquares)
        if self.center_unsatisfied != 1 and (len(self.listOfBombs) == self.numBombs):
            # If the number of found bombs is equal to the number of bombs we can submit our answer
            print(f"List of bombs is {list(self.listOfBombs)}")
            return self.submit_final_answer_format(list(self.listOfBombs))
        else:
            # if we mined a new square around the center in the previous iteration
            if self.center_unsatisfied == 1:
                squareToOpen = self.square
                (sub_grid, sub_bombs, sub_nonbombs) = self.findSurroundingGrid(squareToOpen, boardState) # surrounding grid of mined square
                if boardState[squareToOpen[0]][squareToOpen[1]] > 0 and boardState[squareToOpen[0]][squareToOpen[1]] < 8: # non-deterministic number
                    # mined square is satisfied
                    if sub_bombs == boardState[squareToOpen[0]][squareToOpen[1]]:
                        for coord in sub_grid:
                            self.offLimits.append(coord)
                    elif sub_bombs + len(sub_grid) == boardState[squareToOpen[0]][squareToOpen[1]]:
                        for coord in sub_grid:
                            self.offLimits.append(coord)
                            self.listOfBombs.add(coord)
                            print(coord)
                    else: # mined square is unsatisfied
                        self.unsatisfied[squareToOpen] = boardState[squareToOpen[0]][squareToOpen[1]]
                        if boardState[squareToOpen[0]][squareToOpen[1]] > boardState[self.centerSquare[0]][self.centerSquare[1]]:
                            self.centerSquare = squareToOpen
                elif boardState[squareToOpen[0]][squareToOpen[1]] == 0: # mined square is a 0
                    for coord in sub_grid:
                        self.offLimits.append(coord)
                elif boardState[squareToOpen[0]][squareToOpen[1]] == 8: # mined square is an 8
                    for coord in sub_grid:
                        self.offLimits.append(coord)
                        self.listOfBombs.add(coord)
                        print(coord)
                elif boardState[squareToOpen[0]][squareToOpen[1]] == 9: # mined square is a bomb
                    self.listOfBombs.add(squareToOpen)
                    self.offLimits.append(squareToOpen)
                    print(squareToOpen)
                self.center_unsatisfied = 0

            # check for termination
            if (len(self.listOfBombs) + len(unopenedSquares)) == self.numBombs:
                # If the number of found bombs + unopened squares is equal to the number of bombs, all remaining squares must be bombs, and we can submit our answer
                print(f"List of bombs is {list(self.listOfBombs) + unopenedSquares}")
                return self.submit_final_answer_format(list(self.listOfBombs) + unopenedSquares)
            if (len(self.listOfBombs) == self.numBombs):
                # If the number of found bombs is equal to the number of bombs we can submit our answer
                print(f"List of bombs is {list(self.listOfBombs)}")
                return self.submit_final_answer_format(list(self.listOfBombs))
            
            # normal process
            (grid, bombs, nonbombs) = self.findSurroundingGrid(self.centerSquare, boardState)
            # extra stuff to do first if the center square is the safe square
            if (self.centerSquare is self.safeSquare):
                if boardState[self.centerSquare[0]][self.centerSquare[1]] == 0: # if safe square is 0, this is the max number on the board so there are no bombs
                    return self.submit_final_answer_format(list(self.listOfBombs))
            self.unsatisfied[self.centerSquare] = boardState[self.centerSquare[0]][self.centerSquare[1]]
            # regular case, where the center is a non-deterministic number
            if (boardState[self.centerSquare[0]][self.centerSquare[1]] > 0 and boardState[self.centerSquare[0]][self.centerSquare[1]] < 8):
                # if center is satisfied
                if ((bombs == boardState[self.centerSquare[0]][self.centerSquare[1]]) or (bombs + len(grid) == boardState[self.centerSquare[0]][self.centerSquare[1]])):
                    self.unsatisfied.pop(self.centerSquare)
                    for coord in grid:
                        if (bombs + len(grid) == boardState[self.centerSquare[0]][self.centerSquare[1]]):
                            self.listOfBombs.add(coord)
                            print(coord)
                        self.offLimits.append(coord)
                    # choosing new center
                    if len(self.unsatisfied) != 0: # there are unsatisfied numbers on the board
                        self.centerSquare = max(self.unsatisfied.items(), key=operator.itemgetter(1))[0]
                        (grid, bombs, nonbombs) = self.findSurroundingGrid(self.centerSquare, boardState)
                        while (len(grid) == 0):
                            self.unsatisfied.pop(self.centerSquare)
                            if len(self.unsatisfied) != 0:
                                self.centerSquare = max(self.unsatisfied.items(), key=operator.itemgetter(1))[0]
                                (grid, bombs, nonbombs) = self.findSurroundingGrid(self.centerSquare, boardState)
                            else:
                                grid = [1]
                        if len(self.unsatisfied) == 0:
                            self.centerSquare = random.choice(unopenedSquares)
                            squareToOpen = self.centerSquare
                            print("here1")
                        else:
                            self.center_unsatisfied = 1
                            squareToOpen = random.choice(grid)
                            print("here2")
                            self.square = squareToOpen
                    else:
                        self.centerSquare = random.choice(unopenedSquares)
                        squareToOpen = self.centerSquare
                        if (len(unopenedSquares) == 0):
                            self.last_bomb = self.centerSquare
                        print("here3")
                    print(f"Square to open is {squareToOpen}")
                    print("loc2")
                    return self.open_square_format(squareToOpen)
                # if center is not yet satisfied
                else:
                    self.center_unsatisfied = 1
                    squareToOpen = random.choice(grid)
                    self.square = squareToOpen
                    print(f"Square to open is {squareToOpen}")
                    print("loc3")
                    return self.open_square_format(squareToOpen)         
            # edge cases, where center is an 8, a 0, or a bomb
            else:
                # special case where center tile is an 8
                if (boardState[self.centerSquare[0]][self.centerSquare[1]] == 8):
                    for coord in grid:
                        self.offLimits.append(coord)
                        unopenedSquares.remove(coord)
                        self.listOfBombs.add(coord)
                        print(coord)
                    self.unsatisfied.pop(self.centerSquare)
                # special case where center tile is a bomb
                if (boardState[self.centerSquare[0]][self.centerSquare[1]] == 9):
                    self.listOfBombs.add(self.centerSquare)
                    self.offLimits.append(self.centerSquare)
                    print(self.centerSquare)
                    self.unsatisfied.pop(self.centerSquare)
                # special case where center tile is a 0
                if (boardState[self.centerSquare[0]][self.centerSquare[1]] == 0):
                    for coord in grid:
                        self.offLimits.append(coord)
                        unopenedSquares.remove(coord)
                    self.unsatisfied.pop(self.centerSquare)
                # choosing new center square
                if len(self.unsatisfied) != 0:
                    self.centerSquare = max(self.unsatisfied.items(), key=operator.itemgetter(1))[0]
                    (grid, bombs, nonbombs) = self.findSurroundingGrid(self.centerSquare, boardState)
                    if len(self.unsatisfied) != 0:
                        self.centerSquare = max(self.unsatisfied.items(), key=operator.itemgetter(1))[0]
                        (grid, bombs, nonbombs) = self.findSurroundingGrid(self.centerSquare, boardState)
                        while (len(grid) == 0):
                            self.unsatisfied.pop(self.centerSquare)
                            if len(self.unsatisfied) != 0:
                                self.centerSquare = max(self.unsatisfied.items(), key=operator.itemgetter(1))[0]
                                (grid, bombs, nonbombs) = self.findSurroundingGrid(self.centerSquare, boardState)
                            else:
                                grid = [1]
                        if len(self.unsatisfied) == 0:
                            if (len(unopenedSquares) == 0):
                                return self.submit_final_answer_format(list(self.listOfBombs))
                            self.centerSquare = random.choice(unopenedSquares)
                            squareToOpen = self.centerSquare
                        else:
                            self.center_unsatisfied = 1
                            squareToOpen = random.choice(grid)
                            self.square = squareToOpen
                else:
                    if (len(unopenedSquares) == 0):
                        return self.submit_final_answer_format(list(self.listOfBombs))
                    self.centerSquare = random.choice(unopenedSquares)
                    squareToOpen = self.centerSquare
                print(f"Square to open is {squareToOpen}")
                print("loc1")
                return self.open_square_format(squareToOpen)
    
    def findSurroundingGrid(self, centerSquare, boardState):
        surroundingGrid = []
        numBombs = 0
        numNonBombs = 0
        rows = [centerSquare[0]]
        cols = [centerSquare[1]]
        if (centerSquare[0]-1 >= 0):
            rows.append(centerSquare[0]-1)
        if (centerSquare[0]+1 < self.numRows):
            rows.append(centerSquare[0]+1)
        if (centerSquare[1]-1 >= 0):
            cols.append(centerSquare[1]-1)
        if (centerSquare[1]+1 < self.numCols):
            cols.append(centerSquare[1]+1)
        for row in rows:
            for col in cols:
                if boardState[row][col] == -1 and not((row, col) in self.offLimits):
                    surroundingGrid.append((row, col))
                elif boardState[row][col] == 9 or (row,col) in self.listOfBombs:
                    numBombs += 1
                elif (row, col) in self.offLimits:
                    numNonBombs += 1
        return surroundingGrid, numBombs, numNonBombs