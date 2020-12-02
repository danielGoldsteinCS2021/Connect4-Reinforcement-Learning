import sys
import connect4_daniel


def play(human=True, n=1000):
    # Testing ConnectFour - mcts_uct()
    height = 6
    width = 7
    target = 4
    initial = ((),) * width

    game = connect4_daniel.ConnectFour(height=height, width=width, target=target)
    state = initial
    player = game.players[0]
    computer = game.players[1]

    while not game.terminal(state):
        print(game.pretty_state(state, False))
        if human:
            prompt = 'Choose a move, choices are %s: ' % (game.actions(state),)
            success = False
            while not success:
                choice = input(prompt)
                try:
                    action = int(choice)
                    state = game.result(state, action, player)
                    success = True
                except ValueError:
                    pass
                except Exception:
                    pass
        else:
            action = connect4_daniel.mcts_uct(game, state, player, n)
            state = game.result(state, action, player)

        print()
        print('Player 1 chose ', action)
        print(game.pretty_state(state, False))

        # Intermediate win check
        if game.terminal(state):
            break

        # Computer plays now
        action = connect4_daniel.mcts_uct(game, state, computer, n)
        state = game.result(state, action, computer)

        print('Player 2 chose %s' % action)

    print(game.pretty_state(state, False))
    print()
    outcome = game.outcome(state, player)
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