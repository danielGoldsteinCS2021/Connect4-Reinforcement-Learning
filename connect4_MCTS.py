import queue
from math import sqrt, log
from random import sample

'''
This file contains the template for all methods we will need to implement 
to have our connect4 game
'''

class ConnectFour:
    # represents possible actions we can take
    def actions(self, state):
        return

    # creates and returns the resulting state
    def result(self, state, action, player):
        pass

    # returns true and false based on if we reached a terminal state
    def terminal(self, state):
        pass

    # determines who next player is
    def next_player(self, state):
        pass

    # determines outcome of game upon completion, returns win, lose, draw values
    def outcome(self, state, player):
        pass

    def __init__(self):
        self.player1 = 'x'
        self.player2 = 'o'
        self.height = 6
        self.width = 7
        self.connectNumber = 4
        self.win = 1
        self.lose = -1
        self.draw = 0

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


