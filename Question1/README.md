# Encoding

- A good place to start would be P(i,j,k) is the atomic proposition that the number at grid position (i,j) is k.
- This can be encoded into the 3 digit number ijk, or $100\times i + 10*j + k$ to be that proposition.

# Building the CNF

## Part 1: Encoding the rules of Sudoku
- We will need 4 sets of clauses.
    - First set contains clauses that each grid position has exactly one number in it,
    - Second set contains clauses that say that each row has all numbers 1 through 9 exaclty once,
    - Third set does the same but for coolums, and finally
    - Fourth set does the same for each subgrid.
- Since there are 9 positions and 9 numbers, once we enforce that all numbers appear atleast once, we need not write additional clauses to enforce non-repititions. The first set of clauses will enforce that one grid position cannot hold more than one number. Thus the 9 numbers will occupy the 9 positions and there will be no space for repititions to occur.

## Part 2: Initializing input grid of Sudoku
- This is fairly straightforward, we iterate through the input grid, and when we find a non-zero entry k at position (i,j), we set the clause P(i,j,k) to be true, add it to the CNF.
