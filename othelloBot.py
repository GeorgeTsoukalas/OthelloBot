import pygame
import copy
import math
class OthelloBoard:
    def __init__(self, board, square_counts, player,empty_spaces):
        self.board=board
        self.player=player
        self.square_counts=square_counts
        self.empty_spaces=empty_spaces
        self.gameOverCounter = 0
    def heuristic1(self):
        if (self.square_counts[1]+self.square_counts[-1] == 64):
            if (self.square_counts[1] > self.square_counts[-1]):
                return 65 # higher than any possible eval number (for a white = machine controlled win)
            else:
                return -65
        return self.square_counts[1]-self.square_counts[-1] # this is an example so far, but it must depend on the player! (WE ASSUME MACHINE = WHITE)
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
        for square in self.empty_spaces:
            if self.IsSquarePlayable(square):
                PlayableSpaces.append(square[:]) #duplicating it just in case I don't know how python works - haha!
        if len(PlayableSpaces) == 0:
            return [[-1,-1]] # this indicates no move for the minimax tree
        return PlayableSpaces
    def Move(self, Square):
        #print("Move starting up")
        if self.IsSquarePlayable(Square):
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
            self.board[Square[0]][Square[1]]=self.player
            self.empty_spaces.remove(Square)
            self.player=self.player*-1
            AvailableSpacesCounter=0
            for i in self.empty_spaces:
                if (self.board[i[0]][i[1]] == 0):
                    if self.IsSquarePlayable(i):
                        self.board[i[0]][i[1]] = 2
                        AvailableSpacesCounter+=1
                if (self.board[i[0]][i[1]] == 2):
                    if not(self.IsSquarePlayable(i)):
                        self.board[i[0]][i[1]]=0
                    else:
                        AvailableSpacesCounter+=1
            if AvailableSpacesCounter==0 and self.gameOverCounter == 0: # need to change this
                self.gameOverCounter = 1 # if this is 1 and isvaialblespaces again returns no move then we know 
            elif AvailableSpacesCounter==0 and self.gameOverCounter == 1:
                self.gameOverCounter = 2
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
    def __init__(self,state,depth, value=0, parent=None):
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
        T=[0,0,0,0,0,0,0]
        while (len(L) > 0):
            Q=L.pop(0); # is this the correct order -> NEEDS TO BE QUEUE
            Available = Q.state.AvailableSquares()
            UnAllowed = []
            if [-1,-1] in Available:
                if Q.state.gameOverCounter == 0:
                    T[Q.depth+1]+=1
                    deepCopy = GameNode(copy.deepcopy(Q.state), Q.depth+1, 0, Q)
                    deepCopy.state.player*=-1
                    Q.addChild(deepCopy)
                else:
                    T[Q.depth+1]+=1
                    deepCopy = GameNode(copy.deepcopy(Q.state), Q.depth+1, 0, Q)
                    deepCopy.state.player*=-1
                    Q.addChild(deepCopy)
                    UnAllowed.append(deepCopy)
            else:
                for i in Q.state.AvailableSquares():
                    T[Q.depth+1]+=1
                    deepCopy = GameNode(copy.deepcopy(Q.state), Q.depth+1,0 ,Q)
                    deepCopy.state.Move(i)
                    #deepCopy.value=deepCopy.state.heuristic1()
                    Q.addChild(deepCopy)
            if Q.depth+1 < prescribedDepth: # so the entires will go 1 over the prescribed depth
                for i in [item for item in Q.children if item not in UnAllowed]:
                    L.append(i)
        print(T)
        # let's hope that this actually works thus far
        # might need a deep copy of Q when moved1
    def miniMaxReturnNextNode(self,node,depth,player):
        T=self.miniMax(node,depth,player)
        for i in node.children:
            if i.value == T:
                print(i.state.empty_spaces)
                print("Found one!")
                return i
    def miniMax(self, node,depth,player): # player = 1 for now
        if len(node.children)==0:
            return player*node.state.heuristic1() # opposite value for black
        else:
            if node.state.player == player:
                L=[]
                for state in node.children:
                    L.append(self.miniMax(state,depth,player))
                node.value = max(L)
                return max(L)
            else:
                L=[]
                for state in node.children:
                    L.append(self.miniMax(state,depth,player))
                node.value=min(L)
                return min(L)
    def getSuccessors(self,node):
        assert node is not None
        return node.children
    def isTerminal(self,node):
        assert node is not None
        return len(node.children)==0
    def getUtility(self,node):
        assert node is not None
        return node.value

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
prescribedDepth=2
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
    color = (50,220,50)
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
    draw_markers()
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
            clicked = False
            if (othelloBoard.player == -1): # this is the human controlled player
                game_tree = GameTree()
                game_tree.build_tree(copy.deepcopy(othelloBoard))
                F=game_tree.miniMaxReturnNextNode(game_tree.root, prescribedDepth, othelloBoard.player).state.empty_spaces
                bestMoveList = [item for item in othelloBoard.empty_spaces if item not in F]
                othelloBoard.Move(bestMoveList[0])
            elif (othelloBoard.player == 1): # this is machine controlled player - NEED SOME WAY TO WRITE MOVES WHERE YOU GET ANOTHER TURN, could keep a tracker of available spaces and havea lever for how much a free MOVE is worth.
                game_tree = GameTree()
                game_tree.build_tree(copy.deepcopy(othelloBoard))
                print(game_tree.miniMax(game_tree.root,prescribedDepth,othelloBoard.player))
                F=game_tree.miniMaxReturnNextNode(game_tree.root,prescribedDepth,othelloBoard.player).state.empty_spaces
                bestMoveList=[item for item in othelloBoard.empty_spaces if item not in F]
                print(othelloBoard.empty_spaces)
                print(game_tree.miniMaxReturnNextNode(game_tree.root, prescribedDepth,othelloBoard.player).state.empty_spaces)
                print(bestMoveList)
                othelloBoard.Move(bestMoveList[0]);
    pygame.display.flip()   
pygame.quit()
