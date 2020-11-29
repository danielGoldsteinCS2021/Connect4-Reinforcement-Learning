import numpy as np
import random

rand = random.Random()


class Connect4():
    row_count = 6
    col_count = 7
    win_count = 4

    def __init__(self):
        self.board = np.zeros((self.row_count, self.col_count))

    def __str__(self):
        str_board = "\n\n" + str(self.board).replace("0.",
                                                     "_").replace("-1.", " O").replace("1.", "X")
        str_board = str_board.replace("[", " ").replace("]", " ")
        return str_board

    def possible_moves(self):
        # check top row for empty
        return [m for m in range(self.col_count) if self.board[0][m] == 0]

    def action(self, move):
        if np.sum(self.board) == 0:
            player = 1
        else:
            player = -1

        j = 0
        while j+1 < self.row_count and self.board[j+1][move] == 0:
            j += 1

        self.board[j][move] = player

    def determine_winner(self):
        for i in range(self.row_count-self.win_count+1):
            for j in range(self.col_count-self.win_count+1):
                subboard = self.board[i:i+self.win_count, j:j+self.win_count]
                if np.max(np.abs(np.sum(subboard, 0))) == self.win_count:
                    return True
                if np.max(np.abs(np.sum(subboard, 1))) == self.win_count:
                    return True
                # Diagonal win
                elif np.abs(sum([subboard[k, k] for k in range(self.win_count)])) == self.win_count:
                    return True
                elif np.abs(sum([subboard[k, self.win_count-1-k] for k in range(self.win_count)])) == self.win_count:  # opp diag
                    return True
        return False


def main():
    players = {-1: "O", 0: "Nobody", 1: "X"}
    game = Connect4()
    moves = game.possible_moves()
    print(game)
    player = 1  # first player is alway 1
    human_player = rand.choice([1, -1])
    while moves != []:

        if player == human_player:
            print(f"Available moves are: {moves}")
            move = int(input("Enter move: "))
        else:
            move = rand.choice(moves)
        game.action(move)
        print(game)
        # Determine if a player has one and print win message accordingly
        winner = game.determine_winner()
        if winner:
            print(f"{players[player]} Wins")
            break
        moves = game.possible_moves()  # reset possible moves
        player = -player  # change players


if __name__ == "__main__":
    main()
