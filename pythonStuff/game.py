import pygame as pg
import random

import chess
#from chess import Board as board

def loadImages(squareSize):
    #pieces = ["wB", "bB", "wN", "bN", "wR", "bR", "wP", "bP", "wK", "bK", "wQ", "bQ"]
    pieces = ["bP", "bN", "bR", "bB", "bQ", "bK", "wP", "wN", "wR", "wB", "wQ", "wK"]
    images = []
    for piece in pieces:
        #images.append(pg.image.load('assets/' + piece + '.png'))   #NOTE: figure out how to make python paths work and avoid working directory weirdness
        images.append(pg.image.load('pythonStuff/assets/' + piece + '.png'))
    for piece in range(len(images)):
        images[piece] = pg.transform.scale(images[piece], (squareSize,squareSize))
    return images


def drawBoard(squareSize, screen):
    #Fill board
    whiteSquare = 0xEEEED2
    blackSquare = 0x769656
    for i in range(8):
        for j in range(8):
            #Lol the things i do to avoid an if statement
            pg.draw.rect(screen, (whiteSquare-blackSquare) * ((i + j + 1) % 2) + blackSquare, pg.Rect(squareSize *  i , squareSize * j, squareSize, squareSize))
            
def drawPieces(screen, images, board, squareSize):
    index = 0 #Actual index of the board in the 10x12
    for i in range(8):
        for j in range(8):
            index = (i + 2) *10 + (j + 1) 
            if board[index].colour !=  0:
                screen.blit(images[board[index].piece], pg.Rect(squareSize *  j , squareSize * i, squareSize, squareSize))

#Input/Output

def screenPosToBoard(squareSize, mousePos):
    #Function takes mousePosition and returns the index on the board it corresponds to
    #return (mousePos[0] // squareSize) + 8*(mousePos[1] // squareSize) #x + y*8 = position (8x8 implementation)
    return (mousePos[0] // squareSize + 21) + 10*((mousePos[1]//squareSize)) #10x12 implementation

#Main Stuff
def main():
    #Initialize Window Details
    (width, height) = (800, 800) #Self-explanatory
    squareSize = width // 8
    background_colour = (24,25,26)
    screen = pg.display.set_mode((width, height))
    screen.fill(background_colour)
    pg.display.set_caption('Chess')


    #Load images
    images = loadImages(squareSize) #NOTE: edit the function later so that the square size doesn't need to be a parameter
    drawBoard(squareSize, screen)
    cBoard = chess.Board() 
    board = cBoard.board
    drawPieces(screen, images, board, squareSize)    

    pg.display.flip() #Updates display, i think 

    #Run the window (Game Loop)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT: #Quit while you're ahead champ
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN: #Things related to moving the pieces with the mouse
                #I want drag and drop but I'm too lazy to work for it
                boardPos = screenPosToBoard(squareSize, pg.mouse.get_pos())
                possibleMoves = cBoard.getMoves(boardPos)                   #List of possible moves piece can perform
                if len(possibleMoves): #Should pass true as long as not 0
                    cBoard.movePiece(boardPos, possibleMoves[random.randint(0, len(possibleMoves) - 1)])
                    drawBoard(squareSize, screen) #Probably better to only draw & erase certain pieces but this is easier to implement and don't really need to be that fast
                    drawPieces(screen, images, cBoard.board, squareSize)
        pg.display.flip()
    pg.quit()

main()




