#include <stdio.h>
#include <stdlib.h>
#include "legal_moves.h"

int directions[NUM_DIR] = {7, -7, 8, -8, 9, -9, 1, -1};

int *generate_legal_moves(int moves[MAX_MOVES]) {
    int index = 0;
    return moves;
};

void clear_legal_moves(int moves[MAX_MOVES]) {
    for (int i = 0; i < MAX_MOVES; i++) moves[i] = 0;
};
