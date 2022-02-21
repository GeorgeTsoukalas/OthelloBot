import pygame
import math
import numpy
class OthelloBoard:
    def __init__(self, board, square_counts, player,empty_spaces):
        self.board=board
        self.player=player
        self.square_counts=square_counts
        self.empty_spaces=empty_spaces
    def IsSquarePlayable(self, Square): # square is of the form [x,y]
        #This needs to check each of 8 directions - we can do 8 while loops for now until we hit white space or another black
        currentSquare = Square[:]
        for i in directions:
            currentSquare = Square[:]
            currentSquare[0]+=i[0]
            currentSquare[1]+=i[1] # pass by reference - but I think this is ok? CHECK
            #print("Current Square is "+str(currentSquare))
            oppositePlayerSquaresOnTheWay = 0
            while (0 <= currentSquare[0] and currentSquare[0] <= 7 and 0 <= currentSquare[1] and currentSquare[1] <= 7):
                #print("Curreny Square is "+str(currentSquare))
                if self.board[currentSquare[0]][currentSquare[1]] == -1*self.player:
                    oppositePlayerSquaresOnTheWay+=1
                    currentSquare[0] = currentSquare[0]+i[0]
                    currentSquare[1] = currentSquare[1]+i[1]
                elif self.board[currentSquare[0]][currentSquare[1]] == self.player: # one possible optimization is to check the directions which terminate earliest or something (so it runs the fastest)
                    if (oppositePlayerSquaresOnTheWay > 0):
                        return True; #does Python support having this and the next line on one line
                    break #if its not an opponent square- no line matters
                else:
                    break
        return False
    def AvailableSquares(self): #PLAYER -1 is the Black player - who makes -1 squares, PLAYER 1 is the White player - who makes 1 squares.
        PlayableSpaces=[]
        for square in self.empty_squares:
            if self.IsSquarePlayable(square):
                PlayableSpaces.append(square[:]) #duplicating it just in case I don't know how python works - haha!
        return PlayableSpaces
    def Move(self, Square):
        #print("Move starting up")
        if self.IsSquarePlayable(Square):
            currentSquare = Square[:]
            for i in directions:
                currentSquare = Square[:]
                currentSquare[0]+=i[0]
                currentSquare[1]+=i[1]
                #print("Square is "+str(Square))
                #print("CurrentSquare is "+str(currentSquare))
                L=[]
                #print("Going through direction " + str(i))
                while (0 <= currentSquare[0] and currentSquare[0] <= 7 and 0 <= currentSquare[1] and currentSquare[1] <= 7):
                    if self.board[currentSquare[0]][currentSquare[1]] == -1*self.player:
                        L.append([currentSquare[0], currentSquare[1]])
                        currentSquare[0]+=i[0]
                        currentSquare[1]+=i[1]
                    elif self.board[currentSquare[0]][currentSquare[1]] == self.player:
                        for i in L:
                            #print("Changing the possession of "+str(i))
                            self.board[i[0]][i[1]] = self.player
                            self.square_counts[self.player]+=1
                            self.square_counts[-1*self.player]-=1
                        break
                    else:
                        break
            self.square_counts[self.player]+=1
            return True
        else:
            #print("Square was not available")
            return False
    def clear(self):
        self.player=-1
        self.board=[[0 for x in range(8)] for y in range(8)]
        self.board[4][4]=1
        self.board[3][3]=1
        self.board[3][4]=-1
        self.board[4][3]=-1
        self.board[2][3] = 2
        self.board[3][2] = 2
        self.board[4][5] = 2
        self.board[5][4] = 2
        self.square_counts={
            1:2,
            -1:2
        }
        self.empty_spaces=[[a,b] for a in range(8) for b in range(8)]
        self.empty_spaces.remove([4,4])
        self.empty_spaces.remove([3,3])
        self.empty_spaces.remove([3,4])
        self.empty_spaces.remove([4,3])
class GameNode:
    def __init__(self,state, value=0, parent=None, depth):
        self.state = state
        self.value = value
        self.parent = parent
        self.children = []
        self.depth = depth
    def addChild(self, childNode):
        self.children.append(childNode)
class GameTree: # prescribedDepth is a glboal 
    def __init__(self):
        self.root = None
    def build_tree(self, startingState): # put datalist = (NEED TO HANDLE THE CASE WHERE PLAYER CANNOT MAKE MORE MOVES!
        self.root = GameNode(startingState, 0, None, 0) # MUST PASS IN THE ENTIRE OTHELLOBOARD CLASS
        L=[self.root]
        while (len(L) > 0):
            Q:=L.pop(0);
            deepCopy = OthelloBoard(Q.state.board.copy(), Q.state.square_counts.copy(), Q.state.player, Q.state.empty_spaces.copy())
            for i in Q.state.AvailableSpaces():
                Q[1].addChild(
                    GameNode(
                    deepCopy.Move(i), 0, Q, Q.depth+1)) # update the values here
            if Q.depth+1 < prescribedDepth: # so the entires will go 1 over the prescribed depth
                for i in Q.children:
                    L.append(i)
    
        # let's hope that this actually works thus far
        # might need a deep copy of Q when moved
# Now I will write THE NEW LOOP!

while(blah):
    if player == -1: # this is the HUMAN controlled player atm

    else:
        gameTree = GameTree().build_tree(othelloBoard)
        miniMax =  MiniMax(gameTree)
        miniMax.minimax(self.root)

class MiniMax:
    def __init__(self, game_tree):
        self.game_tree = game_tree
        self.root = game_true.root
        self.currentNode = None
        self.successors = []
        return
    def minimax(self, node):
        best_val = self.max_value(node)
        successors=self.getSuccessors(node)
        best_move=None
        for nextState in successors:
            if nextState.value==best_val:
                best_move=nextState
            break
        return best_move
    def max_value(self,node):
        if self.isTerminal(node):
            return self.getUtility(node)
        max_value=-100000 # basically -infinity
        successors_states=self.getSuccessors(node)
        for state in successors_states:
            max_value=max(max_value, self.min_value(state))
        return max_value
    def min_value(self,node):
        if self.isTerminal(node):
            return self.getUtility(node)
        min_value = 100000 #basically infinity
        successor_states=self.getSucessors(node)
        for state in successor_states:
            min_value=min(min_value, self.max_value(state))
        return min_value
    def getSuccessors(self,node):
        assert node is not None
        return node.children
    def isTerminal(self,node):
        assert node is not None
        return len(node.children)==0
    def getUtility(self,node):
        assert node is not None
        return node.value # change this

#initialize starting setup
player=-1
board=[[0 for x in range(8)] for y in range(8)]
board[4][4]=1
board[3][3]=1
board[3][4]=-1
board[4][3]=-1
board[2][3] = 2
board[3][2] = 2
board[4][5] = 2
board[5][4] = 2
square_counts={
    1:2,
    -1:2
}
empty_spaces=[[a,b] for a in range(8) for b in range(8)]
empty_spaces.remove([4,4])
empty_spaces.remove([3,3])
empty_spaces.remove([3,4])
empty_spaces.remove([4,3])
othelloBoard = OthelloBoard(board, square_counts, player, empty_spaces)
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Times New Roman', 18)
# 2 represents an avaliable square for that player
# SETTING UP THE DISPLAY VARIABLES AND FUNCTIONS (some might not be immediately useful, but there incase I need it)
screen_width = 400
screen_height = 500
white = (255,255,255)
black = (0,0,0)
green = (50,220,50)
gray = (82,94,85)
line_width = 6
def draw_grid():
    color = (50,2
20,50)
    screen.fill(color)
    pygame.draw.line(screen, black, (0, 400), (screen_width, 400), line_width)
    for x in range(1, 8):
        pygame.draw.line(screen, black, (0, x*50), (screen_width, +x*50), line_width)
        pygame.draw.line(screen, black, (x*50, 0), (x*50, screen_height-100), line_width)
    # Run until the user asks to quit

def draw_markers():
    x_pos = 0
    for x in othelloBoard.board:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.circle(screen, white, (x_pos*50 + 25, y_pos*50 + 25), 20, 25) # might be advised to switch the order eventually since blakc goes first
            if y == -1:
                pygame.draw.circle(screen, black,( x_pos*50 + 25, y_pos*50 + 25), 20, 25) # line width increased to 25 wiht the hopes that it will fill the circle
            if y == 2:
                pygame.draw.circle(screen, gray, (x_pos*50 + 25, y_pos*50 + 25), 20, 4)
            y_pos+=1
        x_pos+=1
# SETTING UP THE GAME VARIABLES AND FUNCTIONS
# NOTE: SOME OF THESE AREN'T TOTALLY NECESSARY FOR PLAYING! BUT A BOT WILL NEED THEM!
directions = [[1,0], [0,1], [-1, 0], [0, -1], [1,1], [1, -1], [-1, -1], [-1, 1]]
# NOW MOVING ONTO THE GAME DISPLAYING
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Othello')
running = True
clicked = False
while running:
    draw_grid()
    draw_markers() # change the terminology here
    if (othelloBoard.player == -1):
        textsurface = myfont.render('Turn: Black, Square Counts: Black: '+str(othelloBoard.square_counts[-1]) + ' and White: ' + str(othelloBoard.square_counts[1]), False, (0,0,0))
        screen.blit(textsurface, (0, 450))
    elif (othelloBoard.player==1):
        textsurface = myfont.render('Turn: White, Square Counts: Black: '+str(othelloBoard.square_counts[-1]) + ' and White: ' + str(othelloBoard.square_counts[1]), False, (0,0,0))
        screen.blit(textsurface, (0, 450))
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
            #print("This is cell ["+str(cell_x//50)+","+str(cell_y//50))
            if (cell_y <= 400):
                #print("Made it though the 400 check")
                if othelloBoard.board[cell_x // 50][cell_y // 50] == 2 or othelloBoard.board[cell_x//50][cell_y//50] == 0:
                    #print("Made it through the is it available slot check")
                    # this would be where to check if the move is possible
                    if (othelloBoard.Move([cell_x//50, cell_y//50])):
                        #print("Made it though the move stage")
                        othelloBoard.board[cell_x // 50][cell_y // 50] = othelloBoard.player
                        othelloBoard.player*=-1
                        # eventually will need to swtich around the storage so that i can not have to iterate twice
                        AvailableSpacesCounter=0
                        for i in range(8):
                            for j in range(8):
                                if (othelloBoard.board[i][j] == 0):
                                    if othelloBoard.IsSquarePlayable([i,j]):
                                        othelloBoard.board[i][j] = 2
                                        AvailableSpacesCounter+=1
                                if (othelloBoard.board[i][j] == 2):
                                    if not(othelloBoard.IsSquarePlayable([i,j])):
                                        othelloBoard.board[i][j]=0
                                    else:
                                        AvailableSpacesCounter+=1
                        if AvailableSpacesCounter==0:
                            othelloBoard.player*=-1
                            AvailableSpacesCounter2=0
                            for i in range(8):
                                for j in range(8):
                                    if (othelloBoard.board[i][j] == 0):
                                        if othelloBoard.IsSquarePlayable([i,j]):
                                            othelloBoard.board[i][j] = 2
                                            AvailableSpacesCounter2+=1
                                    if (othelloBoard.board[i][j] == 2):
                                        if not(othelloBoard.IsSquarePlayable([i,j])):
                                            othelloBoard.board[i][j]=0
                                        else:
                                            AvailableSpacesCounter2+=1
                            if AvailableSpacesCounter2 == 0:
                                print("Game Over!")
                        
        # Fill the background with white#screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
