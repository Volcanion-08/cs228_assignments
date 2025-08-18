we are going to have an insane number of propositional variables
aaaaaaaaaaaaaaaaa
since we are allowed t moves, counting the first to the last position we have t+1 board positions in total
at each position there are $N\times M$ grid positions. at each grid position, it can be 1. empty, 2. wall, 3. player, 4, box, 5. goal. since some are not mutually exclusive, we will have to maintain 5 separate variables to check for its properties.
so our total number of propositional variables are $(t+1)\times N\times M\times 5$
we apply constraints on the next time instant propositional values based on the prev time instant values, trying to encode consecutive board positions.
we check if there exist a sequence of moves such that all the boxes do end up at the goals


we are given that $N,M\leq10$. which means the row and column will come in 0-9, a single digit, which is nice.

time instant can be upto 20 as seen in one of the testcases, so i'll let that be highest.

we encode grid position state $s$ as follows:
- 0 - wall
- 1 - player
- 2 - box
- 3 - goal

what we can do is the proposition that at time instant t, at position i,j, there is a certain state is- $t\times1000+i\times100+j\times10+s$
in order to reduce the number of propostional variables, we could also stop tracking grid positions which are walls since they will not change and cannot be any other state. so when checking for wall, we can use the same formula at t=0.



Also, $t*1000+m$ will be the move that we take at time instant t, basically while transtitioning from time t to t+1. m is encoded as follows:
---- Note: can reduce these using 2 binary bits, but this takes much less space compared to the prev one so doesnt matter
- 5 - up
- 6 - down
- 7 - right
- 8 - left

Using these we can write constraints for variables at time t+1 using the value of variables at time t.

- a note on solution shorter than length t:
  - if all the boxes are not at goal positions, then the player moves, and a move is recorded in the move-string.
  - once all the boxes reach goal positions, the player stops moving, in which case no move is added to the move-string.
  - this is still not helping us to minimize the number of moves as a meaningless back and forth can delay a 7-move solution to a 9 move solution. in this case we could add a constrant ki no going back and forth unless you push a box
  - this is still insufficient as the player can move in a square and not move any box to then delay a 7 move solution to a 11 move solution. this would not be an issue if t=10, but in a more general algorithmic design i feel something is missing
  - idea: if the player arrives at the same position without moving a box in between, we do not allow it- not sufficient since 'R' can be written as 'DRU' and will not be caught in this case


what we should do on monday-
1. write constraints on variables at time $t$ using values of variables at time $(t-1)$, first in terms of impllications and then as CNF.
2. convert that to code, finding efficient loops to encode it
3. figuring out how to find optimal solution among all possible solutions.
