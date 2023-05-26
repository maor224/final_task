def check_win(board):
    # Check rows for win
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != 0:
            return row[0]

    # Check columns for win
    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
            return board[0][col]

    # Check diagonal for win
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        return board[0][2]

    return 0


def check_draw(board):
    for row in board:
        if 0 in row:
            return False
    return True


def main():
    board = [
        [1, 1, 0],
        [1, 1, 2],
        [2, 0, 2]
    ]

    winner = check_win(board)
    if winner != 0:
        print(f"Player {winner} wins!")
    else:
        if check_draw(board):
            print("It's a draw!")
        else:
            print("No winner yet.")


if __name__ == '__main__':
    main()
