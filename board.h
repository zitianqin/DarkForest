#ifndef BOARD_H
#define BOARD_H

#include <stdint.h>
#include <stdbool.h>
#include "bitboard_FEN.h"

#define WHITE_TURN true
#define BLACK_TURN false
#define MAX_MOVES 130

enum piece {
    empty = 0b000,
    pawn = 0b001,
    king = 0b010,
    queen = 0b011,
    bishop = 0b100,
    knight = 0b101,
    rook = 0b110,
    black = 0b0 << 3,
    white = 0b1 << 3
};

struct board {
    bool turn;
    uint64_t bitboards[NUM_BITBOARDS];
    char *fen;
    int legal_moves[MAX_MOVES];
    // int full_moves;
    // int half_moves;
    // struct move *move_stack;
};
typedef struct board* Board;

Board boardNew();
void boardFree(Board board);

#endif