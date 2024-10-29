def printer(board):
    n = len(board)
    print('-' * (n * 4 + 1))
    for i in range(n):
        for j in range(n):
            print('| Q' if board[i][j] == 1 else '|  ', end=' ')
        print('|')
        print('-' * (n * 4 + 1))

def solforNQ(board, col, ld, rd, cl, solutions, skip=None):
    n = len(board)
    if col >= n:
        solutions.append([row[:] for row in board])
        return
    
    if col == skip:
        solforNQ(board, col + 1, ld, rd, cl, solutions, skip)
        return
    
    for i in range(n):
        if ld[i - col + n - 1] == 0 and rd[i + col] == 0 and cl[i] == 0:
            board[i][col] = 1
            ld[i - col + n - 1] = 1
            rd[i + col] = 1
            cl[i] = 1
            
            solforNQ(board, col + 1, ld, rd, cl, solutions, skip)
            
            board[i][col] = 0
            ld[i - col + n - 1] = 0
            rd[i + col] = 0
            cl[i] = 0

def solveNQ(n, row, col):
    board = [[0 for _ in range(n)] for _ in range(n)]
    ld = [0] * (2 * n - 1)
    rd = [0] * (2 * n - 1)
    cl = [0] * n
    
    board[row][col] = 1
    ld[row - col + n - 1] = 1
    rd[row + col] = 1
    cl[row] = 1
    
    solutions = []
    solforNQ(board, 0, ld, rd, cl, solutions, skip=col)
    
    if not solutions:
        print(f"No solution found for N = {n}")
    else:
        # print(f"Found {len(solutions)} solutions for N = {n}:")
        print(f"Solution to the N-Queens for the board of {n} ")
        for solution in solutions:
            printer(solution)
            break

def main():
    print("'Maximum Limit is 20'  'exit' to quit")
    while True:
        user_input = input("Enter the Size of the chess board N  : ")
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        try:
            n = int(user_input)
            if n <= 0:
                raise ValueError("Please enter a positive integer.")
            row = int(input(f"Enter a row coordinate bw (1 to {n}) : "))
            col = int(input(f"Enter a col coordinate bw (1 to {n}) : "))
            if not (1 <= row <= n) or not (1 <= col <= n):
                print("Row and column must be within the range of the board.")
                continue
            solveNQ(n, row-1, col-1)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

main()