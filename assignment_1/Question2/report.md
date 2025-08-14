we are going to have an insane number of propositional variables
aaaaaaaaaaaaaaaaa
since we are allowed t moves, counting the first to the last position we have t+1 board positions in total
at each position there are $N\times M$ grid positions.
at each grid position, it can be 1. empty, 2. wall, 3. player, 4, box, 5. goal. some are mutually exclusive while some are not, but thats still 5
so our total number of propositional variables are $(t+1)\times N\times M\times 5$
we apply constraints on the next time instant propositional values based on the prev time instant values, trying to encode consecutive board positions.
we check if there exist a sequence of moves such that all the boxes do end up at the goals


we are given that $N,M\leq10$. which means the row and column will come in 0-9, a single digit, which is nice.

time instant can be upto 20 as seen in one of the testcases, so i'll let that be highest.

we encode grid position state $s$ as follows:
- 0 - empty space
- 1 - player
- 2 - box
- 3 - goal
- 4 - wall

what we can do is the proposition that at time instant t, at position i,j, there is a certain state is- $t\times1000+i\times100+j\times10+s$
in order to reduce the number of propostional variables, we could also stop tracking grid positions which are walls since they will not change and cannot be any other state. so when checking for wall, we can use the same formula at t=0.



Also, $t*1000+m$ will be the move that we take at time instant t, basically while transtitioning from time t to t+1. m is encoded as follows:
---- Note: can reduce these using 2 binary bits, but this takes much less space compared to the prev one so doesnt matter
- 5 - up
- 6 - down
- 7 - right
- 8 - left

Using these we can write constraints for variables at time t+1 using the value of variables at time t.

-  have no idea what we are going to do if there exists a shorter solution than t moves, if yes how to detect it??
(edit) maybe we can use $t*1000+9$ to denote if the position of any block changed from time instant t-1 to t. if in the end we get SAT, the last t at which there was a move
