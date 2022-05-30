from board import *
from bar import *
from PyQt5 import QtWidgets, QtCore


class TowerDefense(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.width = 500
        self.height = 295
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Tower Defense by Sanzhar")

        self.mainBoard = GameBoard(self)
        self.setCentralWidget(self.mainBoard)
        self.toolsBar = toolsBar(self)

        self.mainBoard.start()
        self.toolsBar.start()

        self.timer = QtCore.QBasicTimer()
        self.timer.start(50, self)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_P:
            self.mainBoard.pause()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if len(towers) > 0:
                self.mainBoard.isPaused = False
            self.mainBoard.wave()
            self.mainBoard.fire()
            self.repaint()
        else:
            QtWidgets.QFrame.timerEvent(self, event)

    def mousePressEvent(self, event):
        self.mainBoard.place_towers()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton and str(source).find("GameBoard") > 0:
                pos = event.pos()
                self.mainBoard.update_mouse(pos.x(), pos.y())
                self.mainBoard.isMouseIn = True
            else:
                self.mainBoard.isMouseIn = False
                self.mainBoard.repaint()
        return QtWidgets.QMainWindow.eventFilter(self, source, event)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    game = TowerDefense()
    game.show()
    app.installEventFilter(game)
    sys.exit(app.exec_())
