import numpy as np
import matplotlib.pyplot as plt
from pyomo.environ import ConcreteModel, Var, ConstraintList, SolverFactory, Binary, value

def solve_n_queens(n):
    if n > 27:
        raise ValueError("n must be less than or equal to 27.")

    model = ConcreteModel()
    
    model.x = Var(range(n), range(n), within=Binary)

    model.row_constraint = ConstraintList()
    model.column_constraint = ConstraintList()
    model.diagonal_constraint1 = ConstraintList()
    model.diagonal_constraint2 = ConstraintList()

    for i in range(n):
        model.row_constraint.add(sum(model.x[i, j] for j in range(n)) == 1)

    for j in range(n):
        model.column_constraint.add(sum(model.x[i, j] for i in range(n)) == 1)

    for k in range(-(n-1), n):
        model.diagonal_constraint1.add(sum(model.x[i, i + k] for i in range(n) if 0 <= i + k < n) <= 1)

    for k in range(2 * n - 1):
        model.diagonal_constraint2.add(sum(model.x[i, k - i] for i in range(n) if 0 <= k - i < n) <= 1)

    solver = SolverFactory('glpk')
    solver.solve(model)

    queens = []
    for i in range(n):
        for j in range(n):
            if value(model.x[i, j]) == 1:
                queens.append((i, j))

    board = np.zeros((n, n))
    for queen in queens:
        row, col = queen
        board[row][col] = 1

    return board, queens

def plot_board(board, queens):
    n = board.shape[0]
    checkerboard = np.zeros((n, n, 3))
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                checkerboard[i, j] = [1, 1, 1]  
            else:
                checkerboard[i, j] = [0, 0, 0]  

    plt.figure(figsize=(6, 6))
    plt.imshow(checkerboard, interpolation='nearest')

    for queen in queens:
        row, col = queen
        plt.text(col, row, 'Q', ha='center', va='center', color='red', fontsize=20)

    plt.grid(which='both', color='black', linestyle='-', linewidth=2)
    plt.xticks(np.arange(0.5, n, 1), [])
    plt.yticks(np.arange(0.5, n, 1), [])
    plt.title(f"{n}-Queens Solution")
    plt.show()

while True:
    n = int(input('Enter the number of queens (0 to exit): '))
    if n == 0:
        break
    elif n <= 27:
        board, queens = solve_n_queens(n)

        print("Solution in matrix form:")
        print(board)

        print("\nLocations of queens (i, j):")
        for queen in queens:
            print(queen)

        plot_board(board, queens)
    else:
        print("Please provide a value of n less than or equal to 27.")
