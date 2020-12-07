import pytest
import connect4_MCTS

class TestConnect4:
    def setUp(self):
        self.game = connect4_MCTS.ConnectFour()

    def test_diag1(self):
        self.setUp()
        state = (('x'), ('o', 'x'), ('o', 'o', 'x'), ('o', 'o', 'o', 'x'), (), (), ())
        print(self.game.pretty_state(state))
        print(self.game.isGameOverDiag(state))

    def test_diag2(self):
        self.setUp()
        state = ((), (), (), ('o', 'o', 'o', 'x'), ('o', 'o', 'x'), ('o', 'x'), ('x'))
        print(self.game.pretty_state(state))
        print(self.game.isGameOverDiag(state))

    def test_diag3(self):
        self.setUp()
        state = (('o'),(),('o'),('o','o','x','x'),('x','o','x'),('x','x'),('x','o','o','x','o'))
        print(self.game.pretty_state(state))
        print(self.game.isGameOverDiag(state))

    def test_diag4(self):
        self.setUp()
        state = (('o'),('x','o'),('o','x','o'),('o','o','x','o'),('x','o','x'),('x','x'),('x','o'))
        print(self.game.pretty_state(state))
        print(self.game.isGameOverDiag(state))

test = TestConnect4()
# test.test_diag1()
# test.test_diag2()
# test.test_diag3()
test.test_diag4()

# test = TestConnect4()
# game = connect4_MCTS.ConnectFour()
# state = (('o'),(),('o'),('o','o','x','x'),('x','o','x'),('x','x'),('x','o','o','x','o'))
# print(game.isGameOverDiag(state))
# game = connect4_MCTS.ConnectFour()
# state = (('o'),(),('o'),('o','o','x','x'),('x','o','x'),('x','x'),('x','o','o','x','o'))
# print(game.pretty_state(state))
# print(game.isGameOverDiag(state))
