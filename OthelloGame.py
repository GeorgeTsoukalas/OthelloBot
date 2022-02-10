# This is the Othello Bot - I first need to code the game
OthelloBoard = [[0 for x in range (8)] for y in range(8)]
#Reminder: Always start indexing from 0 - should not be an issue once the game coding is done
#Let's say -1 is for black, 1 is for white, 0 is for nothing on that square
def IsSquarePlayable(Board, Player, Square): # square is of the form [x,y]
    #This needs to check each of 8 directions - we can do 8 while loops for now until we hit white space or another black
    Directions = [[1,0], [0,1], [-1, 0], [0, -1], [1,1], [1, -1], [-1, -1], [-1, 1]]
    for i in Directions:
        currentSquare[0] = Square[1]+i[0]
        currentSquare[1] = Square[1]+i[1] # pass by reference - but I think this is ok? CHECK
        oppositePlayerSquaresOnTheWay = 0
        while (0 <= currentSquare[0] and currentSquare[0] <= 7 and 0 <= currentSquare[1] and currentSquare[0] <= 7):
            if Board[currentSquare[0]][currentSquare[1]] == -1*Player:
                oppositePlayerSquaresOnTheWay++
                currentSquare[0] = currentSquare[0]+i[0]
                currentSquare[1] = currentSquare[1]+i[1]
            else # does Python support having this and the next line on one line
                break # if its not an opponent square- no line matters
        if oppoSitePlayerSquaresOnTheWay > 0:
            return True;
    return False # Could use this method to store info about heuristic aswell - how many grids  - per direction?
def AvailableSquares(Board, Player): #PLAYER -1 is the Black player - who makes -1 squares, PLAYER 1 is the White player - who makes 1 squares.
    PlayableSpaces=[]
    for i in range(8):
        for j in range(8):
            if Board[i][j] == 0:
                if IsSquarePlayable(Board, Player, [i,j]):
                    PlayableSpaces.append([i,j])
    return PlayableSpaces
#OPTIMIZATIONS TO AVAILABLESQUARES
#2. PlayableSpaces can be modified to give information about the Heuristic aswell - can do one function call 
#1. MODIFY BOARD DATA STRUCTURE TO STORE 0 TILES ALL IN ONE PLACE - DONT HAVE TO ITERATE 64 TILES EVERY TIME (major improvement)
def Move(Board, Player, Square):
    if IsSquarePlayable(Board, Player, Square):
        Directions = [[1,0], [0,1], [-1, 0], [0, -1], [1,1], [1, -1], [-1, -1], [-1, 1]]
        for i in Directions:
            currentSquare[0] = Square[1]+i[0]
            currentSquare[1] = Square[1]+i[1]
            while (0 <= currentSquare[0] and currentSquare[0] <= 7 and 0 <= currentSquare[1] and currentSquare[0] <= 7):
                L=[]
                if Board[currentSquare[0]][currentSquare[1]] == -1*Player:
                    L.append([currentSquare[0], currentSquare[1])
                    currentSquare[0] = Square[1]+i[0]
                    currentSquare[1] = Square[1]+i[1]
                elif Board[currentSquare[0]][currentSquare[1]] == Player:
                    for i in L:
                        Board[i[0]][i[1]] = Player
                else
                    break
def Game(Board):
    # need to construct display
    # need to have way to read in inputs for game

            
                
    
