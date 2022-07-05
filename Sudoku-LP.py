import numpy as np
from pulp import *
from scipy.stats import bernoulli as bn
from random import shuffle

rows = columns = np.arange(9)
values = np.arange(1, 10)

# contains problem data
prob = LpProblem("Sudoku_Problem")

# Set a dummy objective
objective = lpSum(0)
prob.setObjective(objective)

# The decision variables are created
choices = LpVariable.dicts("Choice", (values, rows, columns), cat="Binary")

# constraints:

for r in rows:
    for c in columns:
        # constraint 1 (only one value is filled for a cell)
        prob += lpSum([choices[v][r][c] for v in values]) == 1
        c0 = (c // 3) * 3
        r0 = (r // 3) * 3
        for (i, j) in list(itertools.product(range(3), repeat=2)):
            # constraint 2 (values from 1 to 9 is filled only once in a box)
            prob += lpSum([choices[v][r0 + i][c0 + j] for v in values]) == 1

for v in values:
    for r in rows:
        # constraint 3 (values from 1 to 9 is filled only once in a row)
        prob += lpSum([choices[v][r][c] for c in columns]) == 1

    for c in columns:
        # constraint 4 (values from 1 to 9 is filled only once in a column)
        prob += lpSum([choices[v][r][c] for r in rows]) == 1

prob.solve()

# empty sudoku board
grid = np.zeros((9, 9), int)

rc_values = list(itertools.product(range(9), repeat=2))
shuffle(rc_values)

# generates a random, complete sudoku grid
for (r, c) in rc_values:
    for v in values:
        if value(choices[v][r][c]) == 1:
            grid[r][c] = v

# stores complete board
grid_answer = grid


# prints sudoku board
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


# replaces some elements of board with 0 (0 represents an empty space)
# the number of elements replaced is dependent on user input
def problem_grid(board):
    try:
        p = float(input("\nDifficulty? (Number between 0.2-0.8, 0.2 is hardest, 0.8 is easiest)\n"))
        if p < 0.2 or p > 0.8:
            print("that's not a number between 0.2 and 0.8!")
            problem_grid(board)
    except ValueError:
        print("that's not a float!")
        problem_grid(board)
    flag = bn.rvs(p=p, size=(9, 9))
    board *= flag
    print("\nhere is the puzzle board:\n")
    print_board(board)
    reveal_answer()


# asks user if they want the answer
def reveal_answer():
    input("provide any input for an answer\n")
    print("\n")
    solve()


# prints solved board
def solve():
    print_board(grid_answer)


grid_copy = grid.copy()
problem_grid(grid_copy)
