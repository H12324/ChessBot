#include <iostream>
#include "chess.h"

int* getBoardFromBB(U64 bitBoard[12]);
void printBoard(int board[64]);


int main(){
    Board board;
    printBoard(getBoardFromBB(board.pieces));
}

//Gets the board so that it can be easily printed, maybe replace with precreated board and just use BB for move gen but eh
int* getBoardFromBB(U64 bitBoard[12]){
    int board[64] = {0};
    U64 bitTracker = 0x00000001; //Can shift to get bits in BB
    for (int i = 0; i < 12; i++){
        for (int j = 0; j < 64; j++){
            if (bitTracker & bitBoard[i] == 0) board[j] = i + 1;
            bitTracker = bitTracker << 1;
        }
    }


    return board;
}

void printBoard(int board[64]){
    int counter = 0;
    std::cout << "a b c d e f g h" << std::endl;
    for (int row = 0; row < 8; row++){
        std::cout << row << " ";
        for (int col = 0; col < 8; col++){
            std::cout << board[counter] << " ";
            counter++;
        } 
        std::cout << "\n";
    }
    delete [] board;

}
