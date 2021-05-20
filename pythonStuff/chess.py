#A class for pieces

class Board:
    def __init__(self, fenString = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        #Turns a FEN string into a board
        #Originally a helper function, might become one again to make code cleaner or for easily switching states
        #Currently a 8x8 representation, might alter to 10x12 to make easier
    
        board = []
        empty = -1  #Maybe change to empty = 0, invalid = -1
        p = 0
        n = 1
        r = 2
        b = 3
        q = 4
        k = 5
        P = 6
        N = 7
        R = 8
        B = 9
        Q = 10
        K = 11
        bl = 1
        wh = -1
       #Note: it is kinda pointless to differentiate between p and P 
        for letter in fenString:
            #12 pieces could use better approach but lazy
            if letter == "p":
                board.append(Square(p, bl))
            elif letter == "P":
                board.append(Square(P, wh))
            elif letter == "b":
                board.append(Square(b, bl))
            elif letter == "B":
                board.append(Square(B, wh))
            elif letter == "n":
                board.append(Square(n, bl))
            elif letter == "N":
                board.append(Square(N, wh))
            elif letter == "Q":
                board.append(Square(Q, wh))
            elif letter == "q":
                board.append(Square(q, bl))
            elif letter == "r":
                board.append(Square(r, bl))
            elif letter == "R":
                board.append(Square(R, wh))
            elif letter == "k":
                board.append(Square(k,bl))
            elif letter == "K":
                board.append(Square(K,wh))
            #Exit for now here because I don't want to implement/fix
            elif letter == " ":
                break
            #Spaces
            elif letter != "/":
                for i in range(int(letter)):
                    board.append(Square(empty,0)) #Let this represent an empty square for now
             
        self.board = convertTo10x12(board) #lol i'm a big clown, spent an hour debugging looking turns out it was one extra indent...

    #Maybe create a movelist / tracker and implement undo move feature            
    def getBoardState(self):
        return self.board


    def movePiece(self, posA, posB):
        self.board[posB] = self.board[posA] #Don't know enough about python to understand but hope this works
        self.board[posA] = Square()
        
    
    #MOVE GENERATION FUNCTIONS (maybe move to a seperate class)
    #------------------------------------------------------------------------#
    #Get moves functions

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
        for move in movements:
            trg = move + position   #Target square
            if (board[trg].colour != invalid and board[trg].colour != color):
                possibleMoves.append(trg)
        return possibleMoves
    
    #General get move
    def getMoves(self, position):
        
        piece = self.board[position].piece
        if (piece == 0 or piece == 6): #Pawn
            return self.getPawnMoves(position) 
        elif (piece == 1 or piece == 7): #kNIGHT
            return self.getKnightMoves(position)
        elif (piece == 2 or piece == 8): #Rook
            return self.getSlidingMoves(position, diag = False) 
        elif (piece == 3 or piece == 9): #Bishop
            return self.getSlidingMoves(position, vert = False)
        elif (piece == 4 or piece == 10): #Queen
            return self.getSlidingMoves(position) 
        elif (piece == 5 or piece == 11): #King
            return self.getKingMoves(position)
        else:
            return []
#Helper function that converts the 8x8 array to a 10x12 array
#Because I'm too lazy to edit the fenstring code
def convertTo10x12(board):
    invalid = -2
    newBoard = [Square(invalid, invalid)]*120
    for row in range(2, 10):
        for col in range(1, 9):
            newBoard[row*10 + col] =  board[(row-2)*8+(col-1)]         
    return newBoard

class Square:
    #Let black = 1; white = -1 and empty square has colour of 0
    def __init__(self, piece = -1, colour = 0): #Default to empty square
        self.piece = piece
        self.colour = colour
    
                                                  
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

