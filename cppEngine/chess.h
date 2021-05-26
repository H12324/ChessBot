#pragma once

typedef unsigned long long U64; //The bitboard


class Board {

    U64 pieceBB[14] = {0};
    U64 blackBB;
    U64 whiteBB;

    public:
        enum {EMPTY, wP, wN, wB, wR, wQ, wK, bP, bN, bB, bR, bQ, bK, BLACK, WHITE}; //Might not need empty, BLACK or WHITE

        //Should create a second constructor for using a FEN-string
        Board();
        //~Board();

    U64 * getPieceBB() {return pieceBB;};
    
    //I'm thinking the strategy for this engine should be precalculate all possible moves 
    U64 getPawnMoves(int colour); //Maybe have seperate functions for east west and doubles
    U64 getKnightMoves(int colour);
    U64 getSlidingMoves(int pieceType); //Maybe make individual functions
    U64 getKingMoves(int colour);
};


