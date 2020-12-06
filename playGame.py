import sys
import connect4_MCTS
import pygame

'''
Connect 4 class that is used to maintain information for the pygame display. It wraps the MCTS functionality.
'''
class Connect4:
    def __init__(self, size):
        # Pygame initialization
        pygame.init()
        self.clock = pygame.time.Clock()
        
        # Setting up main window
        self.square_size = 100
        self.size = size
        self.screen_height = self.square_size * (size[0] + 1)
        self.screen_width = self.square_size * (size[1])
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Connect 4")
        
        # Colors that are used throughout the window.
        self.bgColor = pygame.Color('grey12')
        self.light_grey = (200,200,200)  
        self.boardColor = (50,131,168)
        self.playerColor = (245,245,66)
        self.AIColor = (245,66,66)

    '''
    Draws the board according to the input state.
    State is given in the form of a tuple of tuples.
    '''
    def drawBoard(self, state):
        # Cols, rows, square size, and circle size
        cols = self.size[1]
        rows = self.size[0]
        size = self.square_size
        circleSize = size - 6
        for c in range(cols):
            for r in range(rows):
                # Top is row 0
                # Increases down
                pygame.draw.rect(self.screen, self.boardColor, ((c*size, r*size + self.square_size),(size-1,size-1)))
                # Drawing circles (black if empty, colour of the player that placed them otherwise)
                if r < (cols - len(state[c]) - 1):
                    pygame.draw.circle(self.screen, self.bgColor, (c*size + (size // 2),r*size + (2*size - size // 2)), int(circleSize // 2))
                else:
                    stateRowIndex = rows - r - 1
                    if state[c][stateRowIndex] == 'x':
                        pygame.draw.circle(self.screen, self.AIColor, (c*size + (size // 2),r*size + (2*size - size // 2)), int(circleSize // 2))
                    else:
                        pygame.draw.circle(self.screen, self.playerColor, (c*size + (size // 2),r*size + (2*size - size // 2)), int(circleSize // 2))
                        
    '''
    Contains the game loop and the running of the MCTS algorithm.
    '''
    def play(self, human=True, n=10000):
        # Init game settings
        width = 7
        initial = ((),) * width

        game = connect4_MCTS.ConnectFour()
        state = initial
        player = game.player1
        computer = game.player2
        playerTurn = True

        # Game loop
        while not game.isTerminalState(state):
            # Human player action
            if playerTurn:
                # Event handling
                for event in pygame.event.get():
                    # Event: Quit
                    if event.type == pygame.QUIT:
                        sys.exit()
                    # Event: Click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # While a legal action has not been taken:
                        success = False
                        while not success:
                            # Getting the choice based on the click ->  Turning it into a valid choice
                            choice = event.pos[0] // self.square_size
                            try:
                                action = int(choice)
                                if action not in game.actions(state):
                                    print("Illegal move!")
                                    break
                                # Player made a legal action, take it
                                state = game.resultingState(state, action, player)
                                success = True
                            except ValueError:
                                pass
                            except Exception:
                                pass
                        if success:
                            print(game.pretty_state(state, False))
                            playerTurn = False
            else:
                # Computer turn
                action = connect4_MCTS.monteCarloTreeSearch(game, state, computer)
                state = game.resultingState(state, action, computer)
                print(game.pretty_state(state, False))
                playerTurn = True

            # Intermediate win check
            if game.isTerminalState(state):
                break
            
            # Applying the changes to the pygame window
            self.screen.fill(self.bgColor)
            self.drawBoard(state)
            pygame.display.update()
            self.clock.tick(60)

        # print(game.pretty_state(state, False))
        # print()
        outcome = game.gameOutcome(state, player)
        if outcome == 1:
            print('Player 1 wins.')
        elif outcome == -1:
            print('Player 2 wins.')
        else:
            print('Tie game.')
            
        # TODO: Address the issue with left diagonal win evaluation

# Driver code
def main():
    n = 1000
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            pass

    n = 1000
    if '-n' in sys.argv:
        try:
            n = int(sys.argv[sys.argv.index('-n') + 1])
        except:
            pass

    human = True
    if '-c' in sys.argv:
        human = False
        
    size = (6,7)
        
    connect4 = Connect4(size)
    
    print('Number of Sample Iterations: ' + str(n))
    print('Human Player: ' + str(human))
    print()
    connect4.play(n=n, human=human)


if __name__ == "__main__":
    main()