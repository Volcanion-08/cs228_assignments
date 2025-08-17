from q1 import solve_sudoku
from typing import List
from tqdm import tqdm

line = '.....48...1.2367..5.3.176.93..5.....1.942...6.751.8..2.9...5..7..2...43.7..68.9.1'

grid = [
    [int(c) if c.isdigit() else 0 for c in line[i*9:(i+1)*9]]
    for i in range(9)
]

solved = solve_sudoku(grid)

for line in solved:
    for val in line:
        print(val, end=" ")
    print()