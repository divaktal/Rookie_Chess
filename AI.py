from Soldier import *
import math

def check_win(board, Color):
    points = 0
    for row in range(side):  # |
        for col in range(side - 1):
            if board[row][col].get_Color() == board[row][col + 1].get_Color() and board[row][col].get_Color() != Color_Grey and board[row][col].get_Color() == Color:
                points += 1
            if points == 3:
                return True

    points = 0
    for row in range(side - 1):  # -
        for col in range(side):
            if board[row][col].get_Color() == board[row + 1][col].get_Color() and board[row][col].get_Color() != Color_Grey and board[row][col].get_Color() == Color:
                points += 1
            if points == 3:
                return True

    for row in range(side - 3):  # /
        for col in range(3, side):
            if board[row][col].get_Color() == board[row + 1][col - 1].get_Color() == board[row + 2][col - 2].get_Color() == board[row + 3][col - 3].get_Color() != Color_Grey and board[row][col].get_Color() == Color:
                return True

    for row in range(side - 3):  # \
        for col in range(side - 3):
            if board[row][col].get_Color() == board[row + 1][col + 1].get_Color() == board[row + 2][col + 2].get_Color() == board[row + 3][col + 3].get_Color() != Color_Grey and board[row][col].get_Color() == Color:
                return True

    return False


def valid_move(chosen_soldier, toRow, toCol, board):
    if chosen_soldier.get_Row() == toRow and chosen_soldier.get_Col() == toCol:  # didn't move (V)
        return False

    elif chosen_soldier.get_Col() == toCol:  # -
        if chosen_soldier.get_Row() < toRow:  # ->
            for row in range(chosen_soldier.get_Row() + 1, toRow + 1):
                if board[row][chosen_soldier.get_Col()].get_Color() != Color_Grey:
                    return False

        if toRow < chosen_soldier.get_Row():  # <-
            for row in range(toRow, chosen_soldier.get_Row()):
                if board[row][chosen_soldier.get_Col()].get_Color() != Color_Grey:
                    return False


    elif chosen_soldier.get_Row() == toRow:  # |
        if chosen_soldier.get_Col() < toCol:  # down
            for col in range(chosen_soldier.get_Col() + 1, toCol + 1):
                if board[chosen_soldier.get_Row()][col].get_Color() != Color_Grey:
                    return False

    elif toCol < chosen_soldier.get_Col():
        for col in range(toCol, chosen_soldier.get_Col()):
            if board[chosen_soldier.get_Row()][col].get_Color() != Color_Grey:
                return False

    elif chosen_soldier.get_Row() != toRow and chosen_soldier.get_Col() != toCol:
        return False

    return True


def four_in_row(board):
    winning_lanes = []
    winning_lane = []
    for col in range(side - 3):  # | (V)
        for row in range(side):
            for count in range(4):
                winning_lane.append(board[row][col + count])
            winning_lanes.append(winning_lane)
            winning_lane = []

    winning_lane = []
    for row in range(side - 3):  # - (V)
        for col in range(side):
            for count in range(4):
                winning_lane.append(board[row + count][col])
            winning_lanes.append(winning_lane)
            winning_lane = []

    winning_lane = []
    for col in range(side - 3):  # \ (V)
        for row in range(side - 3):
            for count in range(4):
                winning_lane.append(board[row + count][col + count])
            winning_lanes.append(winning_lane)
            winning_lane = []

    winning_lane = []
    for col in range(2):  # / (V)
        for row in range(side - 2, side):
            for count in range(4):
                winning_lane.append(board[row - count][col + count])
            winning_lanes.append(winning_lane)
            winning_lane = []

    return winning_lanes


def score_AI(board, chosen_soldier):
    score = 0
    winning_lanes = four_in_row(board)
    for check in range(len(winning_lanes)):
        if board[chosen_soldier.get_Row()][chosen_soldier.get_Col()] in winning_lanes[check]:
            ally_soldiers = 0
            enemy_soldiers = 0
            for search_color in winning_lanes[check]:
                if search_color.get_Color() == chosen_soldier.get_Color():
                    ally_soldiers += 1
                elif search_color.get_Color() != Color_Grey:
                    enemy_soldiers += 1

            if ally_soldiers == 1 and enemy_soldiers == 0:
                score += 10
            elif ally_soldiers == 1 and enemy_soldiers == 1:
                score += 5
            elif ally_soldiers == 1 and enemy_soldiers == 2:
                score += 5
            elif ally_soldiers == 1 and enemy_soldiers == 3:
                score += 20
            elif ally_soldiers == 2 and enemy_soldiers == 0:
                score += 15
            elif ally_soldiers == 2 and enemy_soldiers == 1:
                score += 7
            elif ally_soldiers == 2 and enemy_soldiers == 2:
                score += 5
            elif ally_soldiers == 3 and enemy_soldiers == 0:
                score += 18
            elif ally_soldiers == 3 and enemy_soldiers == 1:
                score += 16
            elif ally_soldiers == 4 and enemy_soldiers == 0:
                score += 1000
    return score


def is_terminal(board):
    return check_win(board, Color_Black) or check_win(board, Color_White)

def valid_locations(board, choosen_soldier):
    location = []
    for row in range(side):
        for col in range(side):
            if valid_move(choosen_soldier, row, col, board):
                location.append(board[row][col])
    return location

def mini_max(board, ally_army, enemy_army, depth, AI_turn):
    if depth == 0:
        return 0, 0
    if is_terminal(board):
        if check_win(board, Color_White):
            return -1000000000000,0
        if check_win(board, Color_Black):
            return 100000000000000, 0

    max_score = -math.inf
    max_soldier = None
    if AI_turn:
        for soldier in ally_army:
            for move in valid_locations(board, soldier):
                board_2 = copy_board(board)
                board_2 = move_soldier(board_2, board_2[soldier.get_Row()][soldier.get_Col()], board_2[move.get_Row()][move.get_Col()])
                ally_army_2 = ally_army.copy()
                for fix in range(len(ally_army_2)):
                    if ally_army_2[fix] == soldier:
                        ally_army_2[fix] == board_2[move.get_Row()][move.get_Col()]
                        break
                mimax = mini_max(board_2, ally_army, enemy_army, depth - 1, False)
                score = score_AI(board_2, board_2[move.get_Row()][move.get_Col()]) + mimax[0]
                if max_score < score:
                    max_score = score
                    max_soldier = board_2[move.get_Row()][move.get_Col()]
        return [max_score, max_soldier]

    elif not AI_turn:
        min_score = math.inf
        min_soldier = None
        for soldier in enemy_army:
            for move in valid_locations(board, soldier):
                board_2 = copy_board(board)
                board_2 = move_soldier(board_2, board_2[soldier.get_Row()][soldier.get_Col()], board_2[move.get_Row()][move.get_Col()])
                enemy_army_2 = enemy_army.copy()
                for fix in range(len(enemy_army_2)):
                    if enemy_army_2[fix] == soldier:
                        enemy_army_2[fix] == board_2[move.get_Row()][move.get_Col()]
                        break
                mimax = mini_max(board_2, ally_army, enemy_army, depth - 1, True)
                score = score_AI(board_2, board_2[move.get_Row()][move.get_Col()]) + mimax[0]
                if min_score > score:
                    min_score = score
                    min_soldier = board_2[move.get_Row()][move.get_Col()]
        return [min_score, min_soldier]
