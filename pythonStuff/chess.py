#A class for pieces

class Board:
    def __init__(self, fenString = 0):
        if fenString != 0:
            self.board = fen_to_board(fenString)
        #Turns a FEN string into a board
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

                self.board = board
    
        else:
            self.board = [Square(0, 0)]*120 #10x12 array
            
    def getBoardState(self):
        return self.board

    def updateState(self, state):
        self.board = state



#print(fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
    #Turns a FEN string into a board
    #Currently a 8x8 representation, might alter to 10x12 to make easier
    """def fen_to_board(fenString):
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

        return board"""   

    #Move a piece from one position to another
    def movePiece(self, pos1, pos2):
        #Maybe have a special rule here for castling
        self.board[place2] = self.board[place1]
        self.board[place1] = 0
        return board
  
    #Get moves functions
    def getAllValidMoves(colour):
        pass

    def getAllPawnMoves(colour, position):
       #Should have something to account for pawn being able to jump 2 during the first round
       pass


#print(fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))

#Turns a FEN string into a board
#Currently a 8x8 representation, might alter to 10x12 to make easier
def fen_to_board(fenString):
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

    return board

class Square:
    #Let black = 1; white = -1 and empty square has colour of 0
    def __init__(self, piece, colour):
        self.piece = piece
        #self.position = position
        self.colour = colour
        #self.image = 0
    

    #Pawns can move +-8 positions on board when unnocupied
    #Pawns can capture enemy pieces that are +- 7 or 9
    #INSERT EN POSSANT RULES
    def getPawnMoves(self, board, position, color):
        possibleMoves = []
        #Normal move 1 square, technically don't have to check if in bounds because it will transform anyways
        if (board[8*color + position].colour == 0):
            possibleMoves.append(8*color + position)

            #Possibility to move 2 squares when at starting position
            if (position >= 8 and position < 16) or (position < 56 and position >= 48) and (position + 16*colour < 64 and position + 16*colour >= 0):
                if (board[16*color + position].colour == 0):
                     possibleMoves.append(16*color + position)
        #Capture enemy piece (West) aka shift 7 
        if (position % 8 != 0 and board[7*color + position].colour == -color): #eh I'll fix the segfault bug later after I fully decide how board representation will work
            possibleMoves.append(7*color + position)
        #Capture enemy piece (East) aka shift 9
        if (position + 1 % 8 != 0 and board[9*color + position].colour == -color): #eh I'll fix the segfault bug later after I fully decide how board representation will work
            possibleMoves.append(9*color + position)

        #Insert en possant code
            

        return possibleMoves

    def getTypeOfMoves(board, position):
        if board[position] == 1:
            getPawnMoves(board, position, "black")
        elif board[position] == 9:
            getPawnMoves(board, position, "white")
                                                  
 
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
chessB = Board(fen)
qBert = chessB.board
pawnMv = (chessB.board[8]).getPawnMoves(chessB.board, 9, 1)
print(pawnMv)

