import unittest

import app
from tower import *
from enemy import *
from constants import *
from bullets import *
from app import *
from board import *
from bar import *


class TestCases(unittest.TestCase):
    a = QtWidgets.QApplication(sys.argv)
    g = TowerDefense()
    a.installEventFilter(g)

    def test_mainBoardActive(self):
        self.assertIsNotNone(self.g.mainBoard)
        self.assertIsNotNone(self.g.toolsBar)

    def test_enemiesEmpty(self):
        self.assertTrue(len(enemies) == 0)


if __name__ == "__main__":
    unittest.main()