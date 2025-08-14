we are going to have an insane number of propositional variables
aaaaaaaaaaaaaaaaa
since we are allowed t moves, counting the first to the last position we have t+1 board positions in total
at each position there are $N\times M$ grid positions.
at each grid position, it can be 1. empty, 2. wall, 3. player, 4, box, 5. goal. some are mutually exclusive while some are not, but thats still 5
so our total number of propositional variables are $(t+1)\times N\times M\times 5$
we apply constraints on the next time instant propositional values based on the prev time instant values, trying to encode consecutive board positions.
we check if there exist a sequence of moves such that all the boxes do end up at the goals

- have no idea what we are going to do if there exists a shorter solution than t moves, if yes how to detect it??
