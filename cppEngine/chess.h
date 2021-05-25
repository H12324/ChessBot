#pragma once

typedef unsigned long long U64; //The bitboard


class Board {

    U64 pieceBB[14] = {0};
    U64 blackBB;
    U64 whiteBB;

    public:
        enum {wP, wN, wB, wR, wQ, wK, bP, bN, bB, bR, bQ, bK, BLACK, WHITE}; //Might not need empty

        //Should create a second constructor for using a FEN-string
        Board();
        //~Board();

    U64 * getPieceBB() {return pieceBB;};
};


