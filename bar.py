from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from constants import *
from board import *
from tower import *
from enemy import *


class toolsBar(QtWidgets.QFrame):

    def __init__(self, parent):
        QtWidgets.QFrame.__init__(self, parent)
        self.mainBoard = parent.mainBoard

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.show_game_stats(qp)
        self.show_tower_info(qp)
        qp.end()

    def start(self):
        self.setStyleSheet("QWidget { background: #70CED0 }")
        self.setGeometry(400, 0, 100, 295)

        towerBtns = []
        for i in range(0, 3):
            btn = QtWidgets.QPushButton(self)
            btn.move(20, btnDistance * (i + 2))
            btn.setIconSize(QtCore.QSize(50, 30))
            img_url = 'Images\droid' + str(i + 1) + '.png'
            btn.setIcon(QtGui.QIcon(img_url))
            towerBtns.append(btn)

        towerBtns[0].clicked.connect(self.tower_one)
        towerBtns[1].clicked.connect(self.tower_two)
        towerBtns[2].clicked.connect(self.tower_three)


    def tower_selected(self):
        self.mainBoard.isTowerSelected = True
        self.mainBoard.isTowerClicked = False

    def tower_one(self):
        self.tower_selected()
        self.mainBoard.lastPlacedTower = R2X2()

    def tower_two(self):
        self.tower_selected()
        self.mainBoard.lastPlacedTower = BB8()

    def tower_three(self):
        self.tower_selected()
        self.mainBoard.lastPlacedTower = R2D2()

    def show_tower_info(self, qp):
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(0, 0, 0, 0))
        qp.drawRect(0, 35, 100, 195)
        qp.drawRect(0, 210, 100, 95)
        qp.setPen(QtGui.QColor(0, 34, 3))
        qp.setFont(QtGui.QFont('Courier', 12, weight=QtGui.QFont.Bold))
        qp.drawText(25, 225, "STATS")
        if self.mainBoard.isTowerClicked or self.mainBoard.isTowerSelected:

            qp.setFont(QtGui.QFont('Courier', 10, weight=QtGui.QFont.Cursive))
            qp.drawText(5, 245, "Damage: "   + str(self.mainBoard.lastPlacedTower.damage))
            qp.drawText(5, 260, "Range:  "    + str(self.mainBoard.lastPlacedTower.range))
            qp.drawText(5, 275, "RoF:    "      + str(self.mainBoard.lastPlacedTower.rof))
            qp.drawText(5, 290, "Cost:   "     + str(self.mainBoard.lastPlacedTower.cost))

    def show_game_stats(self, qp):

        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(0, 0, 0, 0))
        r1 = QtCore.QRect(0, 0, 35 , 35)
        r2 = QtCore.QRect(0, 0, 100, 35)
        r3 = QtCore.QRect(0, 35, 35, 35)
        r4 = QtCore.QRect(35, 35, 100, 35)

        qp.drawRect(r1)
        qp.drawRect(r2)
        qp.drawRect(r3)
        qp.drawRect(r4)

        qp.setPen(QtGui.QColor(0, 34, 3))
        qp.setFont(QtGui.QFont('Cursive', 14))

        qp.drawImage(r1, QtGui.QImage("Images\coin.png").scaled(35, 35, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation))
        qp.drawText(50, 25, str(constants.budget))
        qp.drawImage(r3, QtGui.QImage("Images\lives.png").scaled(35, 35, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation))
        qp.drawText(60, 60, str(constants.crossLimit))
