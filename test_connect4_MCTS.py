import pytest
import connect4_MCTS

class TestConnect4:
    def setUp(self):
        self.game = connect4_MCTS.ConnectFour()

    def test_diag1(self):
        self.setUp()
        state = (('x'), ('o', 'x'), ('o', 'o', 'x'), ('o', 'o', 'o', 'x'), (), (), ())
        assert(self.game.isGameOverDiag(state))

    def test_diag2(self):
        self.setUp()
        state = ((), (), (), ('o', 'o', 'o', 'x'), ('o', 'o', 'x'), ('o', 'x'), ('x'))
        assert(self.game.isGameOverDiag(state))
