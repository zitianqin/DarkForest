#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "board.h"

Board boardNew() {
    // create new empty board
    Board board = malloc(sizeof(struct board));
    if (board == NULL) {
        fprintf(stderr, "Out of memory error, generating board\n");
        exit(EXIT_FAILURE);
    }

    // white turn
    board->turn = WHITE_TURN;

    // initial fen representation
    board->fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0";

    // all them bitties
    uint64_t *starting_bitboards = fen_bitboards(board->fen);
    for (int i = 0; i < NUM_BITBOARDS; i++) board->bitboards[i] = starting_bitboards[i];


    // legal moves
    for (int i = 0; i < MAX_MOVES; i++) board->legal_moves[i] = 0;

    return board;
}

void boardFree(Board board) {
    free(board);
}
