white_tile_address = 'resources/image/white_tile.jpg'
black_tile_address = 'resources/image/black_tile.jpg'
board_address='resources/image/board.PNG'
easy_address='resources/image/easy.PNG'
normal_address='resources/image/normal.PNG'
hard_address='resources/image/hard.PNG'

BACKGROUNDCOLOR = (255, 255, 255)
FPS = 40
CELLWIDTH = 50
CELLHEIGHT = 50
PIECEWIDTH = 47
PIECEHEIGHT = 47
BOARDX = 23
BOARDY = 32

BLACK = (255, 255, 255)
BLUE = (0, 0, 255)


import pygame,sys,random
#导入pygame库
from pygame.locals import *
#导入一些常用的函数和常量
 


#This function checks if the position is in the bound
def inBound(n, row, col):
    if row>n-1 or row<0 or col>n-1 or col<0:
        return False
    return True

#This function finds the opposite colour
def opp(colour):
    if colour == 'W':
        return 'B'
    else:
        return 'W'

#This function checks if a postion is valid in one direction:
def validInDirection(board, n, row, col, colour, rowDir, colDir):
    currentRow = row
    currentCol = col
    count = 0
    oppColour = opp(colour)
    while inBound(n, currentRow+rowDir, currentCol+colDir):
        currentRow+=rowDir
        currentCol+=colDir
        if board[currentRow][currentCol] == oppColour:
            count += 1
        elif board[currentRow][currentCol] == colour:
            if count>0:
                return True
            else:
                return False
        else:
            return False

#This function check if a postion is a valid postion:
def validPosition(board, n, row, col, colour):
    if (not inBound(n, row, col)) or board[row][col] != 'U':
        return False
    else:
        for i in range(-1,2):
            for j in range(-1,2):
                if i != 0 or j != 0:
                    if validInDirection(board, n, row, col, colour, i, j):
                        return True
        return False

#This function print the game board
def printBoard(board, n):
    print(" ",end=" ")
    for x in range(n):
        print(x, end=" ")
    print("\n", end="")
    for i in range(n):
        print(i, end=" ")
        for j in range(n):
            print(board[i][j], end=" ")
        print("\n", end="")

#This function make a move on the board
def makeAMove(board, n, row, col, colour):
    if (not inBound(n, row, col)) or board[row][col] != 'U':
        return
    else:
        for i in range(-1,2):
            for j in range(-1,2):
                if i != 0 or j != 0:
                    if validInDirection(board, n, row, col, colour, i, j):
                        count=1
                        while board[row+count*i][col+count*j] != colour and inBound(n,row+count*i,col+count*j):
                            board[row+count*i][col+count*j] = colour
                            count += 1
        board[row][col]=colour
        return


#This functon calculate he number of tiles to change for a certain postion
def positionScore(board, n, row, col, colour):
    tiles=0
    if not validPosition(board, n, row, col ,colour):
        return tiles
    else:
        for i in range(-1,2):
            for j in range(-1,2):
                if i != 0 or j != 0:
                    if validInDirection(board, n, row, col, colour, i, j):
                        count = 1
                        while board[row+count*i][col+count*j] != colour and inBound(n,row+count*i,col+count*j):
                            count += 1
                            tiles += 1
        return tiles


#This function formats the scoreBoard
def score(scoreBoard, n, colour):
    for i in range(n):
        for j in range(n):
            scoreBoard[i][j]=positionScore(board,n,i,j,colour)
    return

#This function checks if there is a valid move for a certain colour
def validMoveExist(board, n, colour):
    for i in range(n):
        for j in range(n):
            if validPosition(board,n,i,j,colour):
                return True
    return False

#This function find a move based on score
def findScoreMove(board, scoreBoard, n, colour):
    if not validMoveExist(board,n,colour):
        return 
    else:
        max = 0
        row = -1
        col = -1
        for i in range(n):
            for j in range(n):
                if scoreBoard[i][j]>max:
                    max = scoreBoard[i][j]
                    row = i
                    col = j
        return row,col





# Main part
#n = int(input("Enter the size of the board: "))
n=8

board = [['U' for j in range(n)] for i in range(n)]
board[n//2-1][n//2-1] = 'W'
board[n//2-1][n//2] = 'B'
board[n//2][n//2-1] = 'B'
board[n//2][n//2] = 'W'
printBoard(board, n)

#Board value
value = [[0 for j in range(n)] for i in range(n)]
value[0][0]=90
value[0][1]=-60
value[1][0]=-60
value[1][1]=-80
for i in range(2,4):
    value[i][0]=10
    value[i][1]=5
    for j in range(2,4):
        value[0][j]=10;
        value[1][j]=5;
        value[i][j]=1;
for k in range(0,4):
    for l in range(0,4):
        value[k][n-l-1]=value[k][l]
        value[n-k-1][l]=value[k][l]
        value[n-k-1][n-l-1]=value[k][l]

#中等难度函数
def stablePosition(board, n, colour, row, col):
    if not validPosition(board,n,row,col,colour):
        return False
    if((row==0 and col==0)or(row==0 and col==0+n-1)or(row==0+n-1 and col==0)or(row==0+n-1 and col==0+n-1)):
        return True
    else:
        if(row!=0 or row!=0+n-1 or col!=0 or col!=0+n-1):
            return False
        for i in range(0,n):
            if((row==0 and board[0][i]!=colour)or(row==0+n-1 and board[n-1][i]!=colour)or(col==0 and board[i][0]!=colour)or(row==0 and board[n-1][i]!=colour)):
                return False
        return True

def findValueMove(board, scoreBoard, n, colour):
    if not validMoveExist(board,n,colour):
        return 
    else:
        max = -999
        row = -1
        col = -1
        for i in range(n):
            for j in range(n):
                if stablePosition(board,n,colour,i,j):
                    return i,j
                if value[i][j]>max and validPosition(board,n,i,j,colour):
                    max = value[i][j]
                    row = i
                    col = j
        return row,col

#高级难度函数
def computeMobility(board,n, colour):
    mobility=0;
    for i in range(n):
        for j in range(n):
            for deltaRow in range (-1,2):
                for deltaCol in range(-1,2):
                    if(deltaRow!=0 and deltaCol!=0):
                        if(validInDirection(board, n, i,j, colour, deltaRow, deltaCol)==True):
                            mobility+=1
    return mobility

def copyBoard(board, newBoard,n):
    for i in range(n):
        for j in range(n):
            newBoard[i][j]=board[i][j]

def findBestMove(board,scoreBoard,n,colour):
    row = -1
    col = -1
    WORST=-999
    maxRow=-1
    maxCol=-1
    maxOppRow=-1
    maxOppCol=-1
    oppColour=-1
    myMaxValueRow=-1
    myMaxValueCol=-1

    valueWeight=3
    scoreWeight=2
    mobilityWeight=4

    oppColour=opp(colour)
    maxPositionBenifit=-1000
    oppMobilityBoard=[[0 for i in range(n)] for j in range(n)]
    myMobilityBoard=[[0 for i in range(n)] for j in range(n)]
    positionBenifit=[[WORST for i in range(n)] for j in range(n)]
    oppMax=[[-100 for i in range(n)] for j in range(n)]
    
    for i in range(n):
        for j in range(n):
            if validPosition(board,n,i,j,colour):
                if(stablePosition(board,n,colour,i,j)):
                    row=i
                    col=j
                    return row,col
                else:
                    board2=[['C' for i in range(n)] for j in range(n)]
                    copyBoard(board,board2,n)
                    makeAMove(board2,n,i,j,colour)
                    oppMobilityBoard[i][j]=computeMobility(board2,n,oppColour)

                    board3=[['C' for i in range(n)] for j in range(n)]
                    copyBoard(board2,board3,n)
                    board4=[['C' for i in range(n)] for j in range(n)]
                    copyBoard(board2,board4,n)
                        
                    if(validMoveExist(board2,n,oppColour)):
                        oppMoveBenefit=-999
                        for x in range(n):
                            for y in range(n):
                                copyBoard(board2,board3,n)
                                #find the opponent postion where results in max benefit for him
                                if validPosition(board3,n,x,y,oppColour):
                                    makeAMove(board3,n,x,y,oppColour)  
                                    if(oppMoveBenefit<valueWeight*value[x][y]-mobilityWeight*computeMobility(board3,n,colour)):
                                        oppMoveBenefit=valueWeight*value[x][y]-mobilityWeight*computeMobility(board3,n,colour)
                                        maxOppRow=x;
                                        maxOppCol=y;

                        for x in range(n):
                            for y in range(n):
                                copyBoard(board2,board3,n)
                                if validPosition(board3,n,x,y,oppColour): #check the number of my tiles
                                    makeAMove(board3,n,x,y,oppColour);
                                    myTiles=0;
                                    for p in range(n):
                                        for q in range(n):
                                            if(board3[p][q]==colour):
                                                myTiles+=1

                                    if(myTiles==0):#avoid the positon where AI has no tiles(ie. game ends)
                                        positionBenifit[i][j]=-999;

                                    else:#compute my mobility after opponent move
                                        makeAMove(board4,n,maxOppRow,maxOppCol,oppColour);
                                        oppMax[i][j]=value[maxOppRow][maxOppCol];
                                        myMobilityBoard[i][j]=computeMobility(board4,n,colour);
                                        if(validMoveExist(board4,n,colour)):#if I can lie a tile
                                            myMaxValueRow,myMaxValueCol = findValueMove(board4,scoreBoard,n,colour)
                                            positionBenifit[i][j]=mobilityWeight*myMobilityBoard[i][j]+scoreWeight*scoreBoard[i][j]+valueWeight*(value[i][j]
                                            +value[myMaxValueRow][myMaxValueCol])-mobilityWeight*oppMobilityBoard[i][j]
                                                #consider: my mobility for next turn, tiles I flip, value of the my postion this turn and next turn, opponent's mobility
                                            
                                        else:#avoid the postion where I have no valid move for next turn
                                            positionBenifit[i][j]=-999

                    else:#if opponent has no move, lie a tile
                        positionBenifit[i][j]=999

                    #avoid where opp can obtain a stable position
                    for k in range(n):
                        for l in range(n):
                            if validPosition(board2,n,k,l,oppColour) and stablePosition(board2,n,oppColour,k,l):
                                positionBenifit[i][j]=-999

                    #find the position of max benifit
                    if(positionBenifit[i][j]>maxPositionBenifit and validPosition(board,n,i,j,colour)):
                        maxPositionBenifit = positionBenifit[i][j]
                        maxRow=i
                        maxCol=j
                        row=maxRow
                        col=maxCol
    print(positionBenifit)
    return row,col


# 退出
def terminate():
    pygame.quit()
    sys.exit()


# 初始化
pygame.init()
mainClock = pygame.time.Clock()

boardImage = pygame.image.load(board_address)
boardRect = boardImage.get_rect()
blackImage = pygame.image.load(black_tile_address)
blackRect = blackImage.get_rect()
whiteImage = pygame.image.load(white_tile_address)
whiteRect = whiteImage.get_rect()
#导入棋盘和棋子

easyImage = pygame.image.load(easy_address)
easyRect = easyImage.get_rect()
normalImage = pygame.image.load(normal_address)
normalRect = normalImage.get_rect()
hardImage = pygame.image.load(hard_address)
hardRect = hardImage.get_rect()

#导入其他图片

screen = pygame.display.set_mode((boardRect.width, boardRect.height))
#创建了一个窗口
pygame.display.set_caption("reversi")
#设置窗口标题

# 设置窗口
windowSurface = pygame.display.set_mode((boardRect.width, boardRect.height))

def boardDisplay():
    for x in range(n):
            for y in range(n):
                rectDst = pygame.Rect(BOARDX+x*CELLWIDTH+2, BOARDY+y*CELLHEIGHT+2, PIECEWIDTH, PIECEHEIGHT)
                if board[y][x] == 'B':
                    windowSurface.blit(blackImage, rectDst, blackRect)
                elif board[y][x] == 'W':
                    windowSurface.blit(whiteImage, rectDst, whiteRect)
    pygame.display.update()


# 退出
def terminate():
    pygame.quit()
    sys.exit()


# 初始化
pygame.init()
mainClock = pygame.time.Clock()
 
screen = pygame.display.set_mode((boardRect.width, boardRect.height))
#创建了一个窗口
pygame.display.set_caption("reversi")
#设置窗口标题

boardImage = pygame.image.load(board_address)
boardRect = boardImage.get_rect()
blackImage = pygame.image.load(black_tile_address)
blackRect = blackImage.get_rect()
whiteImage = pygame.image.load(white_tile_address)
whiteRect = whiteImage.get_rect()

basicFont = pygame.font.SysFont(None, 28)
gameoverStr = 'Game Over White:Black '
#导入棋盘和棋子

# 设置窗口
windowSurface = pygame.display.set_mode((boardRect.width, boardRect.height))

boardDisplay()


currentColour = 'B'
end = False
result = False
computerColour=''

#选择难度
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

    windowSurface.fill(BACKGROUNDCOLOR)
    outputStr = "Choose a level: "
    text = basicFont.render(outputStr, False, BLACK, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery
    windowSurface.blit(text, textRect)

    easyRectDst = pygame.Rect(224-175,231+25,100, 100)
    normalRectDst = pygame.Rect(224-50,231+20,100, 100)
    hardRectDst = pygame.Rect(224+75,231+20,100, 100)
    windowSurface.blit(easyImage, easyRectDst, easyRect)
    windowSurface.blit(normalImage, normalRectDst, normalRect)
    windowSurface.blit(hardImage, hardRectDst, hardRect)

    pygame.display.update()

    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        x,y = pygame.mouse.get_pos()
        if x >= 224-175 and x <= 224-75 and y>=231+25 and y<=231+125:
            findAMove=findScoreMove
            print("easy")
            break
        elif x >= 224-50 and x <= 224+50 and y>=231+20 and y<=231+120:
            findAMove=findValueMove
            print("normal")
            break
        elif x >= 224+75 and x <= 224+175 and y>=231+20 and y<=231+120:
            findAMove=findBestMove
            print("hard")
            break


#选择颜色

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

    windowSurface.fill(BACKGROUNDCOLOR)
    outputStr = "Choose your Colour: (Black goes the first)"
    text = basicFont.render(outputStr, False, BLACK, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery
    windowSurface.blit(text, textRect)

    wRectDst = pygame.Rect(224+CELLWIDTH,231+CELLHEIGHT,PIECEWIDTH, PIECEHEIGHT)
    bRectDst = pygame.Rect(224-2*CELLWIDTH,231+CELLHEIGHT,PIECEWIDTH, PIECEHEIGHT)
    windowSurface.blit(whiteImage, wRectDst, whiteRect)
    windowSurface.blit(blackImage, bRectDst, blackRect)

    pygame.display.update()

    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        x,y = pygame.mouse.get_pos()
        if x >= 224-2*CELLWIDTH and x <= 224-CELLWIDTH:
            computerColour = 'W'
            break
        elif x >= 224+CELLWIDTH and x <= 224+2*CELLWIDTH:
            computerColour = 'B'
            break

userColour = opp(computerColour)
Wt=0
Bt=0

# 游戏主循环

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

    if (not validMoveExist(board, n,'B')) and (not validMoveExist(board, n,'W')):
        end = True
    else:
        if currentColour == computerColour and not end:
            if validMoveExist(board,n,computerColour):
                scoreBoard = [[0 for j in range(n)] for i in range(n)]
                score(scoreBoard, n, computerColour)
                row,col=findAMove(board,scoreBoard,n,computerColour)
                makeAMove(board,n,row,col,computerColour)
                print("Computer(%s) makes a move at %d %d" %(computerColour,row,col))
                currentColour = opp(currentColour)
                printBoard(board,n)
            else:
                stop = False
                while not stop:
                    for event in pygame.event.get():
                        if event2.type == QUIT:
                            sys.exit()
                    outputStr = "No valid Move for computer, click to continue"
                    text = basicFont.render(outputStr, False, BLACK, BLUE)
                    textRect = text.get_rect()
                    textRect.centerx = windowSurface.get_rect().centerx
                    textRect.centery = windowSurface.get_rect().centery
                    windowSurface.blit(text, textRect)
                    pygame.display.update()

                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        stop = True
                        boardDisplay()

                print("No valid move for computer(%s)" %(computerColour))
                currentColour = opp(currentColour)
        elif currentColour == userColour and not end:
            if validMoveExist(board,n,userColour):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x,y = pygame.mouse.get_pos()
                    col = int((x-BOARDX)/CELLWIDTH)
                    row = int((y-BOARDY)/CELLHEIGHT)
                    if validPosition(board,n,row,col,userColour):
                        makeAMove(board,n,row,col,userColour)
                        currentColour = opp(currentColour)
                        printBoard(board,n)
            else:
                stop = False
                while not stop:
                    for event in pygame.event.get():
                        if event2.type == QUIT:
                            sys.exit()
                    
                    outputStr = "No valid Move for you, click to continue"
                    text = basicFont.render(outputStr, False, BLACK, BLUE)
                    textRect = text.get_rect()
                    textRect.centerx = windowSurface.get_rect().centerx
                    textRect.centery = windowSurface.get_rect().centery
                    windowSurface.blit(text, textRect)
                    pygame.display.update()

                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        stop = True
                        boardDisplay()

                print("No valid move for you(%s)" %(userColour))
                currentColour = opp(currentColour)


    windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(boardImage, boardRect, boardRect)
    boardDisplay()
    
    if end == True and result == False:
        wtiles = 0
        btiles = 0
        for i in range(n):
            for j in range(n):
                if board[i][j] == 'B':
                    btiles+=1
                if board[i][j] == 'W':
                    wtiles+=1
        Wt=wtiles
        Bt=btiles
        if wtiles>btiles:
            print("W player wins")
        elif wtiles<btiles:
            print("B player wins")
        else:
            print("Draw")
        result = True

    if result == True:
        outputStr = gameoverStr + str(Wt) + ":" + str(Bt)
        text = basicFont.render(outputStr, True, BLACK, BLUE)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = windowSurface.get_rect().centery
        windowSurface.blit(text, textRect)
        pygame.display.update()
        

    pygame.display.update()
    mainClock.tick(FPS)

