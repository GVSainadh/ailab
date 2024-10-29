import random
def generate_magic_square():
    magic_square = [[0] * 3 for _ in range(3)]
    i, j = 0, 1
    for num in range(1, 10):
        magic_square[i][j] = num
        new_i, new_j = (i - 1) % 3, (j + 1) % 3
        if magic_square[new_i][new_j] != 0:
            i += 1
        else:
            i, j = new_i, new_j
    return [[magic_square[j][i] for j in range(2, -1, -1)] for i in range(3)]

def print_board(board, magic_square):
    print("Board:")
    for r in range(3):
        row = []
        for c in range(3):
            # Display the board marker if it's occupied, otherwise show the magic square number
            if board[r][c] != " ":
                row.append(f"{board[r][c]:2}")
            else:
                row.append(f"{magic_square[r][c]:2}")
        print("  |  ".join(row))
    print()

def toss_coin():
    return random.choice([0, 1])

def check_winner(board, marker):
    win_cond = [marker] * 3
    for row in board:
        if row == win_cond:
            return True
    for col in range(3):
        if [board[row][col] for row in range(3)] == win_cond:
            return True
    if [board[i][i] for i in range(3)] == win_cond:
        return True
    if [board[i][2 - i] for i in range(3)] == win_cond:
        return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_empty_positions(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def number_to_position(num, magic_square):
    for r in range(3):
        for c in range(3):
            if magic_square[r][c] == num:
                return (r, c)
    return None

def human_move(board, magic_square, marker):
    print("Your move:")
    while True:
        try:
            num = int(input("Enter a number from the magic square: "))
            if num < 1 or num > 9:
                print("Invalid number. Please enter a number from the magic square.")
                continue
            row, col = number_to_position(num, magic_square)        
            if row is not None and col is not None and (row, col) in get_empty_positions(board):
                board[row][col] = marker
                print_board(board, magic_square)
                break
            else:
                print("Invalid move. Cell already occupied or out of bounds.")
        except ValueError:
            print("Invalid input. Please enter a number from the magic square.")

def can_win(board, marker):
    for row in range(3):
        if board[row].count(marker) == 2 and board[row].count(" ") == 1:
            return (row, board[row].index(" "))
    for col in range(3):
        col_values = [board[row][col] for row in range(3)]
        if col_values.count(marker) == 2 and col_values.count(" ") == 1:
            return (col_values.index(" "), col)
    diag1 = [board[i][i] for i in range(3)]
    if diag1.count(marker) == 2 and diag1.count(" ") == 1:
        return (diag1.index(" "), diag1.index(" "))
    diag2 = [board[i][2 - i] for i in range(3)]
    if diag2.count(marker) == 2 and diag2.count(" ") == 1:
        return (diag2.index(" "), 2 - diag2.index(" "))
    return None

def computer_move(board, marker, magic_square, player_marker):
    print("Computer's move:")
    if get_empty_positions(board) and board[1][1] == " ":
        row, col = 1, 1
        board[row][col] = marker
        print_board(board, magic_square)
        return
    move = can_win(board, marker)
    if move:
        row, col = move
        board[row][col] = marker
        print_board(board, magic_square)
        return
    move = can_win(board, player_marker)
    if move:
        row, col = move
        board[row][col] = marker
        print_board(board, magic_square)
        return
    empty_positions = get_empty_positions(board)
    if empty_positions:
        row, col = random.choice(empty_positions)
        board[row][col] = marker
    print_board(board, magic_square)

def main():
    while True:
        magic_square = generate_magic_square()
        print("Welcome to Tic-Tac-Toe!")
        print_board(magic_square, [[" " for _ in range(3)] for _ in range(3)])
        while True:
            try:
                user_toss = input("Choose 0 or 1 for Toss: ")
                if user_toss not in ['0', '1']:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter 0 for Heads or 1 for Tails.")
        coin_toss_result = toss_coin()
        if int(user_toss) == coin_toss_result:
            first_player = "Human"
            print("You won the toss!")
            player_marker = "X"
            computer_marker = "O"
        else:
            first_player = "Computer"
            print("Computer won the toss!")
            player_marker = "O"
            computer_marker = "X"
        board = [[" " for _ in range(3)] for _ in range(3)]
        turn = first_player
        while True:
            if turn == "Human":
                human_move(board, magic_square, player_marker)
                if check_winner(board, player_marker):
                    print("Congratulations! You win!")
                    break
                turn = "Computer"
            else:
                computer_move(board, computer_marker, magic_square, player_marker)
                if check_winner(board, computer_marker):
                    print("Computer wins! Better luck next time.")
                    break
                turn = "Human"
            
            if check_draw(board):
                print("It's a draw!")
                break
        while True:
            play_again = input("Do you want to play again? (yes/no): ").lower()
            if play_again in ["yes", "no"]:
                break
            print("Invalid input. Please enter 'yes' or 'no'.")
        if play_again != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()