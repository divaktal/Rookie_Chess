from AI import *
import pygame
import sys

Color_Yellow = (255,255,0)
tile_zise = 100
radius = int(tile_zise/2 - 5)

def draw_board(board):
   for col in range(side):
       for row in range(side):
           pygame.draw.rect(screen, (0, 0, 200), (col*tile_zise, row*tile_zise + tile_zise, tile_zise, tile_zise))
           if board[row][col].get_Color() == Color_Grey:
               pygame.draw.circle(screen, Color_Grey, (int(col * tile_zise + tile_zise / 2), int(row * tile_zise + tile_zise + tile_zise / 2)), radius)
           elif board[row][col].get_Color() == Color_Black:
               pygame.draw.circle(screen, Color_Black, (int(col * tile_zise + tile_zise / 2), int(row * tile_zise + tile_zise + tile_zise / 2)), radius)
           else:
               pygame.draw.circle(screen, Color_White, (int(col * tile_zise + tile_zise / 2), int(row * tile_zise + tile_zise + tile_zise / 2)), radius)


board_of_soldiers = crate_board_soldier(side)
black_side_col = [1, 3, 0, 0, 2, 4]
black_side_row = [0, 0, 2, 4, 4, 4]
black_army = []
for pos in range(len(black_side_row)):
    black_soldier = Soldier(Color_Black, black_side_row[pos], black_side_col[pos], pos)
    black_army.append(black_soldier)

for soldier in black_army:
    board_of_soldiers[soldier.get_Row()][soldier.get_Col()] = soldier

white_side_col = [0, 2, 4, 4, 1, 3]
white_side_row = [0, 0, 0, 2, 4, 4]
white_army = []
for pos in range(len(white_side_row)):
    white_soldier = Soldier(Color_White, white_side_row[pos], white_side_col[pos], pos)
    white_army.append(white_soldier)

for soldier in white_army:
    board_of_soldiers[soldier.get_Row()][soldier.get_Col()] = soldier

width = side * tile_zise
height = (side + 1) * tile_zise
size = (width, height)
screen = pygame.display.set_mode(size)
screen.fill(Color_Yellow)
draw_board(board_of_soldiers)
pygame.display.update()
turn = 0

while not is_terminal(board_of_soldiers):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn % 3 == 0:
                col = (int((event.pos[0] / 100)))
                row = (int((event.pos[1] - tile_zise) / 100))
                if board_of_soldiers[row][col].get_Color() == Color_White:
                    soldier = board_of_soldiers[row][col]
                    turn += 1
                    print(soldier.get_Color())
            elif turn % 3 == 1:
                tocol = (int((event.pos[0] / 100)))
                torow = (int((event.pos[1] - tile_zise) / 100))
                if valid_move(soldier, torow, tocol, board_of_soldiers):
                    move_soldier(board_of_soldiers, soldier, board_of_soldiers[torow][tocol])
                    turn += 1
                    draw_board(board_of_soldiers)
                    pygame.display.update()

            else:
                mimax = mini_max(board_of_soldiers, black_army, white_army, 3, True)
                max_soldier = mimax[1]
                moving_soldier = None
                for find in black_army:
                    if find.get_id() == max_soldier.get_id():
                        moving_soldier = find
                        break
                board_of_soldiers = move_soldier(board_of_soldiers, moving_soldier, board_of_soldiers[max_soldier.get_Row()][max_soldier.get_Col()])
                turn += 1
                draw_board(board_of_soldiers)
                pygame.display.update()

if check_win(board_of_soldiers, Color_Black):
    pygame.init()
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    X = 400
    Y = 400
    display_surface = pygame.display.set_mode((X, Y))
    pygame.display.set_caption('Show Text')
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Black Won', True, green, blue)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2)
    while True:
        display_surface.fill(white)
        display_surface.blit(text, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pygame.display.update()

if check_win(board_of_soldiers, Color_White):
    pygame.init()
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    X = 400
    Y = 400
    display_surface = pygame.display.set_mode((X, Y))
    pygame.display.set_caption('Show Text')
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('White Won', True, green, blue)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2)
    while True:
        display_surface.fill(white)
        display_surface.blit(text, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pygame.display.update()