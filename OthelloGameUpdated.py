import pygame
import math
pygame.init()

# SETTING UP THE DISPLAY VARIABLES AND FUNCTIONS (some might not be immediately useful, but there incase I need it)
screen_width = 400
screen_height = 500
white = (255,255,255)
black = (0,0,0)
green = (50,220,50)
line_width = 6
def draw_grid():
    color = (50,220,50)
    screen.fill(color)
    pygame.draw.line(screen, black, (0, 400), (screen_width, 400), line_width)
    for x in range(1, 8):
        pygame.draw.line(screen, black, (0, x*50), (screen_width, +x*50), line_width)
        pygame.draw.line(screen, black, (x*50, 0), (x*50, screen_height-100), line_width)
    # Run until the user asks to quit

def draw_markers():
    x_pos = 0
    for x in othelloBoard:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.circle(screen, white, (x_pos*50 + 25, y_pos*50 + 25), 20, 25) # might be advised to switch the order eventually since blakc goes first
            if y ==  -1:
                pygame.draw.circle(screen, black,( x_pos*50 + 25, y_pos*50 + 25), 20, 25) # line width increased to 25 wiht the hopes that it will fill the circle
            y_pos+=1
        x_pos+=1
# SETTING UP THE GAME VARIABLES AND FUNCTIONS
# NOTE: SOME OF THESE AREN'T TOTALLY NECESSARY FOR PLAYING! BUT A BOT WILL NEED THEM!
player = -1 # black is -1, white is 1, black starts
othelloBoard = [[0 for x in range(8)] for y in range(8)]
othelloBoard[3][3] = 1
othelloBoard[3][4] = -1
othelloBoard[4][3] = -1
othelloBoard[4][4] = 1
directions = [[1,0], [0,1], [-1, 0], [0, -1], [1,1], [1, -1], [-1, -1], [-1, 1]]
def IsSquarePlayable(Board, Player, Square): # square is of the form [x,y]
    #This needs to check each of 8 directions - we can do 8 while loops for now until we hit white space or another black
    currentSquare = Square
    for i in directions:
        currentSquare[0] = Square[0]+i[0]
        currentSquare[1] = Square[1]+i[1] # pass by reference - but I think this is ok? CHECK
        oppositePlayerSquaresOnTheWay = 0
        while (0 <= currentSquare[0] and currentSquare[0] <= 7 and 0 <= currentSquare[1] and currentSquare[0] <= 7):
            if Board[currentSquare[0]][currentSquare[1]] == -1*Player:
                oppositePlayerSquaresOnTheWay+=1
                currentSquare[0] = currentSquare[0]+i[0]
                currentSquare[1] = currentSquare[1]+i[1]
            elif Board[currentSquare[0]][currentSquare[1]] == Player: # one possible optimization is to check the directions which terminate earliest or something (so it runs the fastest)
                if (oppositePlayerSquaresOnTheWay > 0):
                    return True; #does Python support having this and the next line on one line
                break #if its not an opponent square- no line matters
            else:
                break
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
        currentSquare = Square
        for i in directions:
            currentSquare[0] = Square[0]+i[0]
            currentSquare[1] = Square[1]+i[1]
            L=[]
            print("Going through direction " + str(i))
            while (0 <= currentSquare[0] and currentSquare[0] <= 7 and 0 <= currentSquare[1] and currentSquare[0] <= 7):
                if Board[currentSquare[0]][currentSquare[1]] == -1*Player:
                    L.append([currentSquare[0], currentSquare[1]])
                    currentSquare[0] = Square[0]+i[0]
                    currentSquare[1] = Square[1]+i[1]
                elif Board[currentSquare[0]][currentSquare[1]] == Player:
                    for i in L:
                        Board[i[0]][i[1]] = Player
                    break
                else:
                    break
        othelloBoard[Square[0]][Square[1]] = Player
    else:
        return False

# NOW MOVING ONTO THE GAME DISPLAYING
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Othello')
running = True
clicked = False
while running:
    draw_grid()
    draw_markers() # change the terminology here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicker = False
            pos = pygame.mouse.get_pos()
            cell_x = pos[0]
            cell_y = pos[1]
            if (cell_y <= 400):
                if othelloBoard[cell_x // 50][cell_y // 50] == 0:
                    # this would be where to check if the move is possible
                    #othelloBoard[cell_x // 50][cell_y // 50] = player
                    if not(Move(othelloBoard, player, [cell_x//50, cell_y//50])):
                        player*=-1
                    else:
                        print("Invalid Move for " + str(player))
                else:
                    print("Board already takes that value")
    # Fill the background with white#screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

    
