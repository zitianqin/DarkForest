#ifndef LEGAL_MOVES_H
#define LEGAL_MOVES_H

#define NUM_DIR 8
#define NUM_PAWN_MOVES 2
#define NUM_KING_MOVES 8
#define NUM_QUEEN_MOVES 56
#define NUM_BISHOP_MOVES 28
#define NUM_KNIGHT_MOVES 8
#define NUM_ROOK_MOVES 28
#define MAX_MOVES 130

struct move {
    int from_square;
    int to_square;
};

int *generate_legal_moves(int moves[MAX_MOVES]);
void clear_legal_moves(int moves[MAX_MOVES]);

#endif