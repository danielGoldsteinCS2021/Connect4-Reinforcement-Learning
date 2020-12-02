import queue
from math import sqrt, log
from random import sample

'''
This file contains the template for all methods we will need to implement 
to have our connect4 game
'''

'''
States are represented as a tuple of tuples. For our game we will have each tuple 
have a max of self.height many integers. The tuples are column based - not row based!
Examples of states 
((), (), (), (), (), (), ()) - this will be our initial state
((x), (), (), (), (), (), ()) - state after first move
((x), (o, o, o, o), (x, x, x), (), (), (), ()) - winner is o
'''
# Top level macros
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
DIAGONAL = 'DIAGONAL'


class ConnectFour:
    def __init__(self):
        self.player1 = 'x'
        self.player2 = 'o'
        self.turn = self.player1
        self.height = 6
        self.width = 7
        self.connectNumber = 4
        self.win = 1
        self.lose = -1
        self.draw = 0

    # represents possible actions we can take
    def actions(self, state):
        possibleActions = [i for i in range(self.width) if len(state[i]) < self.height]
        return tuple(possibleActions)

    # creates and returns the resulting state
    def resultingState(self, state, action, player):
        returnState = []
        for i, col in enumerate(state):
            if i == action:
                returnState.append(col + (player,))
            else:
                returnState.append(col)
        return returnState

    # returns true and false based on if we reached a terminal state
    def isTerminalState(self, state):
        if all([len(col) == self.height for col in state]):
            return True  # board is full
        if self.outcome(state, self.player1) != self.draw:
            return True  # there is a winner, so we're in a terminal state
        return False

    # determines who next player is
    def next_player(self):
        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1

    # determines if players streak 'connection' has been broken
    def streakHandler(self, playerToCompare, p1_count, p2_count):
        if playerToCompare == self.player1:
            p2_count = 0  # current player2 streak has been broken
            p1_count += 1
        else:
            p1_count = 0  # current player1 streak has been broken
            p2_count += 1
        return p1_count, p2_count

    # Determines if game has ended based on up and down connections
    def isGameOverUpDown(self, state):
        # for up and down
        p1_count, p2_count = 0, 0
        for colIdx in range(self.width):  # for each column
            for i in range(self.height):  # for each row
                try:
                    valueAtCurPos = state[colIdx][i]
                except IndexError:
                    break  # no more elements
                p1_count, p2_count = self.streakHandler(valueAtCurPos, p1_count, p2_count)
                if p1_count == self.connectNumber:
                    return True, self.player1
                if p2_count == self.connectNumber:
                    return True, self.player2
        return False, None

    # Determines if game has ended based on left and right connections
    def isGameOverLeftRight(self, state):
        p1_count = 0
        p2_count = 0
        for rowIdx in range(self.height):  # traverse by row
            for i in range(self.width):  # traverse by column
                try:
                    valueAtCurPos = state[i][rowIdx]
                except IndexError:
                    p1_count, p2_count = 0, 0  # reset count because there is no element here
                    continue  # move to next column
                p1_count, p2_count = self.streakHandler(valueAtCurPos, p1_count, p2_count)
                if p1_count == self.connectNumber:
                    return True, self.player1
                if p2_count == self.connectNumber:
                    return True, self.player2
        return False, None

    # Determines if game has ended based on diag connections
    def isGameOverDiag(self, state):
        # diagonal check top left to bottom right
        for row in range(3):
            for col in range(4):
                try:
                    temp = state[row][col]
                    temp = state[row + 1][col + 1]
                    temp = state[row + 2][col + 2]
                    temp = state[row + 3][col + 3]
                except IndexError:
                    continue  # not all indices we're looking at are defined

                if state[row][col] == state[row + 1][col + 1] == state[row + 2][col + 2] == \
                        state[row + 3][col + 3] == 1:
                    return True, self.player1
                if state[row][col] == state[row + 1][col + 1] == state[row + 2][col + 2] == \
                        state[row + 3][col + 3] == 2:
                    return True, self.player2

        # diagonal check bottom left to top right
        for row in range(5, 2, -1):
            for col in range(3):
                try:
                    temp = state[row][col]
                    temp = state[row - 1][col + 1]
                    temp = state[row - 2][col + 2]
                    temp = state[row - 3][col + 3]
                except IndexError:
                    continue  # not all indices we're looking at are defined

                if state[row][col] == state[row - 1][col + 1] == state[row - 2][col + 2] == \
                        state[row - 3][col + 3] == self.player1:
                    return True, self.player1
                if state[row][col] == state[row - 1][col + 1] == state[row - 2][col + 2] == \
                        state[row - 3][col + 3] == self.player2:
                    return True, self.player2
        return False, None

    def isGameOver(self, state):
        upDown = self.isGameOverUpDown(state)
        upDownBool, upDownPlayer = upDown[0], upDown[1]
        leftRight = self.isGameOverLeftRight(state)
        leftRightBool, leftRightPlayer = leftRight[0], leftRight[1]
        diag = self.isGameOverDiag(state)
        diagBool, diagPlayer = diag[0], diag[1]

        if upDownBool:
            return upDownPlayer
        if leftRightBool:
            return leftRightPlayer
        if diagBool:
            return diagPlayer
        return None

    # determines current outcome of game, whether we're in a draw, win or lose state
    def outcome(self, state, player):
        gameOver = self.isGameOver(state)
        if gameOver == player:
            return self.win
        if gameOver is not None:  # the other player has won
            return self.lose
        return self.draw  # game over is None - no one has won

    # THIS CODE NEEDS TO BE CHANGED - however it just prints the game board pretty not needed for logic of game
    def pretty_state(self, state, escape=False):
        output = ''
        for j in range(self.width):
            output += ' ' + str(j)
        output += ' '
        if escape:
            output += '\\n'
        else:
            output += '\n'
        i = self.height - 1
        while i >= 0:
            for column in state:
                if len(column) > i:
                    output += '|' + str(column[i])
                else:
                    output += '| '
            output += '|'
            if escape:
                output += '\\n'
            else:
                output += '\n'
            i -= 1
        return output


'''
File is to be continued, we also need a Node/tree class
'''
