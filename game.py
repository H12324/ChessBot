import pygame
#from chess import Board as board

def loadImages():
    pieces = ["wB", "bB","wN", "bN","wR", "bR","wP", "bP","wK", "bK","wQ", "bQ"]
    images = []
    for piece in pieces:
        images.append(pygame.image.load('assets/' + piece + '.png'))
    for piece in range(len(images)):
        images[piece] = pygame.transform.scale(images[piece], (squareSize,squareSize))
    return images


def drawBoard():
    #Fill board
    for i in range(8):
        for j in range(8):
            #Lol the things i do to avoid an if statement
            pygame.draw.rect(screen, (whiteSquare-blackSquare) * ((i + j + 1) % 2) + blackSquare, pygame.Rect(squareSize *  i + offsetX , squareSize * j + offsetY, squareSize, squareSize))
            
def drawPieces(screen, images, board):
    for i in range(8):
        for j in range(8):
            #Lol the things i do to avoid an if statement
            if board[i + j*8] > -1:
                screen.blit(images[board[i + j*8]], pygame.Rect(squareSize *  i + offsetX , squareSize * j + offsetY, squareSize, squareSize))

#Turns a FEN string into a board
def fen_to_board(fenString):
    board = []
    p = 7
    P = 6
    n = 3
    r = 5
    b = 1
    q = 11
    k = 9
    N = 2
    R = 4
    B = 0
    Q = 10
    K = 8

    for letter in fenString:
        #12 pieces could use better approach but lazy
        if letter == "p":
            board.append(p)
        elif letter == "P":
            board.append(P)
        elif letter == "b":
            board.append(b)
        elif letter == "B":
            board.append(B)
        elif letter == "n":
            board.append(n)
        elif letter == "N":
            board.append(N)
        elif letter == "Q":
            board.append(Q)
        elif letter == "q":
            board.append(q)
        elif letter == "r":
            board.append(r)
        elif letter == "R":
            board.append(R)
        elif letter == "k":
            board.append(k)
        elif letter == "K":
            board.append(K)
        #Exit for now here because I don't want to implement/fix
        elif letter == " ":
            break
        #Spaces
        elif letter != "/":
            for i in range(int(letter)):
                board.append(-1)

    return board
    
#Main Stuff
#Initialize Window Details
(width, height) = (512, 512) #Self-explanatory
background_colour = (24,25,26)
#background_colour = (36,0x19,0x26)
screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.set_caption('Chess')

#Tweak these depending on aesthetic
offsetX = width / 64 
offsetY = height / 64 

offsetX = 0
offsetY = 0

whiteSquare = 0xEEEED2
blackSquare = 0x769656
squareSize = width // 8

#Load images
images = loadImages()
drawBoard()
board = fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
drawPieces(screen, images, board)



pygame.display.flip() #Updates display, i think 


#Run the window (Game Loop)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()

