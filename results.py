import connect4_MCTS
from random import choice
import matplotlib.pyplot as plt

'''
This file just creates the graphs already shown in the report. There isn't much need to view it.
'''


def play(n=100):
    initial = ((),) * 7
    game = connect4_MCTS.ConnectFour()
    state = initial
    player = game.player1
    computer = game.player2

    while not game.isTerminalState(state):
        action = choice(game.actions(state))  # choose random action
        state = game.resultingState(state, action, player)

        # win check
        if game.isTerminalState(state):
            break

        # Computer turn now
        action = connect4_MCTS.monteCarloTreeSearch(game, state, computer, n)
        state = game.resultingState(state, action, computer)

    outcome = game.gameOutcome(state, player)
    if outcome == 1:
        return True
    elif outcome == -1:
        return False
    else:
        return None


print('100 games against AI, with 25 iterations for MCTS algorithm')
p1_win, p2_win, draw = 0, 0, 0
for _ in range(100):
    winner = play(25)
    if winner is None:
        draw += 1
    if winner:
        p1_win += 1
    else:
        p2_win += 1
print("For 100 games at 25 iterations")
print("Random wins: ", p1_win)
print("Computer wins: ", p2_win)
print("Draws: ", draw)

print('100 games against AI, with 50 iterations for MCTS algorithm')
p1_win, p2_win, draw = 0, 0, 0
for _ in range(100):
    winner = play(50)
    if winner is None:
        draw += 1
    if winner:
        p1_win += 1
    else:
        p2_win += 1
print("For 100 games at 50 iterations")
print("Random wins: ", p1_win)
print("Computer wins: ", p2_win)
print("Draws: ", draw)

print('100 games against AI, with 100 iterations for MCTS algorithm')
p1_win, p2_win, draw = 0, 0, 0
for _ in range(100):
    winner = play(100)
    if winner is None:
        draw += 1
    if winner:
        p1_win += 1
    else:
        p2_win += 1
print("For 100 games at 100 iterations")
print("Random wins: ", p1_win)
print("Computer wins: ", p2_win)
print("Draws: ", draw)

print('100 games against AI, with 200 iterations for MCTS algorithm')
p1_win, p2_win, draw = 0, 0, 0
for _ in range(100):
    winner = play(200, )
    if winner is None:
        draw += 1
    if winner:
        p1_win += 1
    else:
        p2_win += 1
print("For 100 games at 200 iterations")
print("Random wins: ", p1_win)
print("Computer wins: ", p2_win)
print("Draws: ", draw)

# MATPLOTLIB ----------------------------------------------
winsPerIterationComputer = [0 for _ in range(10)]
winsPerIterationPlayer = [0 for _ in range(10)]
iterationIncreases20 = [i for i in range(20, 220, 20)]  # [10.....200]

for e, i in enumerate(iterationIncreases20):  # iterations for MCTS per set of 20 games
    p1_wins, p2_wins = 0, 0
    for _ in range(20):  # number of games to play
        result = play(i)
        if result is None:
            continue
        if result:
            p1_wins += 1
        if not result:
            p2_wins += 1
    winsPerIterationPlayer[e] = p1_wins
    winsPerIterationComputer[e] = p2_wins
    print('wP1: ', winsPerIterationPlayer)
    print('wP2: ', winsPerIterationComputer)

plt.title("Agent wins per 20 games. \nMCTS iterations 20 to 200, increases of 20")
plt.plot(iterationIncreases20, [14, 13, 18, 16, 13, 14, 11, 11, 10, 11])  # array is winsPerIterationPlayer
plt.ylabel('Number of wins')
plt.xlabel('MCTS iterations')
plt.show()

plt.title("Random action wins per 20 games. \nMCTS iterations 20 to 200, increases of 20")
plt.plot(iterationIncreases20, [6, 7, 2, 4, 7, 6, 9, 8, 9, 8])  # array is winsPerIterationComputer
plt.ylabel('Number of wins')
plt.xlabel('MCTS iterations')
plt.show()

winsPerIterationComputer2 = [0 for _ in range(190)]
winsPerIterationPlayer2 = [0 for _ in range(190)]
x = len(winsPerIterationPlayer2)

p1_wins, p2_wins = 0, 0
for i in range(10, x + 10):
    result = play(i)
    if result is None:
        winsPerIterationComputer2[i - 10] = p2_wins
        winsPerIterationPlayer2[i - 10] = p1_wins
        continue
    if result:
        p1_wins += 1
    else:
        p2_wins += 1
    winsPerIterationComputer2[i - 10] = p2_wins
    winsPerIterationPlayer2[i - 10] = p1_wins
    print('Random: ', winsPerIterationPlayer2)
    print('Agent: ', winsPerIterationComputer2)

winsPerIterationPlayer2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
                           6, 7, 8, 9, 9, 9, 9, 9, 10, 10, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 15, 15, 16, 16,
                           17, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 21, 22, 23, 24, 24, 25, 26, 27,
                           28, 28, 28, 29, 29, 30, 31, 31, 32, 32, 32, 32, 32, 33, 34, 34, 34, 34, 34, 35, 35, 35, 36,
                           36, 37, 37, 37, 37, 37, 37, 37, 37, 38, 39, 40, 40, 41, 41, 41, 41, 41, 41, 41, 41, 42, 42,
                           43, 43, 43, 43, 43, 44, 45, 45, 45, 45, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 47, 47, 48,
                           48, 48, 48, 48, 48, 49, 49, 49, 49, 49, 49, 49, 49, 50, 50, 50, 51, 52, 52, 52, 52, 53, 53,
                           53, 53, 54, 55, 55, 55, 56, 57, 57, 58, 59, 59, 59, 59, 59, 59, 59, 59, 60]
winsPerIterationComputer2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 9, 10, 10, 11, 11, 12, 12, 13, 14, 15, 16, 17, 18, 19,
                             20, 21, 22, 23, 24, 25, 26, 26, 26, 26, 27, 28, 29, 30, 30, 31, 31, 31, 32, 33, 34, 34,
                             35, 36, 37, 37, 38, 38, 39, 39, 40, 40, 40, 41, 42, 42, 43, 44, 45, 46, 47, 48, 48, 49,
                             50, 51, 51, 51, 51, 51, 52, 52, 52, 52, 52, 53, 54, 54, 55, 55, 55, 56, 56, 57, 58, 59,
                             60, 60, 60, 61, 62, 63, 64, 64, 65, 66, 66, 67, 67, 68, 69, 69, 70, 71, 72, 73, 73, 73,
                             73, 74, 74, 75, 76, 77, 78, 78, 79, 80, 80, 81, 81, 82, 83, 84, 85, 85, 85, 86, 87, 88,
                             88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 97, 98, 98, 99, 100, 101, 102, 103, 103, 104,
                             105, 106, 107, 108, 109, 110, 110, 111, 112, 112, 112, 113, 114, 115, 115, 116, 117,
                             118, 118, 118, 119, 120, 120, 120, 121, 121, 121, 122, 123, 124, 125, 126, 127, 128, 128]

plt.title("Total agent wins as iterations increase.\n Iterations: 10 - 200, increases by 1")
plt.plot([i for i in range(10, 200)], winsPerIterationComputer2)
plt.ylabel('Number of wins')
plt.xlabel('Number of iterations for MCTS')
plt.show()

plt.title("Total random action wins as iterations increase.\n  Iterations: 10 - 200, increases by 1")
plt.plot([i for i in range(10, 200)], winsPerIterationPlayer2)
plt.ylabel('Number of wins')
plt.xlabel('Number of iterations for MCTS')
plt.show()

winsPerIterationComputer3 = [0 for _ in range(30)]
winsPerIterationPlayer3 = [0 for _ in range(30)]
iterationIncreases3 = [i for i in range(30, 61)]
for e, i in enumerate(iterationIncreases3):
    p1_wins, p2_wins = 0, 0
    for _ in range(100):
        result = play(i)
        if result is None:
            continue
        if result:
            p1_wins += 1
        if not result:
            p2_wins += 1
    winsPerIterationPlayer3[e] = p1_wins
    winsPerIterationComputer3[e] = p2_wins
    print('wP1: ', winsPerIterationPlayer3)
    print('wP2: ', winsPerIterationComputer3)

winsPerIterationPlayer3 = [22, 30, 24, 17, 21, 20, 26, 20, 28, 20, 23, 24, 30, 32, 26, 19, 21, 29, 24, 21, 23, 30, 23,
                           30, 27, 32, 25, 31, 28, 32]
winsPerIterationComputer3 = [78, 70, 76, 83, 79, 80, 74, 80, 72, 80, 77, 76, 70, 68, 74, 81, 79, 71, 76, 79, 76, 70, 77,
                             69, 73, 67, 75, 69, 72, 68]
plt.title("Total agent wins for 100 games\n MCTS iterations: 30 - 60, increases by 1")
plt.plot([i for i in range(30, 60)], winsPerIterationComputer3)
plt.ylabel('Number of wins per 100 games')
plt.xlabel('Number of iterations for MCTS')
plt.show()

plt.title("Total player wins for 100 games.\n MCTS iterations: 30 - 60, increases by 1")
plt.plot([i for i in range(30, 60)], winsPerIterationPlayer3)
plt.ylabel('Number of wins per 100 games')
plt.xlabel('Number of iterations for MCTS')
plt.show()
