side = 5
Color_White = (255, 255, 255)  # player
Color_Black = (0, 0, 0)  # AI
Color_Grey = (126, 126, 126)


class Soldier:
    def __init__(self, Color, Row, Col, id):
        self.Color = Color
        self.Row = Row
        self.Col = Col
        self.id = id

    def get_id(self):
        return self.id

    def get_Color(self):
        return self.Color

    def change_Color(self, Color):
        self.Color = Color

    def get_Row(self):
        return self.Row

    def change_Row(self, Row):
        self.Row = Row

    def get_Col(self):
        return self.Col

    def change_Col(self, Col):
        self.Col = Col

    def print_color(self):
        if self.Color == Color_White:
            print("W", end=" ")
        if self.Color == Color_Black:
            print("B", end=" ")
        if self.Color == Color_Grey:
            print("G", end=" ")

def crate_board_soldier(size):
    board = []
    for Row in range(size):
        row = []
        for Col in range(size):
            empty_space = Soldier(Color_Grey, Row, Col, 99)
            row.append(empty_space)
        board.append(row)
    return board


def print_board_of_soldiers(board):
    for col in board:
        print('\n')
        for row in col:
            row.print_color()


def move_soldier(board, moving_soldier, moved_soldier):
    toCol = moved_soldier.get_Col()
    toRow = moved_soldier.get_Row()

    moved_soldier.change_Col(moving_soldier.get_Col())
    moved_soldier.change_Row(moving_soldier.get_Row())
    board[moved_soldier.get_Row()][moved_soldier.get_Col()] = moved_soldier

    moving_soldier.change_Col(toCol)
    moving_soldier.change_Row(toRow)
    board[moving_soldier.get_Row()][moving_soldier.get_Col()] = moving_soldier
    return board


def copy_soldier(copied_soldier):
    copy = Soldier(copied_soldier.get_Color(), copied_soldier.get_Row(), copied_soldier.get_Col(), copied_soldier.get_id())
    return copy


def copy_board(board):
    copy = []
    for row in range(side):
        soldier_row = []
        for col in range(side):
            soldier = copy_soldier(board[row][col])
            soldier_row.append(soldier)
        copy.append(soldier_row)
    return copy




