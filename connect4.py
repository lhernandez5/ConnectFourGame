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
RADIUS = int(SQUARE_SIZE / 2 - 5)
game_over = False
turn = 0
win_font = pygame.font.SysFont("monospace", 75)
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_space(board, col):
    return board[ROW_COUNT - 1][col] == 0


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
                if all(board[r][c + i] == piece for i in range(COLUMNS_TO_WIN)):
                    return True

                # Positive diagonal wins
                if r <= ROW_COUNT - ROWS_TO_WIN and all(
                    board[r + i][c + i] == piece for i in range(ROWS_TO_WIN)
                ):
                    return True

            # Vertical wins
            if r <= ROW_COUNT - ROWS_TO_WIN and all(
                board[r + i][c] == piece for i in range(ROWS_TO_WIN)
            ):
                return True

            # Negative diagonal wins
            if (
                c <= COLUMN_COUNT - COLUMNS_TO_WIN
                and r >= ROWS_TO_WIN - 1
                and all(board[r - i][c + i] == piece for i in range(COLUMNS_TO_WIN))
            ):
                return True


def draw_board(board):
    draw_board_background()
    draw_board_pieces(board)


def draw_board_background():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (
                    c * SQUARE_SIZE,
                    r * SQUARE_SIZE + SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                ),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                    int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2),
                ),
                RADIUS,
            )


def draw_board_pieces(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                draw_piece(RED, c, r)
            elif board[r][c] == 2:
                draw_piece(YELLOW, c, r)


def draw_piece(color, column, row):
    pygame.draw.circle(
        screen,
        color,
        (
            int(column * SQUARE_SIZE + SQUARE_SIZE / 2),
            height - int(row * SQUARE_SIZE + SQUARE_SIZE / 2),
        ),
        RADIUS,
    )


def handle_mouse_button_down(event, turn):
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
    posx = event.pos[0]

    turn = turn
    game_over = False

    if event.type == pygame.MOUSEMOTION:
        color = RED if turn == 0 else YELLOW
        pygame.draw.circle(screen, color, (posx, int(SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

    elif event.type == pygame.MOUSEBUTTONDOWN:
        col = int(math.floor(posx / SQUARE_SIZE))
        player = 1 if turn == 0 else 2

        if is_valid_space(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, player)

            if winning_move(board, player):
                draw_winner_message(player)
                game_over = True

        print_board(board)
        draw_board(board)
        turn += 1
        turn %= 2

        if game_over:
            reset_game()
    return turn


def draw_winner_message(player):
    color = "RED" if player == 1 else "YELLOW"
    draw_board(board)
    pygame.display.update()
    label = win_font.render(f"{color} wins!!", 1, color)
    screen.blit(label, (40, 10))
    pygame.display.update()


def reset_game():
    global board, game_over
    board = create_board()
    draw_board(board)
    game_over = False
    return board, game_over


board = create_board()
print_board(board)
draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
            turn = handle_mouse_button_down(event, turn)
