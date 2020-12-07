from math import sqrt, log
from random import choice

'''
The first class is our ConnectFour class which defines the logic and rules
of our ConnectFour game. It determines when the game has reached a terminal or
winning state and creates the necessary attributes and methods needed to play the game.

States are represented as a tuple of tuples. For our game we will have each tuple 
have a max of self.height many integers. The tuples are column based - not row based!
Examples of states 
((), (), (), (), (), (), ()) - this will be our initial state
((x), (), (), (), (), (), ()) - state after first move
((x), (o, o, o, o), (x, x, x), (), (), (), ()) - winner is o
'''


class ConnectFour:
    def __init__(self):
        self.player1 = 'x'
        self.player2 = 'o'
        self.height = 6
        self.width = 7
        self.connectNumber = 4
        self.win = 1
        self.lose = -1
        self.tie = 0

    # creates and returns the resulting state based on taken action
    def resultingState(self, state, action, player):
        returnState = []
        for i, col in enumerate(state):
            if i == action:
                returnState.append(col + (player,))
            else:
                returnState.append(col)
        return tuple(returnState)

    # returns true and false based on if we reached a terminal state
    def isTerminalState(self, state):
        if all([len(col) == self.height for col in state]):
            return True  # board is full
        if self.gameOutcome(state, self.player1) == self.win or self.gameOutcome(state, self.player1) == self.lose:
            return True  # there is a winner, so we're in a terminal state
        return False

    # tuple returned represents the possible actions we can take
    def actions(self, state):
        possibleActions = [i for i in range(self.width) if len(state[i]) < self.height]
        return tuple(possibleActions)

    # determines who next player is
    def nextPlayer(self, player):
        if self.player1 == player:
            return self.player2
        return self.player1

    # determines if players streak (aka 'connection') has been broken
    def streakHandler(self, playerToCompare, p1_count, p2_count):
        if playerToCompare == self.player1:
            p2_count = 0  # player2 streak has been broken
            p1_count += 1
        else:
            p1_count = 0  # player1 streak has been broken
            p2_count += 1
        return p1_count, p2_count

    # Determines if game has ended based on up and down (vertical) connections
    def isGameOverUpDown(self, state):
        for colIdx in range(self.width):  # for each column
            p1_count, p2_count = 0, 0
            for i in range(self.height):  # for each row
                try:
                    playerAtCurPos = state[colIdx][i]
                except IndexError:
                    break  # no more elements vertically
                p1_count, p2_count = self.streakHandler(playerAtCurPos, p1_count, p2_count)
                if p1_count == self.connectNumber:
                    return True, self.player1
                if p2_count == self.connectNumber:
                    return True, self.player2
        return False, None  # no winner found

    # Determines if game has ended based on left and right connections
    def isGameOverLeftRight(self, state):
        for rowIdx in range(self.height):  # traverse by row
            p1_count, p2_count = 0, 0
            for i in range(self.width):  # traverse by column
                try:
                    valueAtCurPos = state[i][rowIdx]
                except IndexError:
                    p1_count, p2_count = 0, 0  # reset count because there is no element here
                    continue  # move to next column
                p1_count, p2_count = self.streakHandler(valueAtCurPos, p1_count, p2_count)  # update streaks
                if p1_count == self.connectNumber:
                    return True, self.player1
                if p2_count == self.connectNumber:
                    return True, self.player2
        return False, None  # no winner

    # Determines if game has ended based on diag connections
    def isGameOverDiag(self, state):
        # diagonal check from the top left to the bottom right
        for col in range(7):
            for row in range(6):
                try:
                    temp = state[col][row]
                    temp = state[col + 1][row - 1]
                    temp = state[col + 2][row - 2]
                    temp = state[col + 3][row - 3]
                except IndexError:
                    continue  # not all indices we're looking at are defined
                if row - 3 < 0:
                    continue
                if state[col][row] == state[col + 1][row - 1] == state[col + 2][row - 2] == \
                        state[col + 3][row - 3] == self.player1:
                    return True, self.player1
                if state[col][row] == state[col + 1][row - 1] == state[col + 2][row - 2] == \
                        state[col + 3][row - 3] == self.player2:
                    return True, self.player2

        # diagonal check from the bottom left to the top right
        for col in range(7):
            for row in range(6):
                try:
                    temp = state[col][row]
                    temp = state[col + 1][row + 1]
                    temp = state[col + 2][row + 2]
                    temp = state[col + 3][row + 3]
                except IndexError:
                    continue  # not all indices we're looking at are defined
                if state[col][row] == state[col + 1][row + 1] == state[col + 2][row + 2] == \
                        state[col + 3][row + 3] == self.player1:
                    return True, self.player1
                if state[col][row] == state[col + 1][row + 1] == state[col + 2][row + 2] == \
                        state[col + 3][row + 3] == self.player2:
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
    def gameOutcome(self, state, player):
        gameOver = self.isGameOver(state)
        if gameOver == player:
            return self.win
        if gameOver is not None:  # the other player has won
            return self.lose
        return self.tie  # game over is None - no winner has been determined yet

    # TODO: THIS CODE NEEDS TO BE CHANGED - however it just prints the game board pretty not needed for logic of game
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
This class is for using the Monte Carlo Tree Search algorithm and inherits our ConnectFour class defined above.
It uses the methods and attributes defined in ConnectFour and applies the MCTS algorithm to them. 
'''


class Node(ConnectFour):
    def __init__(self, daddyNode, action, state, player, game=None):
        super().__init__()  # for connect4 class
        self.game = game
        self.parentNode = daddyNode
        self.childNodes = dict.fromkeys(self.actions(state))  # creates dict keys that are made of actions.
        self.action = action
        self.state = state
        self.player = player
        self.visits = 0  # needed for MCTS algorithm
        self.value = 0.0  # needed for MCTS algorithm

    # returns the weight of the node based on visits - needed for MCTS
    def nodeWeightForVisits(self):
        return self.value / self.visits if self.visits > 0 else 0

    # computes the formula needed to determine the search weight
    def mctsWeightFormula(self, c):
        return self.nodeWeightForVisits() + c * sqrt(2 * log(self.parentNode.visits) / self.visits)

    # ensures no child nodes are set to None, i.e that have all been expanded
    def allChildrenExpanded(self):
        return None not in self.childNodes.values()

    # expands nodes that haven't been expanded yet, needed for expansion step in MCTS
    def expandNode(self):
        try:
            indexOfNoneNode = list(self.childNodes.values()).index(None)  # cast to a list to use .index() method
            listOfChildNodeKeys = list(self.childNodes.keys())
            action = listOfChildNodeKeys[indexOfNoneNode]
        except ValueError:
            pass  # do nothing
        newState = self.resultingState(self.state, action, self.player)
        nextPlayer = self.nextPlayer(self.player)
        childNode = Node(self, action, newState, nextPlayer)
        self.childNodes[action] = childNode  # map our action to a new childNode
        return childNode  # return expanded node

    # returns the value for the optimal child node, all nodes must be fully expanded.
    def optimalChildNode(self, cVal=1 / sqrt(2)):
        returnValue = None
        if self.allChildrenExpanded():
            returnValue = max(self.childNodes.values(), key=lambda node: node.mctsWeightFormula(cVal))
        return returnValue

    # returns the action taken by the optimal child node
    def optimalAction(self, cVal=1 / sqrt(2)):
        return self.optimalChildNode(cVal).action

    # this simulates the game from it's current state to a terminal state, used for simulation step in MCTS
    def simulate(self):
        player = self.player
        state = self.state
        while not self.isTerminalState(state):  # while game isn't over
            nextAction = choice(self.actions(state))  # choose random action
            state = self.resultingState(state, nextAction, player)
            player = self.nextPlayer(player)
        return self.gameOutcome(state, player)


# This function runs the Monte Carlo Tree Search algorithm using
# the methods defined in our node class
def monteCarloTreeSearch(connect4Game, state, player, numOfIterations=4500):
    rootNode = Node(None, None, state, player, connect4Game)
    for _ in range(numOfIterations):
        curNode = rootNode
        while not curNode.isTerminalState(curNode.state):  # as long as we can still make moves
            if not curNode.allChildrenExpanded():
                curNode = curNode.expandNode()  # if we haven't expanded yet, expand
                break
            curNode = curNode.optimalChildNode()  # all nodes have been expanded, choose the optimal one
        # initial policy
        deltaValue = curNode.simulate()  # simulate playing game
        # Do backpropagation
        while curNode is not None:
            curNode.visits += 1
            curNode.value += deltaValue
            curNode = curNode.parentNode
    return rootNode.optimalAction(0)  # take the optimal action
