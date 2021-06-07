#A class for pieces
#I'll leave these as global variables for now, maybe i'll move them back later
from pygame import color


EMPTY = -1  #Maybe change to empty = 0, invalid = -1
PAWN = 0
KNIGHT = 1
ROOK = 2
BISHOP = 3
QUEEN = 4
KING = 5
WHITE = -1
BLACK = 1
class Board:
    def __init__(self, fenString = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        #Turns a FEN string into a board
        #Originally a helper function, might become one again to make code cleaner or for easily switching states
        #NOTE: Remember to fully implement fenstring
        board = []
        for letter in fenString:
            #12 pieces could use better approach but lazy
            if letter == "p":
                board.append(Square(PAWN, BLACK))
            elif letter == "P":
                board.append(Square(PAWN, WHITE))
            elif letter == "b":
                board.append(Square(BISHOP, BLACK))
            elif letter == "B":
                board.append(Square(BISHOP, WHITE))
            elif letter == "n":
                board.append(Square(KNIGHT, BLACK))
            elif letter == "N":
                board.append(Square(KNIGHT, WHITE))
            elif letter == "Q":
                board.append(Square(QUEEN, WHITE))
            elif letter == "q":
                board.append(Square(QUEEN, BLACK))
            elif letter == "r":
                board.append(Square(ROOK, BLACK))
            elif letter == "R":
                board.append(Square(ROOK, WHITE))
            elif letter == "k":
                board.append(Square(KING, BLACK))
            elif letter == "K":
                board.append(Square(KING, WHITE))
            #Exit for now here because I don't want to implement/fix
            elif letter == " ":
                break
            #Spaces
            elif letter != "/":
                for i in range(int(letter)):
                    board.append(Square(EMPTY,0)) #Let this represent an empty square for now
             
        self.board = convertTo10x12(board) #lol i'm a big clown, spent an hour debugging looking turns out it was one extra indent...
        self.lastMove = (0,0) #From and To
        self.check = 0  #Only one player can be in check var will be colour, NOTE: look into double check
        self.checkPosition = 0 #Position of piece in check
        self.king = [25, 95] #Location of the king, hard coded for now, fix after fixing
        self.castle= [[True, True], [True, True]]   #[White[QueenSide, KingSide], Black[QueenSide, KingSide]]
        self.enPassant = False

    #Maybe create a movelist / tracker and implement undo move feature            
    def pseudoMove(self, posA, posB): #Moves piece, but doesn't change the board
        testBoard = self.board
        testBoard[posB].transfer(testBoard[posA]) #Pretty sure this shouldn't be a shallow copy
        testBoard[posA].empty()
        #Probably don't need to check for check
        return testBoard

    def movePiece(self, posA, posB):
        self.board[posB].transfer(self.board[posA]) #Pretty sure this shouldn't be a shallow copy
        self.board[posA].empty()
        self.lastMove = (posA, posB)                #keep track of last move

        if self.check != 0:
            self.check = 0 
            self.checkPosition = 0

        if self.board[posB].piece == PAWN:
            self.promotePawn(posB, QUEEN)   #When implementing with GUI probably move to Game.py
            
        elif self.board[posB].piece == KING:
            self.castle[(self.board[posB].colour + 1) // 2][0] = False #Should probably make this more readable
            self.castle[(self.board[posB].colour + 1) // 2][1] = False
        elif self.board[posB].piece == ROOK:
            color = self.board[posB].colour
            if posA == 21 and color == BLACK or posA == 91 and color == WHITE:  #It's almost 2 AM so hardcode time wooh
                self.castle[(self.board[posB].colour + 1) // 2][0] = False
            elif posA == 28 and color == BLACK or posA == 98 and color == WHITE:
                self.castle[(self.board[posB].colour + 1) // 2][1] = False
            self.castle[(self.board[posB].colour + 1) // 2][posA % 10 < 5] = False

        #Check if there has been a check
        possibleMoves = self.getMoves(posB)
        for move in possibleMoves:
            if self.board[move].piece == KING:
                self.check = self.board[move].colour  
                self.checkPosition = posB
                print("Check")

    def doCastle(self, kingPosition, castlePosition):
        #Might as well hard code this a bit
        castlePosition *= -1
        castleClrIndex = (self.board[kingPosition].colour + 1) // 2
        if castlePosition % 10 < 5:
            #kingPosition = castlePosition + 2
            rookPosition = castlePosition - 2       
            self.movePiece(kingPosition, castlePosition)
            self.movePiece(rookPosition, castlePosition + 1)
        else:
            #kingPosition = castlePosition - 2
            rookPosition = castlePosition + 1
            self.movePiece(kingPosition, castlePosition)
            self.movePiece(rookPosition, castlePosition - 1)
        
        self.castle[castleClrIndex][0] = False
        self.castle[castleClrIndex][1] = False

    def doEnPassant(self, piece, passantSquare):
        enemyPiece = passantSquare - 10*self.board[piece].colour
        self.movePiece(piece, enemyPiece)
        self.movePiece(enemyPiece, passantSquare)

    def promotePawn(self, position, promotionPiece):
        pawn = self.board[position]
        if (pawn.colour == WHITE and position < 30) or (pawn.colour == BLACK and position > 90):
            self.board[position].piece = promotionPiece
    
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
        passantSqr = self.lastMove[1]
        if abs(self.lastMove[0] - passantSqr) == 20 and board[passantSqr].piece == PAWN:  #Detects if enPossant has occurred
                if (board[moveW].colour == 0 and position - 1*color == passantSqr): #shouldnt seg fault anymore 
                    possibleMoves.append(moveW)
                #Capture enemy piece (East) aka shift 9
                if (board[moveE].colour == 0 and position + 1*color == passantSqr): #eh I'll fix the segfault bug later after I fully decide how board representation will work
                    possibleMoves.append(moveE)
                
        
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
            
        #Put castling rights into a seperate function
        
        return possibleMoves
    
    def getCastleMove(self, position): #Remember can't castle when in check
        color = self.board[position].colour
        castle_index = (color + 1) // 2    #0 or 1 depending on white or black
        #castleRights = self.castle[castle_index]
        possibleMoves = []

        if color == BLACK:
            rowIndex = 25
        else:
            rowIndex = 95

        if (self.castle[castle_index][0] == True):   #Queenside
            pass
            #Check if no piece between king and rook
            #Then check each space and see if check would occur if King moved there
            #Or if king can even move there
            tracker = rowIndex
            moves = self.getKingMoves(rowIndex) #Theres probably a more efficient way to do this
            if (tracker - 1) in moves:
                tracker -= 1
                self.pseudoMove(rowIndex, tracker)   #Change pseudo move when refactoring
                moves = self.getKingMoves(tracker) #Maybe edit kingmoves to take in colour as argument so i don't need to move piece?
                self.pseudoMove(tracker, rowIndex)  #Undo move
                
                if (tracker - 1) in moves and self.board[tracker - 2].colour == 0:  #Can probably make recursive helper
                    
                    possibleMoves.append(-(rowIndex - 2))   #Use negative number to identify castle move
                    #possibleMoves.append(-(rowIndex - 4)) #Can also click on rook

        if (self.castle[castle_index][1] == True):   #Kingside
            tracker = rowIndex
            moves = self.getKingMoves(rowIndex) #Theres probably a more efficient way to do this
            if (tracker + 1) in moves:
                tracker += 1
                self.pseudoMove(rowIndex, tracker)   #Change pseudo move when refactoring
                moves = self.getKingMoves(tracker) #Maybe edit kingmoves to take in colour as argument so i don't need to move piece?
                self.pseudoMove(tracker, rowIndex)  #Undo move
                if (tracker + 1) in moves:  #Can probably make recursive helper
                    possibleMoves.append(-(rowIndex + 2))
        
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
    
    #Returns moves that are legal for pieces (other than the king) for when the king is in check
    def getLegalCheckMoves(self):
        #Get all legal moves when in check
        pieceClr = self.check   #Colour of the piece currently in check
        kingPos = self.getKingPosition(pieceClr)
        checker = self.board[self.checkPosition].piece  #Piece that put it in check
        #Only possible moves are the king moving out of the way
        #Or if a piece blocks that attack
        #So i should return king moves extended with the possible moves of the piece that has put the king in check
        

        possibleMoves = [] 
        
        if checker == PAWN or checker == KNIGHT:      #Technically only need to check if its not a knight
            possibleMoves.append(self.checkPosition)
        else:
            possibleMoves.append(self.checkPosition)
            #Can find a direction vector by knowing the position of the king and checker
            checkA = self.checkPosition // 10 #Ten's digit of checker position
            checkB = self.checkPosition %  10 #One's digit

            kingA = kingPos // 10
            kingB = kingPos % 10
                                        
            directionVector = 0         #0 Vertical translation when equal, directionVector should technically never end up being 0
            if checkA < kingA:
                directionVector = 10   
            elif checkA > kingA:
                directionVector = -10

            if checkB < kingB:          #Horizontal component of vector
                directionVector = directionVector + 1
            elif checkB > kingB:
                directionVector = directionVector - 1
            
            

            tracker = self.checkPosition
            #print(directionVector, tracker, kingPos) #Debugging code
            while tracker != kingPos: #will add legal moves until it reaches the kingPosition
                possibleMoves.append(tracker)
                tracker += directionVector
            #print ("Done")
        
        return possibleMoves

                

    def getKingPosition(self, colour):  #Will probably remove function later when optimizing and just insert king position into class
        for piece in self.board:
            if piece.piece == KING and piece.colour == colour:
                return piece.position
        print("Error Occured")


    def getMovesAdvanced(self, position):      #Get move function accounting for KingCheckWeirdness
        color = self.board[position].colour    #Readability variables
        piece = self.board[position].piece

        if color == 0:  #Case where player clicks on blank square
            return []

        if self.check != color: #If not in check getMoves normally
            possibleMoves = self.getLegalMove(position, self.getMoves(position))
            if piece == KING:
                possibleMoves.extend(self.getCastleMove(position))
            return possibleMoves
        else:
            if piece == KING:
                possibleMoves = self.getKingMoves(position)
            else:
                #Use sets to make finding the intersection easier
                legalMoves = set(self.getLegalCheckMoves())  #Legal squares to intercept the checker
                pseudoLegalMoves = set(self.getMoves(position)) #The possible moves the piece can make
                possibleMoves = list(pseudoLegalMoves.intersection(legalMoves)) #possibleMoves is the pseudoLegalMoves that are legal in check
            return possibleMoves
    
    #Function checks if colour is in check
    def isCheck(self, colour):
        for move in self.getAllPseudoLegalMoves(-colour):
            if self.board[move].piece == KING:
                return True
        return False

    def isCheckMate(self, colour):
        pseudoLegalMoves = set(self.getAllPseudoLegalMoves(colour))
        legalMoves = set(self.getLegalCheckMoves())
        possibleMoves = pseudoLegalMoves.intersection(legalMoves)   #Won't be empty if pieces can defend King
        
        if len(self.getKingMoves(self.getKingPosition(self.check))) + len(possibleMoves)== 0 :
            print("Checkmate")
            return True
    
        return False
    
    def getLegalMove(self, position, possibleMoves): #Check if move will result in a checkmate
        colour = self.board[position].colour
        legalMoves = []

        testBoard = []
        for i in range(120):    #Deep copy, i hate this solution but it works i guess
            testBoard.append(Square())
            testBoard[i].piece = self.board[i].piece
            testBoard[i].colour = self.board[i].colour

        for move in possibleMoves:
            self.board = self.pseudoMove(position, move) # = self.pseudoMove(position, move)     #Maybe change movePiece function so that it just returns a changed board 
            if self.isCheck(colour) == False:
                legalMoves.append(move)
            
            for i in range(120):    #Deep copy
                self.board[i].piece  = testBoard[i].piece  
                self.board[i].colour = testBoard[i].colour 
        return legalMoves

    

            
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
    


