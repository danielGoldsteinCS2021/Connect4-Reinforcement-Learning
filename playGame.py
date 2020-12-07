import sys
import connect4_MCTS
import pygame
from enum import Enum

'''
Connect 4 class that is used to maintain information for the pygame display. It wraps the MCTS functionality.
'''
class Difficulty:
    EASY = 100
    MEDIUM = 1200
    HARD = 4700

class Connect4:
    def __init__(self, size):
        # Pygame initialization
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        
        # Setting up main window
        self.square_size = 100
        self.size = size
        self.screen_height = self.square_size * (size[0] + 1)
        self.screen_width = self.square_size * (size[1])
        self.button_width = 75
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Connect 4")
        
        # Colors that are used throughout the window.
        self.bgColor = pygame.Color('grey12')
        self.light_grey = (200,200,200)  
        self.dark_grey = (150,150,150)
        self.boardColor = (50,131,168)
        self.playerColor = (245,245,66)
        self.AIColor = (245,66,66)
        
        # Font
        self.font = pygame.font.SysFont("monospace", 30)
        self.smallFont = pygame.font.SysFont("monospace", 20)
        
        # Difficulty buttons
        self.hardButton = pygame.Rect(self.screen_width - self.button_width,25,self.button_width - 5,50)
        self.mediumButton = pygame.Rect(self.screen_width - (2 * self.button_width),25,self.button_width - 5,50)
        self.easyButton = pygame.Rect(self.screen_width - (3 * self.button_width),25,self.button_width - 5,50)
        
        # Initial difficulty:
        self.difficulty = Difficulty.EASY;

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
    Draws buttons and button text
    '''
    def drawButtons(self):
        if self.difficulty == Difficulty.EASY:
            pygame.draw.rect(self.screen, self.dark_grey, self.easyButton)
            pygame.draw.rect(self.screen, self.light_grey, self.mediumButton)
            pygame.draw.rect(self.screen, self.light_grey, self.hardButton)
        elif self.difficulty == Difficulty.MEDIUM:
            pygame.draw.rect(self.screen, self.light_grey, self.easyButton)
            pygame.draw.rect(self.screen, self.dark_grey, self.mediumButton)
            pygame.draw.rect(self.screen, self.light_grey, self.hardButton)
        else:
            pygame.draw.rect(self.screen, self.light_grey, self.easyButton)
            pygame.draw.rect(self.screen, self.light_grey, self.mediumButton)
            pygame.draw.rect(self.screen, self.dark_grey, self.hardButton)
            
        # Text
        easyText = self.smallFont.render("Easy", True, (0,0,0))
        easy_text_rect = easyText.get_rect(center=self.easyButton.center)
        mediumText = self.smallFont.render("Med", True, (0,0,0))
        medium_text_rect = mediumText.get_rect(center=self.mediumButton.center)
        hardText = self.smallFont.render("Hard", True, (0,0,0))
        hard_text_rect = hardText.get_rect(center=self.hardButton.center)
        
        self.screen.blit(easyText, easy_text_rect)
        self.screen.blit(mediumText, medium_text_rect)
        self.screen.blit(hardText, hard_text_rect)
       
    '''
    Pygame update: Refresh
    '''
    def update(self, state):
        self.screen.fill(self.bgColor)
        self.drawBoard(state)
        self.drawButtons()
        pygame.display.update()
        self.clock.tick(60)
        
    '''
    Player-specific update, draws "Player turn" to the window
    '''
    def playerUpdate(self, state):
        self.screen.fill(self.bgColor)
        self.drawBoard(state)
        self.drawButtons()
        text_surface = self.font.render("Your move...", True, self.light_grey)
        text_rect = text_surface.get_rect(center=(self.screen_width/4, 50))
        self.screen.blit(text_surface, text_rect)
        pygame.display.update()
                        
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
                self.playerUpdate(state)
                # Event handling
                for event in pygame.event.get():
                    # Event: Quit
                    if event.type == pygame.QUIT:
                        sys.exit()
                    # Event: Click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.Rect.collidepoint(self.easyButton, pygame.mouse.get_pos()):
                            self.difficulty = Difficulty.EASY
                        if pygame.Rect.collidepoint(self.mediumButton, pygame.mouse.get_pos()):
                            self.difficulty = Difficulty.MEDIUM
                        if pygame.Rect.collidepoint(self.hardButton, pygame.mouse.get_pos()):
                            self.difficulty = Difficulty.HARD
                            
                        # While a legal action has not been taken:
                        if event.pos[1] >= self.square_size:
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
                
                # Computer waiting text
                self.update(state)
                text_surface = self.font.render("AI thinking...", True, self.light_grey)
                text_rect = text_surface.get_rect(center=(self.screen_width/4, 50))
                self.screen.blit(text_surface, text_rect)
                pygame.display.update()
                # self.update(state)
                
                # Computer action
                action = connect4_MCTS.monteCarloTreeSearch(game, state, computer, self.difficulty)
                state = game.resultingState(state, action, computer)
                print(game.pretty_state(state, False))
                playerTurn = True

            # Intermediate win check
            if game.isTerminalState(state):
                # If the game is over, print winner and exit
                self.update(state)
                
                # Game outcome:
                if game.gameOutcome(state, player) == 1:
                    # Player wins
                    text_surface = self.font.render("Player 1 Wins!", True, self.light_grey)
                    text_rect = text_surface.get_rect(center=(self.screen_width/2, 50))
                    self.screen.blit(text_surface, text_rect)
                elif game.gameOutcome(state, player) == -1:
                    # Computer wins:
                    text_surface = self.font.render("Computer Wins!", True, self.light_grey)
                    text_rect = text_surface.get_rect(center=(self.screen_width/2, 50))
                    self.screen.blit(text_surface, text_rect)
                else:
                    # Tie
                    text_surface = self.font.render("It's a tie!", True, self.light_grey)
                    text_rect = text_surface.get_rect(center=(self.screen_width/2, 50))
                    self.screen.blit(text_surface, text_rect)
                
                # self.update(state)
                pygame.display.update()
                pygame.time.wait(3000)
                break
                
            # Applying the changes to the pygame window
            # self.update(state)

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