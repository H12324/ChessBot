#include "chess.h"

Board::Board(){
    pieceBB[BLACK] = 0xFFFF000000000000;
    pieceBB[WHITE] = 0x000000000000FFFF;

    //Initialize white pieces
    pieceBB[wP] =    0x000000000000FF00;
    pieceBB[wK] =    0x0000000000000042;
    pieceBB[wR] =    0x0000000000000081;
    pieceBB[wB] =    0x0000000000000024;
    pieceBB[wQ] =    0x0000000000000010;
    pieceBB[wK] =    0x0000000000000008;

    //Initialize black pieces
    pieceBB[bP] =    0x00FF000000000000;
    pieceBB[bK] =    0x4200000000000000;
    pieceBB[bR] =    0x8100000000000000;
    pieceBB[bB] =    0x2400000000000000;
    pieceBB[bQ] =    0x1000000000000000;
    pieceBB[bK] =    0x0800000000000000;
}