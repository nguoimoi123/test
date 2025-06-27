def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j] if board[i][j] != 0 else ".", end=" ")
        print()

# Bảng Sudoku cần giải
board = [
    [0, 0, 4, 1, 0, 0, 3, 9, 0],
    [6, 0, 0, 7, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 7],
    [0, 0, 7, 0, 0, 0, 9, 0, 0],
    [2, 0, 0, 0, 0, 5, 0, 1, 0],
    [9, 4, 0, 0, 1, 7, 5, 3, 0],
    [7, 0, 0, 0, 0, 0, 4, 2, 0],
    [0, 0, 0, 0, 4, 3, 0, 0, 9],
    [0, 0, 3, 9, 0, 8, 0, 0, 0]
]

print("Initial Sudoku:")
print_board(board)

if solve_sudoku(board):
    print("\nSolved Sudoku:")
    print_board(board)
else:
    print("No solution found.")
