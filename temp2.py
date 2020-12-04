import sys
import connect4_MCTS


def play(human=True, n=10000):
    # Testing ConnectFour - mcts_uct()
    width = 7
    initial = ((),) * width

    game = connect4_MCTS.ConnectFour()
    state = initial
    player = game.player1
    computer = game.player2

    while not game.isTerminalState(state):
        print(game.pretty_state(state, False))
        if True:
            prompt = 'Choose a move, choices are %s: ' % (game.actions(state),)
            success = False
            while not success:
                choice = input(prompt)
                try:
                    action = int(choice)
                    state = game.resultingState(state, action, player)
                    success = True
                except ValueError:
                    pass
                except Exception:
                    pass
        else:
            action = connect4_MCTS.monteCarloTreeSearch(game, state, player)
            state = game.resultingState(state, action, player)

        print()
        print('Player 1 chose ', action)
        print(game.pretty_state(state, False))

        # Intermediate win check
        if game.isTerminalState(state):
            break

        # Computer plays now
        action = connect4_MCTS.monteCarloTreeSearch(game, state, computer)
        state = game.resultingState(state, action, computer)

        print('Player 2 chose %s' % action)

    print(game.pretty_state(state, False))
    print()
    outcome = game.gameOutcome(state, player)
    if outcome == 1:
        print('Player 1 wins.')
    elif outcome == -1:
        print('Player 2 wins.')
    else:
        print('Tie game.')


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

print('Number of Sample Iterations: ' + str(n))
print('Human Player: ' + str(human))
print()
play(n=n, human=human)