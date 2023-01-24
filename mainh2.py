from PyQt5 import QtCore, QtGui, QtWidgets
import functools
import sys
from math import inf as infinity
from random import choice
import time


HUMAN = -1
COMP = +1

board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
# h_choice = 'X'  # X or O
# c_choice = 'O'  # X or O
# first = 'Y'  # if human is the first

def possible_wins(state,player):

    win_state = [
        [state[0][0], state[0][1], state[0][2]], # row 1
        [state[1][0], state[1][1], state[1][2]], # row 2
        [state[2][0], state[2][1], state[2][2]], # row 3
        [state[0][0], state[1][0], state[2][0]], # col 1
        [state[0][1], state[1][1], state[2][1]], # col 2
        [state[0][2], state[1][2], state[2][2]], # col 3
        [state[0][0], state[1][1], state[2][2]], # primary digonal
        [state[2][0], state[1][1], state[0][2]], # secondary digonal
    ]
    return int([player, 1, 1] in win_state) + int([1, player, 1] in win_state) + int([1, 1, player] in win_state) + int([1, player, player] in win_state) + int([player, 1, player] in win_state) + int([player, player, 1] in win_state)

def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    score = possible_wins(state,HUMAN) - possible_wins(state,COMP)

    return score


def wins(state, player):
    """
    This function tests if a specific player wins. Possibilities:
    * Here, we have eight total possiblities to win a match. 
    - 3 rows      [X X X] or [O O O]
    - 3 cols      [X X X] or [O O O]
    - 2 diagonals [X X X] or [O O O]

    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]], # row 1
        [state[1][0], state[1][1], state[1][2]], # row 2
        [state[2][0], state[2][1], state[2][2]], # row 3
        [state[0][0], state[1][0], state[2][0]], # col 1
        [state[0][1], state[1][1], state[2][1]], # col 2
        [state[0][2], state[1][2], state[2][2]], # col 3
        [state[0][0], state[1][1], state[2][2]], # primary digonal
        [state[2][0], state[1][1], state[0][2]], # secondary digonal
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False
def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)

def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells

def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value
    return best


class Ui_TicTacToe(object):
    def setupUi(self, TicTacToe):
        self.xImage= "img/playerx.png"
        self.oImage= "img/playero.png"
        TicTacToe.setObjectName("TicTacToe")
        TicTacToe.resize(500, 500)
        TicTacToe.setMinimumSize(QtCore.QSize(500, 500))
        TicTacToe.setMaximumSize(QtCore.QSize(500, 500))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        TicTacToe.setPalette(palette)
        TicTacToe.setAcceptDrops(True)
        TicTacToe.setStyleSheet("background : rgb(2,10,35)")
        self.centralwidget = QtWidgets.QWidget(TicTacToe)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, -10, 421, 421))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(233, 196, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 196, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 196, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 196, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 196, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 196, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 196, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 196, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 196, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(38, 70, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.label.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setStyleSheet("color : #e9c46a")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("img/board.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setGeometry(QtCore.QRect(100, 30, 81, 81))
        self.label_0.setStyleSheet("background : none")
        self.label_0.setText("")
        self.label_0.setScaledContents(True)
        self.label_0.setObjectName("label_0")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(200, 30, 81, 81))
        self.label_1.setStyleSheet("background : none")
        self.label_1.setText("")
        self.label_1.setScaledContents(True)
        self.label_1.setObjectName("label_1")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 130, 81, 81))
        self.label_4.setStyleSheet("background : none")
        self.label_4.setText("")
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(200, 230, 81, 81))
        self.label_7.setStyleSheet("background : none")
        self.label_7.setText("")
        #self.label_7.setPixmap(QtGui.QPixmap(self.xImage))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(100, 130, 81, 81))
        self.label_3.setStyleSheet("background : none")
        self.label_3.setText("")
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(100, 230, 81, 81))
        self.label_6.setStyleSheet("background : none")
        self.label_6.setText("")
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(290, 30, 81, 81))
        self.label_2.setStyleSheet("background : none")
        self.label_2.setText("")
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(290, 130, 81, 81))
        self.label_5.setStyleSheet("background : none")
        self.label_5.setText("")
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(290, 230, 81, 81))
        self.label_8.setStyleSheet("background : none")
        self.label_8.setText("")
        # self.label_8.setPixmap(QtGui.QPixmap(self.oImage))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.notification = QtWidgets.QLabel(self.centralwidget)
        self.notification.setGeometry(QtCore.QRect(130, 350, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(30)
        self.notification.setFont(font)
        self.notification.setStyleSheet("color : #f4a261")
        self.notification.setObjectName("notification")
        self.notification.setAlignment(QtCore.Qt.AlignCenter)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 410, 251, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("border : none; background : #2a9d8f; color : #e9c46a; font-weight : bold; border-radius:6px")
        self.pushButton.setObjectName("newGame")
        TicTacToe.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TicTacToe)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        TicTacToe.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TicTacToe)
        self.statusbar.setObjectName("statusbar")
        TicTacToe.setStatusBar(self.statusbar)
        self.NewGame = QtWidgets.QAction(TicTacToe)
        self.NewGame.setCheckable(False)
        self.NewGame.setChecked(False)
        icon = QtGui.QIcon.fromTheme("background:red")
        self.NewGame.setIcon(icon)
        self.NewGame.setObjectName("NewGame")

        self.pushButton.clicked.connect(self.newGame)

        self.retranslateUi(TicTacToe)
        QtCore.QMetaObject.connectSlotsByName(TicTacToe)
        self.emptySpace = 9 #To Check for draws
        self.gameStatePause = False
        self.label_0.mousePressEvent = functools.partial(self.playerMove, source_object = self.label_0, square = (0,0))
        self.label_1.mousePressEvent = functools.partial(self.playerMove, source_object = self.label_1, square = (0,1))
        self.label_2.mousePressEvent = functools.partial(self.playerMove, source_object = self.label_2, square = (0,2))
        self.label_3.mousePressEvent = functools.partial(self.playerMove, source_object = self.label_3, square = (1,0))
        self.label_4.mousePressEvent = functools.partial(self.playerMove, source_object = self.label_4, square = (1,1))
        self.label_5.mousePressEvent = functools.partial(self.playerMove, source_object = self.label_5, square = (1,2))
        self.label_6.mousePressEvent = functools.partial(self.playerMove, source_object = self.label_6, square = (2,0))
        self.label_7.mousePressEvent = functools.partial(self.playerMove, source_object = self.label_7, square = (2,1))
        self.label_8.mousePressEvent = functools.partial(self.playerMove, source_object = self.label_8, square = (2,2))

    def retranslateUi(self, TicTacToe):
        _translate = QtCore.QCoreApplication.translate
        TicTacToe.setWindowTitle("TicTacToe - MinMax Algo")
        self.notification.setText(_translate("TicTacToe", ""))
        self.pushButton.setText(_translate("TicTacToe", "Nouveau Jeu"))
        self.NewGame.setText(_translate("TicTacToe", "Nouveau Jeu"))
    
    def playerMove(self, event, source_object, square):
        x,y = square
        if board[x][y] != 0 or self.gameStatePause:
            return
        board[x][y] = HUMAN
        source_object.setPixmap(QtGui.QPixmap(self.oImage))
        self.emptySpace -= 1
        if self.emptySpace == 0:
            self.gameStatePause = True
            self.notification.setText("Egalité.")

        if wins(board, HUMAN):
            self.gameStatePause = True
            self.notification.setText("Tu as gagné!")
        self.ai_turn()

    def ai_turn(self):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        depth = len(empty_cells(board))
        if depth == 0 or game_over(board):
            return

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = minimax(board, depth, COMP)
            x, y = move[0], move[1]

        board[x][y] = COMP
        label_no = x * 3 + y
        eval('self.label_'+str(label_no)+'.setPixmap(QtGui.QPixmap(self.xImage))')
        self.emptySpace -= 1
        if wins(board, COMP):
            self.gameStatePause = True
            self.notification.setText("AI a gagné!")

    def newGame(self):
        self.notification.setText("")
        for i in range(3):
            for j in range(3):
                board[i][j] = 0
        self.emptySpace = 9
        self.gameStatePause = False
        self.label_0.clear()
        self.label_1.clear()
        self.label_2.clear()
        self.label_3.clear()
        self.label_4.clear()
        self.label_5.clear()
        self.label_6.clear()
        self.label_7.clear()
        self.label_8.clear()
              


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    TicTacToe = QtWidgets.QMainWindow()
    ui = Ui_TicTacToe()
    ui.setupUi(TicTacToe)
    TicTacToe.show()
    sys.exit(app.exec_())
