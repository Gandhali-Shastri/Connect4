#Gandhali Shastri

import sys
import os.path
from MaxConnect4Game import *

def oneMoveGame(currentGame, depth, game_mode):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        if (currentGame.player1Score > currentGame.player2Score):
            print 'Player 1 is the winner'
        else:
            print 'Player 2 is the winner'
        sys.exit(0)

    currentGame.aiPlay(depth, game_mode) # Make a move (only random is implemented)

    print 'Game state after move:'
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player1 = %d, Player2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()


def interactiveGame(currentGame, c, h, depth, game_mode):
    while(True):
        if currentGame.pieceCount == 42:    # Is the board full already?
            print 'BOARD FULL\n\nGame Over!\n'
            currentGame.countScore()
            print('Score: Player1 = %d, Player2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
            if (currentGame.player1Score > currentGame.player2Score):
                print 'Player 1 is the winner'
            else:
                print 'Player 2 is the winner'
            sys.exit(0)

        elif currentGame.currentTurn == c:
            print 'Computer turn is %d'%(currentGame.currentTurn)
            currentGame.aiPlay(depth, game_mode)
            currentGame.gameFile = open('computer.txt', 'w')
            currentGame.printGameBoardToFile()
            currentGame.gameFile.close()
            currentGame.checkPieceCount()

            print 'Game state after Computer player move:'
            currentGame.printGameBoard()
            currentGame.countScore()
            print('Score: Player1 = %d, Player2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
        else:
            currentGame.humanPlay()
            print 'Game state after Human player move:'
            currentGame.printGameBoard()
            currentGame.countScore()
            print('Score: Player1 = %d, Player2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/h-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]
    depth = int(argv[4])
    h = 0
    c = 0
    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game
    
    #Game mode is Interactive and input file is given.
    if not inFile == '' and os.path.isfile(inFile):
        # Try to open the input file
        try:
            currentGame.gameFile = open(inFile, 'r')
        except IOError:
            sys.exit("\nError opening input file.\nCheck file name.\n")

        # Read the initial game state from the file and save in a 2D list
        file_lines = currentGame.gameFile.readlines()
        currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
        currentGame.currentTurn = int(file_lines[-1][0])
        currentGame.playerType = currentGame.currentTurn
        currentGame.gameFile.close()
    
    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode == 'interactive':
        if  argv[3] == 'computer-next':
            c = currentGame.currentTurn
            if c  == 1:
                h = 2
            else:
                h = 1
        else:
            h = currentGame.currentTurn
            if h == 1:
                c = 2
            else:
                c = 1
        currentGame.playerType = c
        interactiveGame(currentGame, c, h, depth, game_mode) # Be sure to pass whatever else you need from the command line
    else: 
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame, depth, game_mode) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)

