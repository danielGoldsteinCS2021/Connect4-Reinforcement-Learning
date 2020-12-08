import pytest
import connect4_MCTS

'''
No need to view this file it just creates test cases. Included for clarity sake. 
'''

class TestConnect4:
    def setUp(self):
        self.game = connect4_MCTS.ConnectFour()

    def test_diag1(self):
        self.setUp()
        state = (('x'), ('o', 'x'), ('o', 'o', 'x'), ('o', 'o', 'o', 'x'), (), (), ())
        print(self.game.isGameOverDiag(state))

    def test_diag2(self):
        self.setUp()
        state = ((), (), (), ('o', 'o', 'o', 'x'), ('o', 'o', 'x'), ('o', 'x'), ('x'))
        print(self.game.isGameOverDiag(state))

    def test_diag3(self):
        self.setUp()
        state = (('o'),(),('o'),('o','o','x','x'),('x','o','x'),('x','x'),('x','o','o','x','o'))
        print(self.game.isGameOverDiag(state))

    def test_diag4(self):
        self.setUp()
        state = (('o'),('x','o'),('o','x','o'),('o','o','x','o'),('x','o','x'),('x','x'),('x','o'))
        print(self.game.isGameOverDiag(state))

    def test_photo1(self):
        self.setUp()
        state = ((), (), ('o'), ('o', 'x'), ('x', 'o'), ('x'), ('x', 'o'))
        print('Diag', self.game.isGameOverDiag(state))
        print('hor', self.game.isGameOverLeftRight(state))
        print('ver', self.game.isGameOverUpDown(state))

    def test_photo2(self):
        self.setUp()
        state = ((), (), ('x'), ('o', 'x', 'x'), ('o', 'x', 'o'), ('x', 'o', 'o'), ('x', 'x', 'o', 'o'))
        print('Diag', self.game.isGameOverDiag(state))
        print('hor', self.game.isGameOverLeftRight(state))
        print('ver', self.game.isGameOverUpDown(state))

    def test_photo3(self):
        self.setUp()
        state = ((), ('o'), (), ('o', 'x'), ('x'), ('x'), ('x', 'o'))
        print('Diag', self.game.isGameOverDiag(state))
        print('hor', self.game.isGameOverLeftRight(state))
        print('ver', self.game.isGameOverUpDown(state))

    def test_photo4(self):
        self.setUp()
        state = (('x', 'o', 'o'), ('o', 'x'), ('x'), ('o', 'x'), ('x', 'o'), ('x'), ('o'))
        print('Diag', self.game.isGameOverDiag(state))
        print('hor', self.game.isGameOverLeftRight(state))
        print('ver', self.game.isGameOverUpDown(state))


test = TestConnect4()
test.test_diag1()
test.test_diag2()
test.test_diag3()
test.test_diag4()
test.test_photo1()  # should not win
test.test_photo2()  # should not win
test.test_photo3()  # should not win
test.test_photo4()  # should not win
