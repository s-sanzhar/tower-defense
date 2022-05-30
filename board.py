import sys
import time
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from bar import *
from tower import *
from enemy import *
from bullets import *
from constants import *
import copy


class GameBoard(QtWidgets.QFrame):
    def __init__(self, parent):
        QtWidgets.QFrame.__init__(self, parent)

        self.mouse_x = -1
        self.mouse_y = -1
        self.isMouseIn = False
        self.isTowerSelected = False
        self.isTowerClicked = False
        self.lastPlacedTower = Tower()
        self.parent = parent
        self.isPaused = True

        self.waveCount = 1
        self.waveInProgress = False
        self.finalWave = False
        self.waveSent = False
        self.unitsSent = 0

    def wave_control(self):
        if constants.span:
            time.sleep(1)
            constants.span = False

        meta = open('waves.json')
        data = json.load(meta)

        id = data["wave " + str(self.waveCount)]["class"]
        units = data["wave " + str(self.waveCount)]["units"]
        span = data["wave " + str(self.waveCount)]["pause"]

        if self.waveSent == False and self.waveInProgress == False:
            if self.unitsSent == 0 or len(enemies) == 0:
                enemies.insert(0, getattr(sys.modules[__name__], id)
                (copy.deepcopy(enemyPath)))
                self.unitsSent += 1

            elif self.unitsSent < data["wave " + str(self.waveCount)]["units"]:
                if not len(enemies) == 0:
                     if enemies[0].x_pos >= span:
                         enemies.insert(0, getattr(sys.modules[__name__], id)
                         (copy.deepcopy(enemyPath)))
                         self.unitsSent += 1

                if self.unitsSent == units:
                    self.waveSent = False
                    self.waveInProgress = True
                    try:
                        id = data["wave " + str(self.waveCount + 1)]["class"]
                        self.waveCount += 1
                        self.unitsSent = 0
                    except:
                        self.finalWave = True
                        self.unitsSent = 0

        if self.waveInProgress and len(enemies) == 0:
            self.waveInProgress = False
            self.waveSent = False

        meta.close()

    def start(self):
        self.setStyleSheet("QWidget { background: #25B396 }")
        self.setFixedSize(boardWidth, boardHeight)
        #for enemy in enemyPath:
            #busy.append((enemy[0] * blockSize, enemy[1] * blockSize))

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if constants.crossLimit <= 0:
            self.game_over(qp)
        elif self.finalWave and len(enemies) == 0:
            self.game_won(qp)
        else:
            self.draw_path(qp)
            self.draw_grid(qp)
            self.draw_towers(qp)
            if self.isTowerSelected:
                self.draw_outline(qp)
            if self.isTowerClicked:
                self.select_tower(qp, self.lastPlacedTower)
            self.draw_bullets(qp)
            if not self.isPaused:
                self.wave_control()
            self.draw_enemies(qp)
            self.draw_hp_line(qp)
        qp.end()

    def draw_bullets(self, qp):
        constants.bullets = []
        i = 0
        for tower in towers:
            for target in tower.find_target(enemies):
                constants.bullets.append(Bullet(tower, target))
                qp.setPen(QtGui.QPen(constants.bullets[i].color, 3, QtCore.Qt.DotLine))
                qp.drawLine(tower.get_center(), target.get_center())
                i += 1

    def draw_path(self, qp):
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(25, 46, 91))
        for i in enemyPath:
            qp.drawRect(i[0] * blockSize, i[1] * blockSize, 20, 20)

    def draw_grid(self, qp):
        pen = QtGui.QPen(QtGui.QColor(25, 6, 12, 15), 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        for i in range(0, 600, blockSize):
            qp.drawLine(i, 0, i, boardHeight)
            qp.drawLine(0, i, boardWidth, i)

    def draw_towers(self, qp):
        for tower in towers:
            qp.setBrush(tower.color)
            qp.drawRect(tower.x_pos, tower.y_pos, tower.size * blockSize, tower.size * blockSize)

    def draw_outline(self, qp):
        if self.isMouseIn:
            qp.setPen(QtCore.Qt.NoPen)
            qp.setBrush(self.lastPlacedTower.color)
            qp.drawRect(self.round(self.get_x()), self.round(self.get_y()), self.lastPlacedTower.size * 20, self.lastPlacedTower.size * 20)
            qp.setBrush(QtGui.QColor(0, 0, 0, 55))
            center = QtCore.QPoint(self.round(self.get_x()) + (self.lastPlacedTower.size * 20 / 2), self.round(self.get_y()) + self.lastPlacedTower.size * 20 / 2)
            qp.drawEllipse(center, self.lastPlacedTower.range, self.lastPlacedTower.range)

        #if not self.check_placement() and self.isMouseIn:
            #qp.setPen(QtCore.Qt.NoPen)
            #qp.setBrush(QtGui.QColor(0, 0, 0, 155))
            #qp.drawRect(self.round(self.get_x()), self.round(self.get_y()), self.lastPlacedTower.size * 20, self.lastPlacedTower.size * 20)

    def draw_enemies(self, qp):
        qp.setPen((QtGui.QPen(QtGui.QColor(0, 0, 0), 1, QtCore.Qt.SolidLine)))
        for enemy in enemies:
            qp.setBrush(enemy.color)
            qp.drawEllipse(enemy.get_center(), enemy.size, enemy.size)
            if enemy.isFinished:
                constants.crossLimit -= 1
        enemies[:] = [i for i in enemies if i.isFinished == False]
        enemies[:] = [i for i in enemies if i.eliminated == False]

    def draw_hp_line(self, qp):
        qp.setPen(QtGui.QColor(0, 255, 0))
        for enemy in enemies:
            coord = QtCore.QPoint(enemy.x_pos, enemy.y_pos)
            x = coord.x()
            y = coord.y()
            qp.drawRect(x - 2, y - 5, enemy.hp / 10, 1)

    def get_x(self):
        if self.mouse_x > boardWidth - 40 and self.lastPlacedTower.size == 2:
            return boardWidth - 40
        return self.mouse_x

    def get_y(self):
        if self.mouse_y > boardHeight - 40 and self.lastPlacedTower.size == 2:
            return boardHeight - 40
        return self.mouse_y

    def round(self, x, div = 20):
        return x - (x % div)

    def update_mouse(self, x, y):
        self.mouse_x = x
        self.mouse_y = y
        self.repaint()

    def fire(self):
        for j in constants.bullets:
            j.shoot()

    def check_placement(self):
        if self.lastPlacedTower.size == 1:
            if [self.round(self.get_x()), self.round(self.get_y())] in busy:
                return False
        elif self.lastPlacedTower.size == 2:
            if [self.round(self.get_x()), self.round(self.get_y())] in busy or \
                [self.round(self.get_x()), self.round(self.get_y()) + blockSize] in busy or \
                [self.round(self.get_x()) + blockSize, self.round(self.get_y())] in busy or \
                [self.round(self.get_x()) + blockSize, self.round(self.get_y()) + blockSize] in busy:
                return False
        return True

    def place_towers(self):
        if self.check_placement() and self.isTowerSelected:
            self.lastPlacedTower.x_pos = self.round(self.get_x())
            self.lastPlacedTower.y_pos = self.round(self.get_y())
            if self.isMouseIn and constants.budget >= self.lastPlacedTower.cost:
                towers.append(self.lastPlacedTower)
                self.isTowerSelected = False
                self.isTowerClicked = True
                constants.budget -= self.lastPlacedTower.cost

                if self.lastPlacedTower.size == 1:
                    busy.append([self.round(self.get_x()), self.round(self.get_y())])
                    self.lastPlacedTower.occupied.append([self.round(self.get_x()), self.round(self.get_y())])

                elif self.lastPlacedTower.size == 2:
                    busy.append([self.round(self.get_x()), self.round(self.get_y())])
                    busy.append([self.round(self.get_x()) + blockSize, self.round(self.get_y())])
                    busy.append([self.round(self.get_x()), self.round(self.get_y()) + blockSize])
                    busy.append([self.round(self.get_x()) + blockSize, self.round(self.get_y()) + blockSize])
                    self.lastPlacedTower.occupied.append([self.round(self.get_x()), self.round(self.get_y())])
                    self.lastPlacedTower.occupied.append([self.round(self.get_x()) + blockSize, self.round(self.get_y())])
                    self.lastPlacedTower.occupied.append([self.round(self.get_x()), self.round(self.get_y()) + blockSize])
                    self.lastPlacedTower.occupied.append([self.round(self.get_x()) + blockSize, self.round(self.get_y()) + blockSize])
            else:
                self.lastPlacedTower = Tower()
                self.isTowerSelected = False
        elif self.isMouseIn:
            print("WTF2")
            for tower in towers:
                if [self.round(self.get_x()), self.round(self.get_y())] in tower.get_occupied():
                    print("WTF1")
                    self.lastPlacedTower = tower
                    self.isTowerSelected = False
                    self.isTowerClicked = True
                    break
                else:
                    print("WTF3")
                    self.isTowerClicked = False
        self.repaint()

    def select_tower(self, qp, tower):
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(0, 0, 0, 55))
        qp.drawEllipse(tower.get_center(), tower.range, tower.range)

    def wave(self):
        for enemy in enemies:
            enemy.move()

    def clear_data(self):
        for i in range(len(enemies)):
            enemies.pop()
        for i in range(len(towers)):
            towers.pop()
        for i in range(len(busy)):
            busy.pop()

    def print_result(self, qp, res):
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setFont(QtGui.QFont('Courier', 50))
        qp.drawText(140, 150, res)

    def game_over(self, qp):
        self.clear_data()
        self.parent.timer.stop()
        constants.over = True
        self.print_result(qp, "GAME OVER")

    def game_won(self, qp):
        self.clear_data()
        self.parent.timer.stop()
        self.print_result(qp, "YOU WON!")
