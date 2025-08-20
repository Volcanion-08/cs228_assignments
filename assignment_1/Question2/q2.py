"""
Sokoban Solver using SAT (Boilerplate)
--------------------------------------
Instructions:
- Implement encoding of Sokoban into CNF.
- Use PySAT to solve the CNF and extract moves.
- Ensure constraints for player movement, box pushes, and goal conditions.

Grid Encoding:
- 'P' = Player
- 'B' = Box
- 'G' = Goal
- '#' = Wall
- '.' = Empty space
"""

from pysat.formula import CNF
from pysat.solvers import Solver

# Directions for movement
DIRS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


class SokobanEncoder:
    def __init__(self, grid, T):
        """
        Initialize encoder with grid and time limit.

        Args:
            grid (list[list[str]]): Sokoban grid.
            T (int): Max number of steps allowed.
        """
        self.grid = grid
        self.T = T
        self.N = len(grid)
        self.M = len(grid[0])

        self.goals = []
        self.boxes = []
        # have added walls, asking if it is allowed
        self.walls = []
        self.empty = []
        self.player_start = None

        # TODO: Parse grid to fill self.goals, self.boxes, self.player_start
        self._parse_grid()

        self.num_boxes = len(self.boxes)
        self.cnf = CNF()

    def _parse_grid(self):
        """Parse grid to find player, boxes, and goals."""
        # TODO: Implement parsing logic
        for i in range(self.N):
            for j in range(self.M):
                if self.grid[i][j] == 'P':
                    if self.player_start != None:
                        raise ValueError("Multiple Players")
                    self.player_start = (i,j)
                elif self.grid[i][j] == 'B':
                    self.boxes.append((i,j))
                elif self.grid[i][j] == 'G':
                    self.goals.append((i,j))
                elif self.grid[i][j] == '#':
                    self.walls.append((i,j))
        return

    # ---------------- Variable Encoding ----------------
    def var_walls(self):
        """
        Variable ID for player at (x, y) at time t.
        """
        # TODO: Implement encoding scheme

        for i in range(self.N):
            for j in range(self.M):
                if (i,j) in self.walls:
                    self.cnf.append([1000*i+10*j+4])
                else:
                    self.cnf.append([-(1000*i+10*j+4)])

        return
    
    
    def var_player(self):
        """
        Variable ID for player at (x, y) at time t.
        """
        # TODO: Implement encoding scheme
        self.cnf.append([1000*self.player_start[0]+10*self.player_start[1]+1])
        # this is sufficient since we are enforcing only one player

        return

    def var_box(self):
        """
        Variable ID for box b at (x, y) at time t.
        """
        # TODO: Implement encoding scheme

        for i in range(self.N):
            for j in range(self.M):
                if (i,j) in self.boxes:
                    self.cnf.append([1000*i+10*j+2])
                else:
                    self.cnf.append([-(1000*i+10*j+2)])

        return
    
    def var_goals(self):
        """
        Variable ID for box b at (x, y) at time t.
        """
        # TODO: Implement encoding scheme
        
        for i in range(self.N):
            for j in range(self.M):
                if (i,j) in self.goals:
                    self.cnf.append([1000*i+10*j+3])
                else:
                    self.cnf.append([-(1000*i+10*j+3)])

        return

    # ---------------- Encoding Logic ----------------

    def encode_move(self):

        # at least one player at all times
        self.cnf.append([(self.T*100000+i*1000+j*10+1) for i in range(self.N) for j in range(self.M)])

        for i in range(self.N):
            for j in range(self.M):
                # there cannot be more than one player
                for i1 in range(self.N):
                    for j1 in range(self.M):
                        if i1==i and j1==j:
                            continue
                        self.cnf.append([-(self.T*100000+i*1000+j*10+1), -(self.T*100000+i1*1000+j1*10+1)])

        for t in range(self.T):

            # at least one player at all times
            self.cnf.append([(t*100000+i*1000+j*10+1) for i in range(self.N) for j in range(self.M)])

            # once completed, should remain completed
            self.cnf.append([-(t*100000+9),(t+1)*100000+9])

            # exaclty one among completed, U, D, R, L
            self.cnf.append([t*100000+9, t*100000+5, t*100000+6, t*100000+7, t*100000+8])
            for k in range(5,9):
                self.cnf.append([-(t*100000+9), -(t*100000+k)])
            self.cnf.append([-(t*100000+5), -(t*100000+6)])
            self.cnf.append([-(t*100000+5), -(t*100000+7)])
            self.cnf.append([-(t*100000+5), -(t*100000+8)])
            self.cnf.append([-(t*100000+6), -(t*100000+7)])
            self.cnf.append([-(t*100000+6), -(t*100000+8)])
            self.cnf.append([-(t*100000+7), -(t*100000+8)])

            for i in range(self.N):
                for j in range(self.M):

                    # wall, box and player are mutually exclusive
                    self.cnf.append([-(t*100000+i*1000+j*10+1), -(i*1000+j*10+4)])
                    self.cnf.append([-(t*100000+i*1000+j*10+2), -(i*1000+j*10+4)])
                    self.cnf.append([-(t*100000+i*1000+j*10+1), -(t*100000+i*1000+j*10+2)])

                    # there cannot be more than one player
                    for i1 in range(self.N):
                        for j1 in range(self.M):
                            if i1==i and j1==j:
                                continue
                            self.cnf.append([-(t*100000+i*1000+j*10+1), -(t*100000+i1*1000+j1*10+1)])

            # cannot go beyond boundary
            for j in range(self.M):
                self.cnf.append([-(t*100000+j*10+1), -(t*100000+5)])
                self.cnf.append([-(t*100000+1000*(self.N-1)+j*10+1), -(t*100000+6)])
            for i in range(self.N):
                self.cnf.append([-(t*100000+i*1000+1), -(t*100000+8)])
                self.cnf.append([-(t*100000+1000*i+10*(self.M-1)+1), -(t*100000+7)])

            # cannot run into wall
            """
            for i in range(self.N):
                for j in range(self.M-1):
                    self.cnf.append([-(t*100000+i*1000+j*10+1), -(t*100000+7), -(i*1000+(j+1)*10+4)])
                    self.cnf.append([-(t*100000+i*1000+(j+1)*10+1), -(t*100000+8), -(i*1000+(j)*10+4)])
            for i in range(self.N-1):
                for j in range(self.M):
                    self.cnf.append([-(t*100000+(i+1)*1000+j*10+1), -(t*100000+5), -((i)*1000+(j)*10+4)])
                    self.cnf.append([-(t*100000+i*1000+j*10+1), -(t*100000+6), -((i+1)*1000+(j)*10+4)])
            """

            # cannot push box out of boundary            
            for j in range(self.M):
                self.cnf.append([-(t*100000+1000+j*10+1), -(t*100000+j*10+2), -(t*100000+5)])
                self.cnf.append([-(t*100000+1000*(self.N-2)+j*10+1), -(t*100000+1000*(self.N-1)+j*10+2),  -(t*100000+6)])
            for i in range(self.N):
                self.cnf.append([-(t*100000+i*1000+10+1), -(t*100000+1000*i+2), -(t*100000+8)])
                self.cnf.append([-(t*100000+1000*i+10*(self.M-2)+1), -(t*100000+1000*i+10*(self.M-1)+2), -(t*100000+7)])

            # cannot push box into wall
            """
            for i in range(self.N):+
                for j in range(self.M-2):
                    self.cnf.append([-(t*100000+(i)*1000+j*10+1), -(t*100000+(i)*1000+(j+1)*10+2), -(t*100000+7), -((i)*1000+(j+2)*10)])
                    self.cnf.append([-(t*100000+(i)*1000+(j+2)*10+1), -(t*100000+(i)*1000+(j+1)*10+2), -(t*100000+8), -((i)*1000+(j)*10)])
            for i in range(self.N-2):
                for j in range(self.M):
                    self.cnf.append([-(t*100000+(i+2)*1000+j*10+1), -(t*100000+(i+1)*1000+j*10+2), -(t*100000+5), -((i)*1000+(j)*10)])
                    self.cnf.append([-(t*100000+(i)*1000+j*10+1), -(t*100000+(i+1)*1000+j*10+2), -(t*100000+6), -((i+2)*1000+(j)*10)])
            """

            # cannot push a box into another box
            for i in range(self.N):
                for j in range(self.M-2):
                    self.cnf.append([-(t*100000+(i)*1000+(j)*10+1), -(t*100000+(i)*1000+(j+1)*10+2), -(t*100000+7), -(t*100000+(i)*1000+(j+2)*10+2)])
                    self.cnf.append([-(t*100000+(i)*1000+(j+2)*10+1), -(t*100000+(i)*1000+(j+1)*10+2), -(t*100000+8), -(t*100000+(i)*1000+(j)*10+2)])
            for i in range(self.N-2):
                for j in range(self.M):
                    self.cnf.append([-(t*100000+(i)*1000+(j)*10+1), -(t*100000+(i+1)*1000+(j)*10+2), -(t*100000+6), -(t*100000+(i+2)*1000+(j)*10+2)])
                    self.cnf.append([-(t*100000+(i+2)*1000+(j)*10+1), -(t*100000+(i+1)*1000+(j)*10+2), -(t*100000+5), -(t*100000+(i)*1000+(j)*10+2)])

            for i in range(self.N):
                for j in range(self.M):

                    # Constraining that box cannot show up unless pushed
                    if j>=self.M-2:
                        self.cnf.append([(t*100000+i*1000+j*10+2), -(t*100000+8), -((t+1)*100000+i*1000+j*10+2)])
                    else:
                        self.cnf.append([(t*100000+i*1000+j*10+2), -((t+1)*100000+i*1000+j*10+2), -(t*100000+i*1000+(j+1)*10+2), -((t+1)*100000+i*1000+(j+1)*10+2)])

                    # updating (t+1) variables
                    # first line is about player movement
                    # second line is about box movement

                    if j!=self.M-1:
                        self.cnf.append([ -(t*100000+i*1000+j*10+1), -(t*100000+7), ((t+1)*100000+i*1000+(j+1)*10+1)])
                        self.cnf.append([ -(t*100000+i*1000+j*10+2), -((t+1)*100000+i*1000+j*10+1), -(t*100000+7), ((t+1)*100000+i*1000+(j+1)*10+2)])
                        
                    if j!=0:
                        self.cnf.append([ -(t*100000+i*1000+j*10+1), -(t*100000+8), ((t+1)*100000+i*1000+(j-1)*10+1)])
                        self.cnf.append([ -(t*100000+i*1000+j*10+2), -((t+1)*100000+i*1000+j*10+1), -(t*100000+8), ((t+1)*100000+i*1000+(j-1)*10+2)])


                    if i!=0:
                        self.cnf.append([ -(t*100000+i*1000+j*10+1), -(t*100000+5), ((t+1)*100000+(i-1)*1000+(j)*10+1)])
                        self.cnf.append([ -(t*100000+i*1000+j*10+2), -((t+1)*100000+i*1000+j*10+1), -(t*100000+5), ((t+1)*100000+(i-1)*1000+(j)*10+2)])


                    if i!=self.N-1:
                        self.cnf.append([ -(t*100000+i*1000+j*10+1), -(t*100000+6), ((t+1)*100000+(i+1)*1000+(j)*10+1)])
                        self.cnf.append([ -(t*100000+i*1000+j*10+2), -((t+1)*100000+i*1000+j*10+1), -(t*100000+6), ((t+1)*100000+(i+1)*1000+(j)*10+2)])

                    # No moving
                    self.cnf.append([ -(t*100000+9), -(t*100000+i*1000+j*10+1), ((t+1)*100000+(i)*1000+(j)*10+1)])

                    # If Box is no more, then player must be present
                    self.cnf.append([ -(t*100000+i*1000+j*10+2), ((t+1)*100000+i*1000+j*10+1), ((t+1)*100000+i*1000+j*10+2)])


                    # self.cnf.append([ (t*100000+i*1000+j*10+2), ((t+1)*100000+i*1000+j*10+1), -((t+1)*100000+i*1000+j*10+2)])


    def encode(self):
        """
        Build CNF constraints for Sokoban:
        - Initial state
        - Valid moves (player + box pushes)
        - Non-overlapping boxes
        - Goal condition at final timestep
        """
        # TODO: Add constraints for:
        # 1. Initial conditions
        # 2. Player movement
        # 3. Box movement (push rules)
        # 4. Non-overlap constraints
        # 5. Goal conditions
        # 6. Other conditions

        self.var_box()
        self.var_goals()
        self.var_player()
        self.var_walls()

        self.encode_move()

        self.cnf.append([-9])

        # checking for clear condition  
        for i in range(self.N):
            for j in range(self.M):
                self.cnf.append([-(self.T*100000+i*1000+j*10+2), (i*1000+j*10+3)])

        return self.cnf


def decode(model, encoder):
    """
    Decode SAT model into list of moves ('U', 'D', 'L', 'R').

    Args:
        model (list[int]): Satisfying assignment from SAT solver.
        encoder (SokobanEncoder): Encoder object with grid info.

    Returns:
        list[str]: Sequence of moves.
    """

    str_out = ""
    N, M, T = encoder.N, encoder.M, encoder.T
    for t in range(T):
        if (t*100000+5) in model:
            str_out = str_out + "U"
        elif (t*100000+6) in model:
            str_out = str_out + "D"
        elif (t*100000+7) in model:
            str_out = str_out + "R"
        elif (t*100000+8) in model:
            str_out = str_out + "L"
    #     count = 0
    #     for i in range(N):
    #         for j in range(M):
    #             if (t*100000+i*1000+j*10+1) in model:
    #                 print((i,j))
    #                 count += 1
    #     if count!=1:
    #         print(count)
    #     for i in range(N):
    #         for j in range(M):
    #             if (i*1000+j*10+4) in model:
    #                 print("#", end="")
    #             elif (t*100000+i*1000+j*10+1) in model:
    #                 print("P", end="")
    #             elif (t*100000+i*1000+j*10+2) in model:
    #                 print("B", end="")
    #             elif (i*1000+j*10+3) in model:
    #                 print("G", end="")
    #             else:
    #                 print(".", end="")
    #         print()
    # for i in range(N):
    #     for j in range(M):
    #         if (T*100000+i*1000+j*10+1) in model:
    #             print((i,j))
    #             count += 1
    # if count!=1:
    #     print(count)
    # for i in range(N):
    #     for j in range(M):
    #         if (i*1000+j*10+4) in model:
    #             print("#", end="")
    #         elif (T*100000+i*1000+j*10+1) in model:
    #             print("P", end="")
    #         elif (T*100000+i*1000+j*10+2) in model:
    #             print("B", end="")
    #         elif (i*1000+j*10+3) in model:
    #             print("G", end="")
    #         else:
    #             print(".", end="")
    #     print()
        
    # TODO: Map player positions at each timestep to movement directions
    return str_out


def solve_sokoban(grid, T):
    """
    DO NOT MODIFY THIS FUNCTION.

    Solve Sokoban using SAT encoding.

    Args:
        grid (list[list[str]]): Sokoban grid.
        T (int): Max number of steps allowed.

    Returns:
        list[str] or "unsat": Move sequence or unsatisfiable.
    """
    encoder = SokobanEncoder(grid, T)
    cnf = encoder.encode()

    with Solver(name='g3') as solver:
        solver.append_formula(cnf)
        if not solver.solve():
            return -1

        model = solver.get_model()
        if not model:
            return -1

        return decode(model, encoder)


