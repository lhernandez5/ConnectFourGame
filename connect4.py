import numpy as np
import pygame
import sys
import math

pygame.init()

ROW_COUNT = 6
COLUMN_COUNT = 7
ROWS_TO_WIN = 4
COLUMNS_TO_WIN = 4
EMPTY_CELL = 0
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 5)
game_over = False
turn = 0
win_font = pygame.font.SysFont("monospace", 75)
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE
size = (width, height)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

def create_board():
    board= np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_space(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, EMPTY_CELL))

def winning_move(board, piece):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if c <= COLUMN_COUNT - COLUMNS_TO_WIN:
                # Horizontal wins
                if all(board[r][c+i] == piece for i in range(COLUMNS_TO_WIN)):
                    return True
                
                # Positive diagonal wins
                if r <= ROW_COUNT - ROWS_TO_WIN and all(board[r+i][c+i] == piece for i in range(ROWS_TO_WIN)):
                    return True
                
            # Vertical wins
            if r <= ROW_COUNT - ROWS_TO_WIN and all(board[r+i][c] == piece for i in range(ROWS_TO_WIN)):
                return True
                
            # Negative diagonal wins
            if c <= COLUMN_COUNT - COLUMNS_TO_WIN and r >= ROWS_TO_WIN-1 and all(board[r-i][c+i] == piece for i in range(COLUMNS_TO_WIN)):
                return True

def draw_board(board):
    draw_board_background()
    draw_board_pieces(board)
    pygame.display.update()

def draw_board_background():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)

def draw_board_pieces(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                draw_piece(RED, c, r)
            elif board[r][c] == 2:
                draw_piece(YELLOW, c, r)

def draw_piece(color, column, row):
    pygame.draw.circle(screen, color, (int(column*SQUARE_SIZE+SQUARE_SIZE/2), height-int(row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
    

board = create_board()
print_board(board)
draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            print(event.pos)
            #Ask for Player 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if is_valid_space(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = win_font.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
            # #Ask for Player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if is_valid_space(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    if winning_move(board, 2):
                        label = win_font.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)  
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)