import numpy as np
import random


class AI1():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows" 
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare

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

        unopenedSquares = []
        notBombs = []
        bombsFoundSoFar = []
        for row in range(self.numRows):
            for col in range(self.numCols):
                if boardState[row][col] == -1:
                    unopenedSquares.append((row, col))
                # if square is zero, add all adjacent squares into notBombs list.
                elif boardState[row][col] == 0:
                    notBombs.append((row, col))
                    notBombs.extend([(row + 1, col + 1), (row - 1, col - 1), (row + 1, col), (row - 1, col),
                                     (row, col + 1), (row, col - 1), (row + 1, col - 1), (row - 1, col + 1)])
                elif boardState[row][col] == 9:
                    bombsFoundSoFar.append((row, col))
                # if square is 2-8
                else:
                    counter = 0
                    adjacentTiles = []
                    # add adjacent tiles into adjacentTiles list
                    adjacentTiles.extend([(row + 1, col + 1), (row - 1, col - 1), (row + 1, col), (row - 1, col),
                                          (row, col + 1), (row, col - 1), (row + 1, col - 1), (row - 1, col + 1)])

                    # loop through adjacent tiles and count number of unopened tiles and bombs
                    for x, y in adjacentTiles:
                        if x == -1 or y == -1 or x == self.numRows or y == self.numCols:
                            continue
                        elif boardState[x][y] == -1:
                            counter += 1
                        elif boardState[x][y] == 9:
                            counter += 1

                    # if counter is equal to center tile, add all unopened tiles to bombsFoundSoFar list
                    if counter == boardState[row][col]:
                        for x, y in adjacentTiles:
                            if x == -1 or y == -1 or x == self.numRows or y == self.numCols:
                                continue

                            elif boardState[x][y] == -1 and (x, y) not in bombsFoundSoFar:
                                bombsFoundSoFar.append((x, y))
                    adjacentTiles.clear()

        if len(bombsFoundSoFar) == self.numBombs:
            # If the number of unopened squares is equal to the number of bombs, all squares must be bombs, and we can submit our answer
            print(f"List of bombs is {bombsFoundSoFar}")
            return self.submit_final_answer_format(bombsFoundSoFar)
        else:
            # pick a random square
            squareToOpen = random.choice(unopenedSquares)

            # if square in notBombs or bombsFoundSoFar, pick a new square
            while squareToOpen in notBombs:
                squareToOpen = random.choice(unopenedSquares)
                while squareToOpen in bombsFoundSoFar:
                    squareToOpen = random.choice(unopenedSquares)
            print(f"Square to open is {squareToOpen}")
            return self.open_square_format(squareToOpen)
