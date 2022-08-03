# OthelloBot

[Feb 2022] I first encountered the game Othello on a plane ride, where I played on the screen of the seat infront of me. Now, years later, I am taking an introductory course in artificial intelligence. I figure it would be good to get some hands on experience implementing the ideas that we are seeing in class. I chose this game to implement, because its not one I've thought about for a long time - I have no real experience in it, and I do not know any strategy. I will keep it this way - besides playing the game for myself. My goal is to create a bot that can beat me - using minimax and some measure of position evaluation.

Update Log
----------
[2/9/2022] Preliminary Coding of the Game

[2/17/2022] The visual and game functionality now works and is available in OthelloGameUpdated.py. It requires pygame to run, and also keeps a tracker of the square counts for each player. Next up is coding the minimax algorithm.

[2/20/2022] Modified the structure to be object-oriented in preparation for implementation of the minimax algorithm.

[2/22/2022] Finally implemented the minimax algorithm - the game now plays! The initial heuristic is the difference between white/black squares, and a game tree is computed up to depth prescribedDepth, which runs quickly for d = 2, 3, 4. Have not tested 5. I have made the bot play itself, it ends up in an interesting arrow pattern for d = 4, for d = 2 some more degenerate form of this arrow pattern. I have added a to do section to this README as a reminder of some things to improve.

To do
-----
1. Implement alpha-beta pruning - should be able to compute 1-2 more plies.
2. Fix error in specific case where no moves possible.
3. Add some randomized component to the game-playing (perhaps let the opening be random - so that the arrow pattern is harder to reduce to).
4. Make prescribedDepth a function of gametime. The middle game generally has the most squares to evaluate - so here we could set d = 4 or so at the moment, but the opening and endgame have very low branching factors, and can probably handle d = 6 or 7.
5. Test against online engine.

Ideas
-----
1. Placing tiles on the boundary of the board is probably a little more useful than just the best choice
2. Heuristic function should also take into account the neighboring squares (including those which are empty!)
3. Initial measure of a position is playerTiles - opponent Tiles
4. It is probably beneficial for a player to make a move that leaves the opponent without moves, so as to get another turn

Ultimately the problem of coming up with a good heuristic depends on a good understanding of the game. I have been playing sporadically so I can return to this project at a later date so I have some more intuition as to how to proceed.
