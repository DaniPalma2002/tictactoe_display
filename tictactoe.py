''' JOGO DO GALO COM DISPLAY '''

# MODULES
import sys
import pygame
import numpy as np

# initializes pygame
pygame.init()

# -----------
# CONSTANTS
#------------
# parametros do tamanho da janela
WIDTH = 600
HEIGHT = WIDTH
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 2 - SQUARE_SIZE // 6
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
# rgb: (red, green, blue)
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# -------
# SCREEN
# -------
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'TIC TAC TOE' ) #titulo
screen.fill( BG_COLOR )
# line: (screen, color, start point, end point, width)
# pygame.draw.line( screen, RED, (10, 10), (300, 300), 10 )

# board - lista das pos
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )
# print(board)


def draw_lines():
    ''' desenha o tabuleiro '''
    # 1 horizontal
    pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )
    # 2 horizontal
    pygame.draw.line( screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH )
    # 1 vertical
    pygame.draw.line( screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH )
    # 2 vertical
    pygame.draw.line( screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH )


def draw_figures():
    ''' PLAYER 1 - CIRCLE
        PLAYER 2 - CROSS
        desenha a figura pretendida no board'''
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle( screen, CIRCLE_COLOR,
                                   (int( col * SQUARE_SIZE + SQUARE_SIZE // 2 ),
                                    int( row * SQUARE_SIZE + SQUARE_SIZE // 2 )),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH )
            elif board[row][col] == 2:
                pygame.draw.line( screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH )
                pygame.draw.line( screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH )


def mark_square(row, col, PLAYER):
    ''' marca a peca do jogador na posicao pretendida, destrutivamente'''
    board[row][col] = PLAYER


def available_square(row, col):
    '''retorna true se a posicao for livre '''
    return board[row][col] == 0


def is_board_full():
    ''' verifica se alguma pos esta livre'''
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row, col):
                return False
    return True


def check_win(PLAYER):
    # vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == PLAYER and board[1][col] == PLAYER and board[2][col] == PLAYER:
            draw_vertical_winning_line(col, PLAYER)
            return True

    # horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == PLAYER and board[row][1] == PLAYER and board[row][2] == PLAYER:
            draw_horizontal_winning_line(row, PLAYER)
            return True

    # asc diagonal win check
    if board[2][0] == PLAYER and board[1][1] == PLAYER and board[0][2] == PLAYER:
        draw_asc_diagonal(PLAYER)
        return True

    # desc horizontal line
    if board[0][0] == PLAYER and board[1][1] == PLAYER and board[2][2] == PLAYER:
        draw_desc_diagonal(PLAYER)
        return True

    return False


def draw_vertical_winning_line(col, PLAYER):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2

    if PLAYER == 1:
        color = CIRCLE_COLOR
    elif PLAYER == 2:
        color = CROSS_COLOR

    pygame.draw.line( screen, color, (posX, 15), (posX, HEIGHT - 15), 15 )


def draw_horizontal_winning_line(row, PLAYER):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2

    if PLAYER == 1:
        color = CIRCLE_COLOR
    elif PLAYER == 2:
        color = CROSS_COLOR

    pygame.draw.line( screen, color, (15, posY), (WIDTH - 15, posY), 15 )


def draw_asc_diagonal(PLAYER):
    if PLAYER == 1:
        color = CIRCLE_COLOR
    elif PLAYER == 2:
        color = CROSS_COLOR

    pygame.draw.line( screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15 )


def draw_desc_diagonal(PLAYER):
    if PLAYER == 1:
        color = CIRCLE_COLOR
    elif PLAYER == 2:
        color = CROSS_COLOR

    pygame.draw.line( screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15 )


def restart():
    screen.fill( BG_COLOR )
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# ----------
# VARIABLES
# ----------

PLAYER = 1
GAME_OVER = False


draw_lines()

#!  mainloop  ------------------------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not GAME_OVER:
        # se clicas no ecra ou eh game over

            mouseX = event.pos[0] #x
            mouseY = event.pos[1] #y

            clicked_row = int(mouseY // SQUARE_SIZE) # limita a pos entre 0, 1, 2
            clicked_col = int(mouseX // SQUARE_SIZE)

            # marcar na pos onde clicamos no ecra, se estiver livre
            if available_square(clicked_row, clicked_col):
                mark_square( clicked_row, clicked_col, PLAYER )
                if check_win( PLAYER ):
                    GAME_OVER = True
                PLAYER = PLAYER % 2 + 1 # muda para outro player
                draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # se a tecla R for clicada, reinicia o jogo
                restart()
                GAME_OVER = False


    pygame.display.update()
