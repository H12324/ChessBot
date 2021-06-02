#A class for pieces
#I'll leave these as global variables for now, maybe i'll move them back later
EMPTY = -1  #Maybe change to empty = 0, invalid = -1
PAWN = 0
KNIGHT = 1
ROOK = 2
BISHOP = 3
QUEEN = 4
KING = 5
class Board:
    def __init__(self, fenString = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        #Turns a FEN string into a board
        #Originally a helper function, might become one again to make code cleaner or for easily switching states
        #Currently a 8x8 representation, might alter to 10x12 to make easier
    
        board = []

        
        bl = 1
        wh = -1
       #Note: it is kinda pointless to differentiate between p and P 
        for letter in fenString:
            #12 pieces could use better approach but lazy
            if letter == "p":
                board.append(Square(PAWN, bl))
            elif letter == "P":
                board.append(Square(PAWN, wh))
            elif letter == "b":
                board.append(Square(BISHOP, bl))
            elif letter == "B":
                board.append(Square(BISHOP, wh))
            elif letter == "n":
                board.append(Square(KNIGHT, bl))
            elif letter == "N":
                board.append(Square(KNIGHT, wh))
            elif letter == "Q":
                board.append(Square(QUEEN, wh))
            elif letter == "q":
                board.append(Square(QUEEN, bl))
            elif letter == "r":
                board.append(Square(ROOK, bl))
            elif letter == "R":
                board.append(Square(ROOK, wh))
            elif letter == "k":
                board.append(Square(KING,bl))
            elif letter == "K":
                board.append(Square(KING,wh))
            #Exit for now here because I don't want to implement/fix
            elif letter == " ":
                break
            #Spaces
            elif letter != "/":
                for i in range(int(letter)):
                    board.append(Square(EMPTY,0)) #Let this represent an empty square for now
             
        self.board = convertTo10x12(board) #lol i'm a big clown, spent an hour debugging looking turns out it was one extra indent...
        self.lastMove = (0,0) #From and To
        self.check = [0,0]      #0 is white, 1 is black

    #Maybe create a movelist / tracker and implement undo move feature            

    def movePiece(self, posA, posB):
        self.board[posB].transfer(self.board[posA]) #Pretty sure this shouldn't be a shallow copy
        self.board[posA].empty()
        self.lastMove = (posA, posB)                #keep track of last move
        
        #Check if there has been a check
        possibleMoves = self.getMoves(posB)
        for move in possibleMoves:
            if self.board[move].piece == KING:
                self.check[(self.board[move].colour + 1) // 2] = 1
                print("check")
        

        
    
    #MOVE GENERATION FUNCTIONS (maybe move to a seperate class)
    #------------------------------------------------------------------------#
    #Get moves functions
    def getAllPseudoLegalMoves(self, color):    #All moves of a color disregarding checks
        possibleMoves = []
        for piece in self.board:
            if piece.colour == color:
                possibleMoves.extend(self.getMoves(piece.position))   #Might remove position parameter and use nested for loop, would technically be faster
        return possibleMoves

    #Pawns can move +-8 positions on board when unnocupied
    #Pawns can capture enemy pieces that are +- 7 or 9
    #INSERT EN POSSANT RULES
    def getPawnMoves(self, position):
        board = self.board #I don't want to type it multiple times
        possibleMoves = []
        color = board[position].colour
        #Variable definitions to make code more readable
        empty = 0
        move1 = 10*color + position  #8*color + position  (8x8 Versions)
        move2 = 20*color + position #16*color + position
        moveW = 9*color + position #7*color + position
        moveE = 11*color + position #9*color + position

        #Normal move 1 square, technically don't have to check if in bounds because it will transform anyways
        if (board[move1].colour == empty):
            possibleMoves.append(move1)
            #Possibility to move 2 squares when at starting position, maybe just have an unmoved flag to keep code nicer
            if (position > 30 and position < 39) or (position > 80 and position < 89): 
                if (board[move2].colour == empty): 
                     possibleMoves.append(move2)
        #Capture enemy piece (West) aka shift 7 
        if (board[moveW].colour == -color): #shouldnt seg fault anymore 
            possibleMoves.append(moveW)
        #Capture enemy piece (East) aka shift 9
        if (board[moveE].colour == -color): #eh I'll fix the segfault bug later after I fully decide how board representation will work
            possibleMoves.append(moveE)

        #Insert en possant code
        
        return possibleMoves

    def getKnightMoves(self, position):
        board = self.board
        possibleMoves = []
        invalid = -2
        color = board[position].colour
        movements = [12, 8, 21, 19, -12, -8, -21, -19]
        for move in movements:
            trg = move + position   #Target square
            if (board[trg].colour != invalid and board[trg].colour != color):
                possibleMoves.append(trg)
        return possibleMoves

    #Generate moves, for Queen (true, true), Rook (true, false), and Bishop (false, true)
    def getSlidingMoves(self, position, vert = True, diag = True):
        #Note: Can probably remove vert and diag and just check piece type in the function
        board = self.board
        possibleMoves = []
        movements = []
        invalid = -2
        color = board[position].colour
        if (vert):
            movements.extend([1, -1 , 10, -10]) #East, West, South, North assuming piece is black
        if diag:
            movements.extend([11, 9, -11, -9])  #Diagonals
        for move in movements:
            trg = move + position
            while board[trg].colour == 0:
                possibleMoves.append(trg)
                trg += move
            if board[trg].colour == -color:
                possibleMoves.append(trg)
        return possibleMoves
    
    #Still need to add checkmate conditions but should be fine as a starter
    def getKingMoves(self, position):
        board = self.board

        possibleMoves = []

        invalid = -2
        color = board[position].colour
        movements = [11, 10, 9, 1, -1,  -9, -10, -11]
        pawnMv = [9, 11]
        knightMv = [12, 8, 21, 19, -12, -8, -21, -19]
        cardMv = [1, -1 , 10, -10] #Moves for cardinal directions
        diagMv = [11, 9, -11, -9]  #Diagonals

        #There's probably a way to make this more efficient but brute force for now
        for move in movements:
            trg = move + position   #Target square
            valid = False
            if (board[trg].colour == -color or board[trg].colour == 0):   #Check if spot is enemy or if its empty
                valid = True    #Flag true so far
                #Check if pawn in way of move
                for mv in pawnMv:
                    loc = trg + mv*(color)  #Check to see if pawn can attack from that location
                    if board[loc].piece == PAWN and board[loc].colour == -color:
                        valid = False   #flag false
                
                #Check if knight in way of move
                for mv in knightMv: #Can probably combine pawnMv and knightMv into 2d array type structure
                    loc = trg + mv #Check to see if pawn can attack from that location
                    if board[loc].piece == KNIGHT and board[loc].colour == -color:
                        valid = False   #flag false

                #Insert something for sliding moves
                for mv in cardMv:
                    loc = trg + mv
                    while board[loc].colour == 0:
                        loc = loc + mv
                    if (board[loc].piece == QUEEN or board[loc].piece == ROOK) and board[loc].colour == -color:
                        valid = False
                
                for mv in diagMv:
                    loc = trg + mv
                    while board[loc].colour == 0:
                        loc = loc + mv
                    if (board[loc].piece == QUEEN or board[loc].piece == BISHOP) and board[loc].colour == -color:
                        valid = False

            if valid == True:
                possibleMoves.append(trg)
            
        #Lol let's just brute force this
        #NOTE: find some fix for king walking into a check
        
        return possibleMoves
    
    #General get move
    def getMoves(self, position):
        
        piece = self.board[position].piece
        if (piece == 0): #Pawn
            return self.getPawnMoves(position) 
            
        elif (piece == 1): #kNIGHT
            return self.getKnightMoves(position)
        elif (piece == 2): #Rook
            return self.getSlidingMoves(position, diag = False) 
        elif (piece == 3): #Bishop
            return self.getSlidingMoves(position, vert = False)
        elif (piece == 4 ): #Queen
            return self.getSlidingMoves(position) 
        elif (piece == 5): #King
            return self.getKingMoves(position)
        else:
            return []
    
    def getMovesAdvanced(self, position):      #Get move function accounting for KingCheckWeirdness
        color = self.board[position].colour    #Readability variables
        piece = self.board[position].piece

        
        possibleMoves = self.getMoves(position)
        return possibleMoves
        

#Helper function that converts the 8x8 array to a 10x12 array
#Because I'm too lazy to edit the fenstring code
def convertTo10x12(board):
    invalid = -2
    newBoard = [Square(invalid, invalid)]*120
    for row in range(2, 10):
        for col in range(1, 9):
            newBoard[row*10 + col] =  board[(row-2)*8+(col-1)]
            newBoard[row*10 + col].position = row*10 + col          #May remove         
    return newBoard

class Square:
    #Let black = 1; white = -1 and empty square has colour of 0
    def __init__(self, piece = -1, colour = 0, position = 0): #Default to empty square
        self.piece = piece
        self.colour = colour
        self.position = position

    def transfer(self, otherSqr):      #Copy contents of one square into another
        self.piece = otherSqr.piece
        self.colour = otherSqr.colour

    def empty(self):     #set square to be empty 
        self.piece = -1
        self.colour = 0
    
    #Ideas for getting check/mate
    #Use pseudo legal moves until find out in check (using lastMove)
    #Then use special move generation
    #   - find all the moves of enemy if they can take piece than no move
                                                  
#Some code for testing functions
#"""for i in range(12):
#   word = ""
#    for j in range(10):
#        word += str(chessB.board[i*10 + j].colour)
#    print(word)"""

#fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#chessB = Board()
#pawnMv = chessB.getMoves(22)
#print(pawnMv)

