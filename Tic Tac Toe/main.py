# importing required libraries
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QMainWindow, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt
# 1 for human, 2 for computer move

import sys


# create a Window class 
class Window(QMainWindow):
    # constructor
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(550, 200, 550, 650)
        self.setStyleSheet("background-color: papayawhip;")
        self.Ui()
        self.show()

    # method for components
    def Ui(self):
        self.turn = 0
        self.board = []
        for _ in range(3):
            temp = []
            for _ in range(3):
                temp.append((QPushButton(self)))
            self.board.append(temp)

        for i in range(3):
            for j in range(3):
                self.board[i][j].setGeometry(50 + (i % 3) * 150, 130 + (j % 3) * 150, 140, 140)
                self.board[i][j].setIcon(QIcon('Images/empty.png'))
                self.board[i][j].setIconSize(QSize(100, 100))
                self.board[i][j].setStyleSheet("background-color:rgba(255, 255, 255, 0)")
                self.board[i][j].move = 0
                self.board[i][j].clicked.connect(self.acti)

        shadow = QGraphicsDropShadowEffect()
        shadow1 = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(3)
        shadow1.setBlurRadius(100)
        self.labe = QLabel(self)
        self.labe.setText("")
        self.labe.setFont(QFont('Courier', 20))
        self.labe.setGeometry(170, 30, 200, 50)
        self.labe.setGraphicsEffect(shadow)
        self.labe.setStyleSheet("""
        QLabel {
            color: white;
            background-color: indianred;
            }
        """)
        self.labe.setAlignment(Qt.AlignCenter)
        reset_game = QPushButton("", self)
        reset_game.setGeometry(170, 585, 200, 50)
        reset_game.setStyleSheet("background-color:rgba(255, 255, 255, 0)")
        reset_game.setGraphicsEffect(shadow1)
        reset_game.setIcon(QIcon('Images/restart.png'))
        reset_game.setIconSize(QSize(200, 50))
        reset_game.clicked.connect(self.reset_game_action)
        self.change_turn = QPushButton("", self)
        self.change_turn.setGeometry(430, 580, 70, 70)
        self.change_turn.setStyleSheet("background-color:rgba(255, 255, 255, 0)")
        self.change_turn.setIcon(QIcon('Images/rotate.png'))
        self.change_turn.setIconSize(QSize(70, 70))
        self.change_turn.clicked.connect(self.changeturn)
        self.order = 0

    def check(self):
        v = 0
        # check cross
        for i in range(3):
            if self.board[0][i].move == self.board[1][i].move and self.board[1][i].move == self.board[2][i].move and \
                    self.board[1][i].move > 0:
                v = self.board[1][i].move
        # check column
        for i in range(3):
            if self.board[i][0].move == self.board[i][1].move and self.board[i][1].move == self.board[i][2].move and \
                    self.board[i][1].move > 0:
                v = self.board[i][1].move
        # check diagonal
        if self.board[0][0].move == self.board[1][1].move and self.board[1][1].move == self.board[2][2].move and \
                self.board[1][1].move > 0:
            v = self.board[0][0].move
        if self.board[0][2].move == self.board[1][1].move and self.board[1][1].move == self.board[2][0].move and \
                self.board[1][1].move > 0:
            v = self.board[0][2].move
        if v > 0:
            return v
        # check full
        full = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j].move == 0:
                    full = 1
        if full == 0:
            return -1
        if full == 1:
            return 0

    def changeturn(self):
        if self.order == 0:
            self.order = 1
        else:
            self.order = 0

    def reset_game_action(self):
        self.turn = 0
        self.labe.setText("")
        for buttons in self.board:
            for button in buttons:
                button.move = 0
                button.setEnabled(True)
                button.setIcon(QIcon('Images/empty.png'))
                button.setIconSize(QSize(100, 100))
                button.setStyleSheet("background-color:rgba(255, 255, 255, 0)")
        if self.order == 1: self.acti()

    def miniMax(self, bstate, isMaximizing):
        result = self.check()
        if result == -1: return 0
        if result == 1: return -1
        if result == 2: return 1
        if isMaximizing:
            bestScore = -100
            for row in range(3):
                for column in range(3):
                    if self.board[row][column].move == 0:
                        self.board[row][column].move = 2
                        score = self.miniMax(self.board, False)
                        self.board[row][column].move = 0
                        if score > bestScore: bestScore = score
                        if bestScore == 1: break
                if bestScore == 1: break
            return bestScore
        else:
            bestScore = 100
            for row in range(3):
                for column in range(3):
                    if (self.board[row][column].move == 0):
                        self.board[row][column].move = 1
                        score = self.miniMax(self.board, True)
                        self.board[row][column].move = 0
                        if score < bestScore: bestScore = score
                        if bestScore == -1: break
                if bestScore == -1: break
            return bestScore

    def bestMove(self):
        bestScore = -100
        for row in range(3):
            for column in range(3):
                if (self.board[row][column].move == 0):
                    self.board[row][column].move = 2
                    score = self.miniMax(self.board, False)
                    self.board[row][column].move = 0
                    if (score > bestScore):
                        bestScore = score
                        bestrow = row
                        bestcolumn = column
        self.board[bestrow][bestcolumn].move = 2
        self.board[bestrow][bestcolumn].setEnabled(False)
        self.board[bestrow][bestcolumn].setIcon(QIcon('Images/o.png'))

    def acti(self):
        if self.turn % 2 == self.order and self.turn != 9:
            button = self.sender()
            button.setEnabled(False)
            button.setIcon(QIcon('Images/x.png'))
            button.move = 1
            self.turn += 1
        if self.turn != 9 and self.turn % 2 != self.order:
            self.bestMove()
            self.turn += 1
        p = "Checking..."
        result = self.check()
        if result == 1:
            p = "Human Won"
        if result == 2:
            p = "Computer Won"
        if result == -1:
            p = "Draw"
        if result != 0:
            for buttons in self.board:
                for push in buttons:
                    push.setEnabled(False)
        self.labe.setText(p)


# create pyqt5 app
app = QApplication(sys.argv)

# create the instance of our Window 
window = Window()

# start the app 
sys.exit(app.exec_())
