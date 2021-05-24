import pygame as pg
from pygame import gfxdraw

import random

import chess
#from chess import Board as board

def loadImages(SQUARE_SIZE):
    #pieces = ["wB", "bB", "wN", "bN", "wR", "bR", "wP", "bP", "wK", "bK", "wQ", "bQ"]
    pieces = ["bP", "bN", "bR", "bB", "bQ", "bK", "wP", "wN", "wR", "wB", "wQ", "wK"]
    images = []
    for piece in pieces:
        #images.append(pg.image.load('assets/' + piece + '.png'))   #NOTE: figure out how to make python paths work and avoid working directory weirdness
        images.append(pg.image.load('pythonStuff/assets/' + piece + '.png'))
    for piece in range(len(images)):
        
        
        #images[piece] = pg.transform.scale(images[piece], (SQUARE_SIZE, SQUARE_SIZE))
        images[piece] = pg.transform.smoothscale(images[piece], (SQUARE_SIZE,SQUARE_SIZE))
    return images


def drawBoard():
    #Fill board
    whiteSquare = 0xEEEED2
    blackSquare = 0x769656
    for i in range(8):
        for j in range(8):
            #Lol the things i do to avoid an if statement
            pg.draw.rect(screen, (whiteSquare-blackSquare) * ((i + j + 1) % 2) + blackSquare, pg.Rect(SQUARE_SIZE *  i , SQUARE_SIZE * j, SQUARE_SIZE, SQUARE_SIZE))
            
def drawPieces(board):      #NOTE: Technically don't need board because cBoard is a global variable but oh well might fix later
    index = 0 #Actual index of the board in the 10x12
    for i in range(8):
        for j in range(8):
            index = (i + 2) *10 + (j + 1) 
            if board[index].colour !=  0:
                screen.blit(images[board[index].piece], pg.Rect(SQUARE_SIZE *  j , SQUARE_SIZE * i, SQUARE_SIZE, SQUARE_SIZE))

def updateScreen(board):        
    drawBoard()
    drawPieces(board)
    pg.display.flip()  

#Unneccessary graphics for funsies and learning
def draw_circle(surface, color, x, y , radius):          #Function to draw anti-aliased circles; Merci Beacoup, Stack Overflow
    gfxdraw.aacircle(surface, x, y, radius, color)       #Unaliased circles look terrible
    gfxdraw.filled_circle(surface, x, y, radius, color)

def highlightMoves(possibleMoves, boardPos): #Function here to improve user quality of life, is technically unneccesary
    drawBoard() #Probably better to only draw & erase certain pieces but this is easier to implement and don't really need to be that fast
    highlight.fill((255, 255, 0, 128))
    screen.blit(highlight, boardToScreenPos(SQUARE_SIZE, boardPos))
    
    for move in possibleMoves:
        highlight.fill((0, 0, 0, 0))  #Clear surface so don't blit multiple times, removing this causes visual bug where both highlights can occur simultaneously for sliding pieces
        #Use a different highlight for if space empty, vs if enemy piece exists
        if cBoard.board[move].colour == 0:      
            draw_circle(highlight, (0, 1, 0, 100), int(SQUARE_SIZE/2), int(SQUARE_SIZE/2), int(SQUARE_SIZE/5.8)) #maybe I'll change the colour to green or something
            screen.blit(highlight, boardToScreenPos(SQUARE_SIZE, move))
        else:  #Might change into something else, i don't really like chess.com's version
            draw_circle(highlight, (0, 1, 0, 100), int(SQUARE_SIZE/2), int(SQUARE_SIZE/2), int(SQUARE_SIZE/2))
            draw_circle(highlight, (255, 255, 255, 0), int(SQUARE_SIZE/2), int(SQUARE_SIZE/2), int(SQUARE_SIZE/2.3))
            screen.blit(highlight, boardToScreenPos(SQUARE_SIZE, move))   
        #pg.draw.circle(highlight, (0, 0, 0, 128), (int(SQUARE_SIZE/2), int(SQUARE_SIZE/2)),int(SQUARE_SIZE/2)) #isn't aliased so looks kinda bad
    
    drawPieces(cBoard.board)
    pg.display.flip()


#Input/Output

def screenPosToBoard(SQUARE_SIZE, mousePos):
    #Function takes mousePosition and returns the index on the board it corresponds to
    #return (mousePos[0] // SQUARE_SIZE) + 8*(mousePos[1] // SQUARE_SIZE) #x + y*8 = position (8x8 implementation)
    return (mousePos[0] // SQUARE_SIZE + 21) + 10*((mousePos[1]//SQUARE_SIZE)) #10x12 implementation

#Does the opposite of screenPosToBoard()
def boardToScreenPos(SQUARE_SIZE, boardPos):
    return (SQUARE_SIZE*(int(str(boardPos)[1]) - 1) , SQUARE_SIZE * ((boardPos - 21) // 10)) #Weird implementation but it works 

def doMove(boardPos, move):
    cBoard.movePiece(boardPos, move)
    updateScreen(cBoard.board)
    
    
  

#Global Variables because i don't want to pass arguments multiple times, might move back into main later
#Initialize Window Details
(WIDTH, HEIGHT) = (800, 800) #Self-explanatory
SQUARE_SIZE = WIDTH // 8
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill((24,25,26))  #backgorund colour
pg.display.set_caption('Chess')


#Load images/ initialize board
images = loadImages(SQUARE_SIZE) #NOTE: edit the function later so that the square size doesn't need to be a parameter
highlight = pg.Surface((SQUARE_SIZE, SQUARE_SIZE), pg.SRCALPHA)
#pg.draw.circle(highlight, (0, 0, 0, 128), (int(SQUARE_SIZE/2), int(SQUARE_SIZE/2)),int(SQUARE_SIZE/2), 2)


cBoard = chess.Board() 

updateScreen(cBoard.board)  

pg.display.flip() #Updates display, i think 

def main():  #I structured this weirdly, maybe fix later
    #Player/Game logic
    #player = 1      #Initial player is black
    currentTurn = -1 #White goes first
    
    #Run the window (Game Loop)
    running = True
    clicked = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT: #Quit while you're ahead champ
                running = False
            #NOTE: bug that scroll wheel counts as MOUSEBUTTONDOWN
            elif event.type == pg.MOUSEBUTTONDOWN: #Things related to moving the pieces with the mouse
                #I want drag and drop but I'm too lazy to work for it
                boardPos = screenPosToBoard(SQUARE_SIZE, pg.mouse.get_pos()) #Get the piece they clicked on
                possibleMoves = cBoard.getMoves(boardPos)               #List of possible moves piece can perform
                #print(boardToScreenPos(SQUARE_SIZE, boardPos))
                if len(possibleMoves) and cBoard.board[boardPos].colour == currentTurn : #Should pass true as long as not 0
                    #Get move
                    highlightMoves(possibleMoves, boardPos)     #NOTE: maybe i should change graphics style of game to be less like chess.com
                    #doMove(boardPos, possibleMoves[random.randint(0, len(possibleMoves) - 1)])
                    clickedValid = True
                    while clickedValid:
                        for e in pg.event.get():
                            if e.type == pg.MOUSEBUTTONDOWN:
                                secondPos = screenPosToBoard(SQUARE_SIZE, pg.mouse.get_pos())
                                
                                if secondPos == boardPos:
                                    updateScreen(cBoard.board)
                                    clickedValid = False
                                elif cBoard.board[secondPos].colour == currentTurn:
                                    boardPos = secondPos
                                    possibleMoves = cBoard.getMoves(boardPos)
                                    highlightMoves(possibleMoves, boardPos)
                                    #clickedValid = False
                                elif secondPos in possibleMoves:
                                    doMove(boardPos, secondPos)
                                    currentTurn *= -1
                                    clickedValid = False
                                else:
                                    updateScreen(cBoard.board)
                                    clickedValid = False                        
                            elif e.type == pg.QUIT: #Quit while you're ahead champ
                                running = False
                                clickedValid = False
                                  
        #drawBoard(SQUARE_SIZE, screen) #Probably better to only draw & erase certain pieces but this is easier to implement and don't really need to be that fast
        #drawPieces(screen, images, cBoard.board, SQUARE_SIZE)            
        pg.display.flip()
    pg.quit()

main()





