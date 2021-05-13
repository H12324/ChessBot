#A class for pieces

class Board:
    def __init__(self, fenString):
        self.board = fen_to_board(fenString)

    def getBoardState(self):
        return self.board

    def updateState(self, state):
        self.board = state



    #Turns a FEN string into a board
    def fen_to_board(fenString):
        board = []
        p = 1
        P = 9
        n = 2
        r = 3
        b = 4
        q = 5
        k = 6
        N = 10
        R = 11
        B = 12
        Q = 13
        K = 14

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
                    board.append(0)

        return board


#print(fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))

class Piece:
    def __init__(self, rank, position):
        self.type = rank
        self.position = position
        self.image = 0



    

