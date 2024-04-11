#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "bitboard_FEN.h"
#include "legal_moves.h"
#include "board.h"

int main() {
    Board board = boardNew();

    printf("Bitboards:\n");
    for (int i = 0; i < NUM_BITBOARDS; i++) {
        printf("Bitboard %d:\n", i);
        for (int j = 0; j < 64; j++) {
            printf("%llu ", (board->bitboards[i] >> (63 - j)) & 1ULL);
            if ((j + 1) % 8 == 0) {
                printf("\n");
            }
        }
        printf("\n");
    }

    boardFree(board);
    return EXIT_SUCCESS;
}
