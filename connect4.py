import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
game_over = False
turn = 0

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
    print(np.flip(board, 0))

def winning_move(board, piece):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if c <= COLUMN_COUNT - 4:
                # Horizontal wins
                if all(board[r][c+i] == piece for i in range(4)):
                    return True
                
                # Positive diagonal wins
                if r <= ROW_COUNT - 4 and all(board[r+i][c+i] == piece for i in range(4)):
                    return True
                
            # Vertical wins
            if r <= ROW_COUNT - 4 and all(board[r+i][c] == piece for i in range(4)):
                return True
                
            # Negative diagonal wins
            if (c <= COLUMN_COUNT - 4 and r >= 3) and all(board[r-i][c+i] == piece for i in range(4)):
                return True
            
board = create_board()
print_board(board)

while not game_over:
    #Ask for Player 1 input
    if turn == 0:
        col = int(input("Player 1 make your selection (0-6):"))
        
        if is_valid_space(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                print("PLAYER 1 WINS!!! CONGRATS!!!")
                game_over = True
    #Ask for Player 2 input
    else:
        col = int(input("Player 2 make your selection (0-6):"))

        if is_valid_space(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            if winning_move(board, 2):
                print("PLAYER 2 WINS!!! CONGRATS!!!")
                game_over = True

    print_board(board)
        
    turn += 1
    turn = turn % 2