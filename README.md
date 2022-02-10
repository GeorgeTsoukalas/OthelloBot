# OthelloBot

I first encountered the game Othello on a plane ride, where I played on the screen of the seat infront of me. Now, years later, I am taking an introductory course in artificial intelligence. I figure it would be good to get some hands on experience implementing the ideas that we are seeing in class. I chose this game to implement, because its not one I've thought about for a long time - I have no real experience in it, and I do not know any strategy. I will keep it this way - besides playing the game for myself. My goal is to create a bot that can beat me, and then see if there is some ELO system I can use to rank my bot - and see how well it can perform. I don't know if this game is solved or not, and I'm not going to look it up. Seems complicated enough that we might not have it yet.

Update Log
----------
[2/9/2022] Preliminary Coding of the Game


Ideas
-----
1. Placing tiles on the boundary of the board is probably a little more useful than just the best choice
2. Heuristic function should also take into account the neighboring squares (including those which are empty!)
3. Initial measure of a position is playerTiles - opponent Tiles
4. It is probably beneficial for a player to make a move that leaves the opponent without moves, so as to get another turn

More to come, for sure.
