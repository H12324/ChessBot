#include "chess.h"

#define DoublePosition 0x00FF00000000FF00


Board::Board(){
    pieceBB[BLACK] = 0xFFFF000000000000;    //Maybe switch to their own unique bitBoard for readability
    pieceBB[WHITE] = 0x000000000000FFFF;
    pieceBB[EMPTY] = 0x0000FFFFFFFF0000;

    //Initialize white pieces
    pieceBB[wP] =    0x000000000000FF00;
    pieceBB[wN] =    0x0000000000000042;
    pieceBB[wR] =    0x0000000000000081;
    pieceBB[wB] =    0x0000000000000024;
    pieceBB[wQ] =    0x0000000000000010;
    pieceBB[wK] =    0x0000000000000008;

    //Initialize black pieces
    pieceBB[bP] =    0x00FF000000000000;
    pieceBB[bN] =    0x4200000000000000;
    pieceBB[bR] =    0x8100000000000000;
    pieceBB[bB] =    0x2400000000000000;
    pieceBB[bQ] =    0x1000000000000000;
    pieceBB[bK] =    0x0800000000000000;
}

//Move generation
U64 Board::getPawnMoves(int colour){    //If i pass in a BB as an argument I can isolate pieces probably
    U64 westAttack; //Shift bits left 9(white) or right 9(black)
    U64 eastAttack; //Shift bits left 11(white) or right 11(black)
    U64 singleMove; //Shift bits by 8
    U64 doubleMove; //Shift by 16 
    //INSERT EN POISSANT THINGS

    int shiftDir = 1;   //Direction of shift, right or left depending on colour
    int attackIdx = wP; //Piece being attacked

    if (colour == WHITE){
        shiftDir = -1;
        attackIdx = bP;
    }

    //Move BB's, maybe make a helper function
    singleMove = (pieceBB[wP] >> 8*shiftDir) & pieceBB[EMPTY];  //Maybe should get rid of empty and just do !(pieceBB[white] | pieceBB[black])
    doubleMove = (pieceBB[wP] >> 16*shiftDir) & pieceBB[EMPTY]; //
    westAttack = (pieceBB[wP] >> 9*shiftDir) & pieceBB[attackIdx]; //
    eastAttack = (pieceBB[wP] >> 11*shiftDir) & pieceBB[attackIdx]; //

    return (singleMove | doubleMove | westAttack | eastAttack) //NOTE: Probably break into multiple seperate functions because there is no way to differentiate between overlapping moves
}
 
