import pygame , random
BLACK = (0,0,0)
WHITE = (255,255,255)
pi =3.14

class piece:
    def __init__(self,cent,rad):
        self.rad = rad
        self.player = 0
        self.cent = cent
    def update(self,cent,rad,player):
        self.cent , self.rad , self.player = cent , rad , player
    def draw(self,scr):
        if self.player == 1:
            pygame.draw.circle(scr,WHITE,self.cent,self.rad)
        if self.player == -1:
            pygame.draw.circle(scr,BLACK,self.cent,self.rad)
        if self.player == 2:
            pygame.draw.circle(scr,WHITE,self.cent,round(self.rad/pi))
        if self.player == -2:
            pygame.draw.circle(scr,BLACK,self.cent,round(self.rad/pi))

class Tile:
    def __init__(self,colour,rect,cent,boxSize):
        rad=round((boxSize)*0.75)
        rad = rad//2
        self.Piece = piece(cent,rad)
        self.colour = colour
        self.rect = rect
    def update(self,rect,cent,boxSize):
        rad=round((boxSize)*0.75)
        rad = rad//2
        self.Piece.update(cent,rad,self.Piece.player)
        #self.colour = colour
        self.rect = rect
    def draw(self,scr):
        pygame.draw.rect(scr,self.colour,self.rect)
        self.Piece.draw(scr)
    def __repr__(self):
        print(str(self.Piece.player))


class board:
    def __init__(self,sx):


        #print(self.Tiles)
        self.gap = 3
        self.boxSize = (sx-9*self.gap)//8
        self.diff = (sx-(8*self.boxSize))/2
        self.colour1 = (10,110,11)
        self.colour2 = (7,138,6)
        self.Tiles = []
        for x in range(0,8):
            self.Tiles.append([])
            for y in range(0,8):

                rect = (self.diff+x*self.boxSize,self.diff+y*self.boxSize,self.boxSize-self.gap,self.boxSize-self.gap)
                cent = (int(2*(self.diff+x*self.boxSize)+self.boxSize-self.gap)//2,int(2*(self.diff+y*self.boxSize)+self.boxSize-self.gap)//2)
                if (x+y) %2 == 0 :
                    aTile = Tile(self.colour1,rect,cent,self.boxSize)
                else:
                    aTile = Tile(self.colour2,rect,cent,self.boxSize)
                self.Tiles[x].append(aTile)
        #self.piece = piece(self.boxSize,cent)
    def changeSize(self,sx,sy):
        if sx > sy:
            sx = sy
        self.gap = 3
        self.boxSize = (sx-9*self.gap)//8
        self.diff = (sx-(8*self.boxSize))/2
        self.colour1 = (10,110,11)
        self.colour2 = (7,138,6)
        self.update()
    def update(self):
        for x in range(0,8):
            for y in range(0,8):

                rect = (self.diff+x*self.boxSize,self.diff+y*self.boxSize,self.boxSize-self.gap,self.boxSize-self.gap)
                cent = (int(2*(self.diff+x*self.boxSize)+self.boxSize-self.gap)//2,int(2*(self.diff+y*self.boxSize)+self.boxSize-self.gap)//2)
                self.Tiles[x][y].update(rect,cent,self.boxSize)

    def draw(self,scr):
        for row in self.Tiles:
            for item in row:
                item.draw(scr)


    def getBox(self,xpos,ypos,ply,Moves):
        xpos = xpos - self.diff
        ypos = ypos - self.diff
        x = int(xpos//self.boxSize)
        y = int(ypos//self.boxSize)
        if (x,y) in Moves:
            if 0 <= x <= 7 and 0 <= y <= 7:
                self.findLine((x,y),ply)
                self.Tiles[x][y].Piece.player =ply
                return True
        return False
    def findLine(self,move,ply):
        vectors = [(0,1),(1,0),(0,-1),(-1,0),(-1,-1),(-1,1),(1,-1),(1,1)]
        for item in vectors:
            tempTiles = []
            for rel in range(1,8):
                #print(relx)
                checksqx , checksqy = move[0]+rel*item[0] , move[1] +rel*item[1]

                if checksqx == 8 or checksqy ==8 or checksqx == -1 or checksqy == -1:
                    break
                #print(checksqx,checksqy)
                currentTile = self.Tiles[checksqx][checksqy].Piece.player
                if currentTile == 0 or currentTile ==2 or currentTile == -2:
                    break
                if currentTile == -ply:
                    tempTiles.append((checksqx,checksqy))
                if currentTile ==ply:
                    for temp in tempTiles:
                        self.Tiles[temp[0]][temp[1]].Piece.player = ply



        return False

    def addStartPieces(self):
        cord = [(3,3),(3,4),(4,4),(4,3)]
        ply = 1
        for item in cord:
            self.Tiles[item[0]][item[1]].Piece.player =ply
            ply = -ply

class Othello:
    def __init__(self,sizex,sizey):
        pygame.init()
        self.done = False
        self.sizex , self.sizey = sizex,sizey
        self.theBoard = board(sizex)
        self.theBoard.addStartPieces()
        self.currentPlayer = -1
        self.Main()
    def Main(self):
        WINDOW_SIZE = [self.sizex, self.sizey]
        width , height = self.sizex , self.sizey
        fps = 5
        t1 , t2 = 1000, 1000
        self.screen = pygame.display.set_mode(WINDOW_SIZE,pygame.RESIZABLE )
        pygame.display.set_caption("Risk Game")
        self.clock = pygame.time.Clock()
        thisMoves=self.legalMoves()
        resize = None
        self.theBoard.draw(self.screen)
        pygame.display.flip()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN :
                    fps = 5
                    pos = pygame.mouse.get_pos()
                    if self.theBoard.getBox(pos[0],pos[1],self.currentPlayer,thisMoves):

                        self.currentPlayer = -self.currentPlayer
                        thisMoves=self.legalMoves()
                        if len(thisMoves) == 0:
                            self.currentPlayer = -self.currentPlayer
                            thisMoves=self.legalMoves()
                        self.theBoard.draw(self.screen)
                        pygame.display.flip()
                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    #width , height = width -self.sizex, height - self.sizey
                    if width < 400:
                        width = 400
                    if height < 400:
                        height = 400

                    self.screen.fill(BLACK)
                    self.theBoard.changeSize(width,height)
                    self.theBoard.draw(self.screen)
                    pygame.display.flip()
                    fps = 60


            self.clock.tick(fps)
            #fps =5
            #pygame.display.flip()
        pygame.quit()

    def legalMoves(self):
        Moves = []
        currentBoard = self.theBoard.Tiles
        for x in range(0,8):
            #print(self.theBoard.Tiles[x][0])
            for y in range(0,8):
                if currentBoard[x][y].Piece.player ==2 or currentBoard[x][y].Piece.player ==-2:
                    currentBoard[x][y].Piece.player = 0
                    #print(x,y)
                if currentBoard[x][y].Piece.player == 0 or currentBoard[x][y].Piece.player ==2 or currentBoard[x][y].Piece.player ==-2:
                    move = (x,y)
                    if self.isLegal(move,currentBoard):
                        Moves.append(move)
        for move in Moves:
            currentBoard[move[0]][move[1]].Piece.player = self.currentPlayer*2
        return Moves
    def isLegal(self,move,board):

        vectors = [(0,1),(1,0),(0,-1),(-1,0),(-1,-1),(-1,1),(1,-1),(1,1)]
        for item in vectors:
            firstVal = None
            for rel in range(1,8):
                #print(relx)
                checksqx , checksqy = move[0]+rel*item[0] , move[1] +rel*item[1]
                if checksqx == 8 or checksqy ==8 or checksqx == -1 or checksqy == -1:
                    break
                if firstVal == -self.currentPlayer and (board[checksqx][checksqy].Piece.player == self.currentPlayer):
                    return True
                if board[checksqx][checksqy].Piece.player == 0 or board[checksqx][checksqy].Piece.player == 2 or board[checksqx][checksqy].Piece.player ==-2:
                    break
                if firstVal == None:
                    firstVal = board[checksqx][checksqy].Piece.player
                    if firstVal != -self.currentPlayer:
                        break
        return False


    def draw(self):
        #self.screen.fill(BLACK)
        self.theBoard.draw(self.screen)
        pygame.display.flip()

test = Othello(1000,1000)
