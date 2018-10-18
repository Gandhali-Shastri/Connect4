#References:
#http://web.mit.edu/sp.268/www/2010/connectFourSlides.pdf
#http://www.cs.virginia.edu/~evans/poker/wp-content/uploads/2011/01/class2.pptx
#wiki alpha beta pseudocode

from copy import deepcopy
import sys

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.playerType = 1
        self.alpha =  -1000000
        self.beta = 1000000

    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1
    
    # The AI section. Currently plays randomly.
    def aiPlay(self, depth, game_mode):
        alphaBeta = self.alphaBetaPruning(depth, game_mode)
        self.gameBoard = deepcopy(alphaBeta.gameBoard)
        self.changeTurn()
        #print 'aI turn chnaged'
        if game_mode == 'interactive':
            self.gameFile = open('computer.txt', 'w')
            self.printGameBoardToFile()
            self.gameFile.close()

    #human player
    def humanPlay(self):
        print 'Human turn is %d'%(self.currentTurn)
        column = input("Please enter the column where you want to play: ")
        if column > 0 and column < 8 :
            result = self.playPiece(column - 1)
            while not result:
                print 'That was not a valid move. Try again.'
                column = input("Please enter valid column where you want to play: ")
                result = self.playPiece(column - 1)
        elif  column >= 8 or column <= 0:
            while column >= 8 or column <= 0 :
                print ('Enter a column between 1 and 7')
                column = input("Please enter valid column where you want to play: ")
                result = self.playPiece(column - 1)
    
        self.changeTurn()
        self.gameFile = open('human.txt', 'w')
        self.printGameBoardToFile()
        self.gameFile.close()
        self.checkPieceCount()

    def changeTurn(self):  
        if self.currentTurn == 1:
            self.currentTurn = 2
        else:
            self.currentTurn = 1

    #check whether the next move is valid or not.
    def validMoves(self, column):
        move = maxConnect4Game()
        move.gameBoard = deepcopy(self.gameBoard)
        move.currentTurn = deepcopy(self.currentTurn)
        move.playerType =  deepcopy(self.playerType)
        result = move.playPiece(column)
        if result:          
            move.changeTurn()
            #print 'turn chnaged'
            move.checkPieceCount()
            move.countScore()
            return move

    #alpha beta with pruning and depth limit
    def alphaBetaPruning(self, depth, game_mode):
        if game_mode == 'interactive':
            validMove = self
            
            self.checkPieceCount()
            if not self.gameBoard[5][3]:
                validMove = self.validMoves(3)
                return validMove
            elif not self.gameBoard[5][2]:
                validMove = self.validMoves(2)
                return validMove
            elif not self.gameBoard[5][4]:
                validMove = self.validMoves(4)
                return validMove

        v = -1000000
        for column in range(7):
            nextValidMove = self.validMoves(column)
            if not nextValidMove:
                continue
            u = nextValidMove.minValue(1,depth)
            if u  > v:
                v =  u
                self.alpha = max(self.alpha, v)
                validMove = deepcopy(nextValidMove)
        return validMove

    def minValue(self, d, depth):
        if self.pieceCount == 42:
            if (self.playerType == 1) and (self.player1Score > self.player2Score):
                v = 1   #max is winning
            elif (self.playerType == 1) and (self.player1Score < self.player2Score):
                v = -1  #max is losing
            elif (self.playerType == 2) and (self.player1Score < self.player2Score):
                v = 1   #max is winning
            elif(self.playerType == 2) and (self.player1Score > self.player2Score):
                v = -1  #max is losing
            else:
                v = 0   #draw
        else:
            v = 2   #continue

        if v < 2:
            return v
        if d == depth:  #depth limit reached
            return self.eval()

        v = 1000000
        for i in range(7):
            nextValidMove = self.validMoves(i)
            if not nextValidMove:
                continue
            u = nextValidMove.maxValue(d +1,depth)
            if u  < v:
                v =  u
            if v <= self.alpha:
                return v
            self.beta = min(self.beta, v)
        return v

    def maxValue(self, d, depth):


        if self.pieceCount == 42:
            if (self.playerType == 1) and (self.player1Score > self.player2Score):
                v = 1
            elif (self.playerType == 1) and (self.player1Score < self.player2Score):
                v = -1
            elif (self.playerType == 2) and (self.player1Score < self.player2Score):
                v = 1
            elif(self.playerType == 2) and (self.player1Score > self.player2Score):
                v = -1
            else:
                v =0
        else:
            v = 2

        if v < 2:
            return v
        if d == depth:
            return self.eval()

        v = -1000000
        for i in range(7):
            nextValidMove = self.validMoves(i)
            if not nextValidMove:
                continue
            u = nextValidMove.minValue(d + 1, depth)
            if u  > v:
                v =  u
            if v >= self.beta:
                return v
            self.alpha = max(self.alpha, v)
        return v

    def eval(self):
        
        self.countScore()
        if self.playerType == 1:
            maxPlayer = 1
            minPlayer = 2
            max4Connect = self.player1Score
            min4Connect = self.player2Score
        else:
            maxPlayer = 2
            minPlayer = 1
            max4Connect = self.player2Score
            min4Connect = self.player1Score

        max3Connect = self.checkForConnect(maxPlayer, 3)
        max2Connect = self.checkForConnect(maxPlayer, 2)
        min3Connect = self.checkForConnect(minPlayer, 3)
        min2Connect = self.checkForConnect(minPlayer, 2)
        
        maxValue = (max4Connect * 1)+(max3Connect * 0.6) + (max2Connect * 0.2)
        minValue = (min4Connect * 1)+(min3Connect * 0.6) + (min2Connect * 0.2)
        finalValue= (maxValue - minValue)
        return finalValue

    def checkForConnect(self, player, connect):
        count= 0
        for i in range(6):
            for j in range(7):
                    count += self.diagonalConnect(i, j, player, connect)

        count += self.verticalConnect(player, connect)
        count += self.horizontalConnect( player, connect)
        return count

    def verticalConnect(self,  player, connect):
        cont = 0
        for j in range(7):
            if connect == 3:
                if (self.gameBoard[0][j] == player and self.gameBoard[1][j] == player and
                        self.gameBoard[2][j] == player):
                    cont += 1
                if (self.gameBoard[1][j] == player and self.gameBoard[2][j] == player and
                            self.gameBoard[3][j] == player):
                    cont += 1
                if (self.gameBoard[2][j] == player and self.gameBoard[3][j] == player and
                            self.gameBoard[4][j] == player):
                    cont += 1
                if (self.gameBoard[3][j] == player and self.gameBoard[4][j] == player and
                                    self.gameBoard[5][j] == player):
                    cont += 1
            elif connect == 2:
                if (self.gameBoard[0][j] == player and self.gameBoard[1][j] == player):
                    cont += 1
                if (self.gameBoard[1][j] == player and self.gameBoard[2][j] == player):
                    cont += 1
                if (self.gameBoard[2][j] == player and self.gameBoard[3][j] == player):
                    cont += 1
                if (self.gameBoard[3][j] == player and self.gameBoard[4][j] == player):
                    cont += 1
                if (self.gameBoard[4][j] == player and self.gameBoard[5][j] == player):
                    cont += 1
        return cont

    def horizontalConnect(self, player, connect):
        cont = 0
        for row in self.gameBoard:
            if connect == 3:
                if row[0:3] == [player]*3:
                    cont += 1
                if row[1:4] == [player]*3:
                    cont += 1
                if row[2:5] == [player]*3:
                    cont += 1
                if row[3:6] == [player]*3:
                    cont += 1
                if row[4:7] == [player]*3:
                    cont += 1
            elif connect == 2:
                if row[0:2] == [player]*2:
                        cont += 1
                if row[1:3] == [player]*2:
                        cont += 1
                if row[2:4] == [player]*2:
                        cont += 1
                if row[3:5] == [player]*2:
                        cont += 1
                if row[4:6] == [player]*2:
                        cont += 1
                if row[5:7] == [player]*2:
                        cont += 1
        return cont

    def diagonalConnect(self, row, col, player, connect):
        cont =0
        total = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.gameBoard[i][j] == player and self.gameBoard[row][col] == player:
                cont += 1
            else:
                break
            j += 1

        if cont >= connect:
            total += 1

        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.gameBoard[i][j] == player and self.gameBoard[row][col] == player:
                cont += 1
            else:
                break
            j += 1

        if cont >= connect:
            total += 1

        return total    

    def countScore(self):
        self.player1Score = 0;
        self.player2Score = 0;

        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
