from connect4 import Connect4
import pygame
import sys
import random
import math

rand = random.Random()


class Connect4_GUI(Connect4):

    # Initialize colours for game board
    blue = (0, 100, 250)
    light_blue = (0, 0, 128)
    black = (0, 0, 0)
    red = (255, 68, 68)
    yellow = (255, 230, 68)

    # Initialize variables for game board
    window_size = 75
    width = Connect4.col_count*window_size
    height = (1+Connect4.row_count)*window_size
    size = (width, height)
    radius = int(window_size/2 - 5)
    screen = pygame.display.set_mode(size)

    # Create the game board based on parameters specified above
    def draw_board(self):
        for col in range(self.col_count):
            for row in range(self.row_count):
                location_size = (col*self.window_size, (row+1)*self.window_size,
                                 self.window_size, self.window_size)
                pygame.draw.rect(self.screen, self.blue, location_size)
                location = (int((col+0.5)*self.window_size),
                            int((row+1.5)*self.window_size))
                pygame.draw.circle(self.screen, self.black,
                                   location, self.radius)

        for col in range(self.col_count):
            for row in range(self.row_count):
                if self.board[row][col] == 1:
                    location = (int((col+0.5)*self.window_size),
                                int((row+1.5)*self.window_size))
                    pygame.draw.circle(self.screen, self.red,
                                       location, self.radius)
                elif self.board[row][col] == -1:
                    location = (int((col+0.5)*self.window_size),
                                int((row+1.5)*self.window_size))
                    pygame.draw.circle(
                        self.screen, self.yellow, location, self.radius)
        pygame.display.update()

    def run_game(self):
        pygame.init()
        font = pygame.font.SysFont("monospace", 25)
        self.draw_board()
        pygame.display.update()

        moves = self.possible_moves()
        player = 1
        human_player = rand.choice([1, -1])
        winner = False
        exiting = False
        while moves != [] and winner == False and exiting == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exiting = True

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.black,
                                     (0, 0, self.width, self.window_size))
                    posx = event.pos[0]
                    if player != 1:
                        pygame.draw.circle(
                            self.screen, self.yellow, (posx, int(self.window_size/2)), self.radius)
                    else:
                        pygame.draw.circle(
                            self.screen, self.red, (posx, int(self.window_size/2)), self.radius)

                    pygame.display.update()

                # get first player's move
                if player == human_player and event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.black,
                                     (0, 0, self.width, self.window_size))
                    posx = event.pos[0]
                    move = int(math.floor(posx/self.window_size))
                    if move in moves:
                        self.action(move)
                        self.draw_board()
                        if self.determine_winner():
                            if human_player == 1:
                                label = font.render(
                                    "Human wins", 1, self.blue)
                            else:
                                label = font.render(
                                    "Human wins", 1, self.blue)
                            self.screen.blit(label, (25, 25))
                            self.draw_board()
                            winner = True
                            break

                        player = -player

                # get second player's move
                elif player == -human_player:
                    move = rand.choice(moves)
                    if move in moves:
                        self.action(move)
                        self.draw_board()
                        if self.determine_winner():
                            if player == 1:
                                label = font.render(
                                    "Human loses", 1, self.red)
                            else:
                                label = font.render(
                                    "Human loses", 1, self.yellow)
                            self.screen.blit(label, (40, 10))
                            self.draw_board()
                            winner = True
                            break

                        player = -player
            moves = self.possible_moves()
        if winner == False and moves == []:
            label = font.render("Draw", 1, self.light_blue)
            self.screen.blit(label, (40, 10))
            self.draw_board()
        while exiting == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exiting = True
        pygame.quit()


def main():
    game = Connect4_GUI()
    game.run_game()


if __name__ == "__main__":
    main()
