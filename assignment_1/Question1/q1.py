"""
sudoku_solver.py

Implement the function `solve_sudoku(grid: List[List[int]]) -> List[List[int]]` using a SAT solver from PySAT.
"""

from pysat.formula import CNF
from pysat.solvers import Solver
from typing import List

def solve_sudoku(grid: List[List[int]]) -> List[List[int]]:
    """Solves a Sudoku puzzle using a SAT solver. Input is a 2D grid with 0s for blanks."""

    # TODO: implement encoding and solving using PySAT

    cnf = CNF()

    # Set 1

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                cnf.append([100*i+10*j+grid[i][j]])
            cnf.append([100*i + 10*k + (j+1) for k in range(9)])
            cnf.append([100*k + 10*i + (j+1) for k in range(9)])
            clause0 = []
            for k in range(1,10):
                for k1 in range(k+1,10):
                    cnf.append([-(100*i+10*j+k), -(100*i+10*j+k1)])
                clause0.append(100*i+10*j+k)
            cnf.append(clause0)

    for i in range(3):
        for j in range(3):
            for k in range(1,10):
                cnf.append([100*(3*i+i0) + 10*(3*j+j0) + k for j0 in range(3) for i0 in range(3)])

    with Solver(name='glucose3') as solver:
        solver.append_formula(cnf.clauses)
        if solver.solve():
            model = solver.get_model()
            sol = []
            for i in range(9):
                row = []
                for j in range(9):
                    for k in range(1,10):
                        if (100*i+10*j+k) in model:
                            row.append(k)
                sol.append(row)
            return sol
                    
        else:
            return grid
