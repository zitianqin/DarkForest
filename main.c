#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "bitboard_FEN.h"
#include "legal_moves.h"

int main() {
    uint64_t bitboards[NUM_BITBOARDS];
    for (int i = 0; i < NUM_BITBOARDS; i++) {
        bitboards[i] = 0;
    }
    bitboards[1] = 0b0000000000000000000000000000000000000000000000001111111100000000; // White pawns
    bitboards[2] = 0x0000000000000042; // White knights
    bitboards[3] = 0x0000000000000024; // White bishops
    bitboards[4] = 0x0000000000000081; // White rooks
    bitboards[5] = 0b0000000000000000000000000000000000000000000000000000000000010000; // White queen
    bitboards[6] = 0b0000000000000000000000000000000000000000000000000000000000001000; // White king
    bitboards[7] = 0x00FF000000000000; // Black pawns
    bitboards[8] = 0b0100001000000000000000000000000000000000000000000000000000000000; // Black knights
    bitboards[9] = 0b0010010000000000000000000000000000000000000000000000000000000000; // Black bishops
    bitboards[10] = 0b1000000100000000000000000000000000000000000000000000000000000000; // Black rooks
    bitboards[11] = 0b0001000000000000000000000000000000000000000000000000000000000000; // Black queen
    bitboards[12] = 0b0000100000000000000000000000000000000000000000000000000000000000; // Black king
    bitboards[14] = 0b0000000000000000000000000000000000000000000000000000000000000001;
    bitboards[14] |= 0b1111 << 1;
    bitboards[13] = 0;
    bitboards[15] = 0;


    printf("Bitboards:\n");
    for (int i = 0; i < NUM_BITBOARDS; i++) {
        printf("Bitboard %d:\n", i);
        for (int j = 0; j < 64; j++) {
            printf("%llu ", (bitboards[i] >> (63 - j)) & 1ULL);
            if ((j + 1) % 8 == 0) {
                printf("\n");
            }
        }
        printf("\n");
    }

    // generate fen string from bitboards
    char* fen = bitboard_fen(bitboards);
    if (fen == NULL) {
        fprintf(stderr, "Failed to generate FEN string\n");
        return EXIT_FAILURE;
    }
    printf("FEN: %s\n", fen);

    // parse fen string to get bitboards
    char *fent = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0";
    uint64_t* bitboard_return = fen_bitboards(fent);
    if (bitboard_return == NULL) {
        fprintf(stderr, "Failed to parse FEN string\n");
        return EXIT_FAILURE;
    }


    printf("Bitboards:\n");
    for (int i = 0; i < NUM_BITBOARDS; i++) {
        printf("Bitboard %d:\n", i);
        for (int j = 0; j < 64; j++) {
            printf("%llu ", (bitboard_return[i] >> (63 - j)) & 1ULL);
            if ((j + 1) % 8 == 0) {
                printf("\n");
            }
        }
        printf("\n");
    }

    free(fen);
    return EXIT_SUCCESS;
}
