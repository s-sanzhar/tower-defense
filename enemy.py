from PyQt5 import QtCore, QtGui
from math import *
import constants


class Enemy:

    def __init__(self, ep=None):
        self.enemyPath = ep
        self.hp = 100
        self.speed = 2
        self.size = 4
        self.direction = "R"
        self.color = QtGui.QColor(25, 80, 100, 255)
        self.value = 10

        self.isFinished = False
        self.eliminated = False

        self.x_pos = self.enemyPath[0][0] * 20
        self.y_pos = self.enemyPath[0][1] * 20
        self.current_block = [self.enemyPath[0][0], self.enemyPath[0][1]]

    def move(self):
        temp = self.current_block
        self.current_block = self.get_cur_block()
        try:
            if temp != self.current_block:
                self.enemyPath.pop(0)
                if self.enemyPath[1] != self.get_ftr_block():
                    if self.get_cur_block()[1] < self.enemyPath[1][1]:
                        self.direction = "D"
                    elif self.get_cur_block()[1] > self.enemyPath[1][1]:
                        self.direction = "F"
                    elif self.get_cur_block()[0] < self.enemyPath[1][0]:
                        self.direction = "R"
                    elif self.get_cur_block()[0] > self.enemyPath[1][0]:
                        self.direction = "L"
        except:
            self.isFinished = True

        if self.direction == "R":
            self.x_pos += self.speed
        elif self.direction == "D":
            self.y_pos += self.speed
        elif self.direction == "L":
            self.x_pos -= self.speed
        elif self.direction == "F":
            self.y_pos -= self.speed

        self.hp_status()

    def hp_status(self):
        if self.hp <= 0:
            self.eliminated = True
            constants.budget += self.value

    def get_cur_block(self):

        if self.direction == "F":
            current_y = int(floor((self.y_pos + 20) / 20))
            if self.y_pos <= 0:
                current_y = 0
        else:
            current_y = int(floor(self.y_pos / 20))
            if current_y <= 0:
                current_y = 0
        if self.direction == "L":
            current_x = int(floor((self.x_pos + 20) / 20))
        else:
            current_x = int(floor(self.x_pos / 20))

        return [current_x, current_y]

    def get_ftr_block(self):
        if self.direction == "R":
            return [self.get_cur_block()[0] + 1, self.get_cur_block()[1]]
        elif self.direction == "L":
            return [self.get_cur_block()[0] - 1, self.get_cur_block()[1]]
        elif self.direction == "F":
            return [self.get_cur_block()[0], self.get_cur_block()[1] - 1]
        elif self.direction == "D":
            return [self.get_cur_block()[0], self.get_cur_block()[1] + 1]
        return None

    def get_center(self):
        return QtCore.QPoint(self.x_pos + 10, self.y_pos + 10)


class battleDroid(Enemy):
    def __init__(self, ep: None):
        super(battleDroid, self).__init__(ep)
        self.hp = 250
        self.speed = 2
        self.size = 8
        self.color = QtGui.QColor(112, 206, 208)
        self.value = 100


class tortureDroid(Enemy):

    def __init__(self, ep: None):
        super(tortureDroid, self).__init__(ep)
        self.hp = 50
        self.speed = 2
        self.color = QtGui.QColor(45, 80, 100, 255)
        self.value = 10