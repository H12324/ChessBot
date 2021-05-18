#include <iostream>
#include "chess.h"

void getBoardFromBB(U64 bitBoard[12], int board[64]);
void printBoard(int board[64]);


int main(){
    Board board;
    int scalarBoard[64] = {0};
    getBoardFromBB(board.getPieceBB(), scalarBoard);
    printBoard(scalarBoard);
    
    return 0;
}

//Gets the board so that it can be easily printed, maybe replace with precreated board and just use BB for move gen but eh
void getBoardFromBB(U64 bitBoard[14], int board[64]){
    //int board[64] = {0};
    U64 bitTracker = 0x0000000000000001; //Can shift to get bits in BB
    for (int i = 0; i < 12; i++){
        bitTracker = 0x0000000000000001;
        for (int j = 0; j < 64; j++){
            if ((bitTracker & bitBoard[i]) == bitTracker) board[j] = i + 1;
            bitTracker = bitTracker << 1;
        }
    }


    //return board;
}

//Helper function for printBoard which turns a number into a piece
char numberToPiece(int index){
    switch(index) {
        case 1:
            return 'p';
            break;
        case 2:
            return 'n';
            break;
        case 3:
            return 'b';
            break;
        case 4:
            return 'r';
            break;
        case 5:
            return 'q';
            break;
        case 6:
            return 'k';
            break;
        case 7:
            return 'P';
            break;
        case 8:
            return 'N';
            break;
        case 9:
            return 'B';
            break;
        case 10:
            return 'R';
            break;
        case 11:
            return 'Q';
            break;
        case 12:
            return 'K';
            break;
        default:
            return '0';
    }
}

//Prints the board
void printBoard(int board[64]){
    int counter = 0;
    for (int row = 0; row < 8; row++){
        std::cout << row + 1 << "  ";
        for (int col = 0; col < 8; col++){
            std::cout <<numberToPiece(board[counter]) << " ";
            counter++;
        } 
        std::cout << "\n";
    }
    //delete [] board;
    std::cout << "   a b c d e f g h" << std::endl;

}
