#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "bitboard_FEN.h"

//in array of bitboards, first one is empty,  first 12 is pieces, index 13 is enpassant, index 14 is to move and castle rights (first 5 bits), index 15 is half move counter and full move counter
char* bitboard_fen(uint64_t bitboards[]) {
    
    char* fen = malloc(100 * sizeof(char));
    if (fen == NULL) {
        exit(EXIT_FAILURE);
    }
    memset(fen, 0, 100 * sizeof(char));
    char piece_chars[] = "0PNBRQKpnbrqk";
    
    //add pieces
    int fen_index = 0;
    for (int y = 0; y <= 7; y++) {
        int empty = 0;
        for (int x = 0; x <= 7; x++) {
            int curr = y * 8 + x;
            int piece = 0; 
            for (int type = 1; type <= 12; type++){
                if (bitboards[type] & (1ULL << (63- curr))) {
                    piece = type;
                    break;
                }
            }
            if (piece != 0) {
                if (empty > 0) {
                    fen[fen_index++] = '0' + empty;
                    empty = 0;
                }
                fen[fen_index++] = piece_chars[piece];
            } else {
                empty++;
            }
        }
        if (empty > 0) {
            fen[fen_index++] = '0' + empty;
        }
        if (y < 7) {
            fen[fen_index++] = '/';
        }
    }

    //to move and castle rights
    uint64_t to_move_and_castling = bitboards[14];
    uint64_t to_move = (to_move_and_castling >> 4) & 0b1;
    uint64_t kingside_white = (to_move_and_castling >> 3) & 0b1;
    uint64_t queenside_white = (to_move_and_castling >> 2) & 0b1;
    uint64_t kingside_black = (to_move_and_castling >> 1) & 0b1;
    uint64_t queenside_black = to_move_and_castling & 0b1;

    fen[fen_index++] = ' ';
    fen[fen_index++] = to_move ? 'w' : 'b';
    fen[fen_index++] = ' ';

    if (kingside_white) fen[fen_index++] = 'K';
    if (queenside_white) fen[fen_index++] = 'Q';

    if (!kingside_white && !queenside_white) {
        fen[fen_index++] = '-';
        fen[fen_index++] = ' ';
    }

    if (kingside_black) fen[fen_index++] = 'k';
    if (queenside_black) fen[fen_index++] = 'q';

    if (!kingside_black && !queenside_black) fen[fen_index++] = '-';
    fen[fen_index++] = ' ';

    int en_passant_x = -1;
    int en_passant_y = -1;

    // Find x and y of en passant square
    for (int y = 0; y < 8; y++) {
        for (int x = 0; x < 8; x++) {
            if (bitboards[13] & (1ULL << (y * 8 + x))) {
                en_passant_x = x;
                en_passant_y = y;
                break;
            }
        }
    }
    if (en_passant_x != -1 && en_passant_y != -1) {
        fen[fen_index++] = en_passant_x + 'a';
        fen[fen_index++] = '1' + en_passant_y;
    } else {
        fen[fen_index++] = '-';
    }

    //half and full move counter
    uint64_t half_move_counter = bitboards[15] >> 32;
    uint64_t full_move_counter = (bitboards[15] << 32) >> 32;

    fen_index += sprintf(&fen[fen_index], " %lu", half_move_counter);
    fen[fen_index++] = ' ';
    fen_index += sprintf(&fen[fen_index], "%lu", full_move_counter);

    fen[fen_index] = '\0';

    return fen;
}

uint64_t* fen_bitboards(char *fen) {
    static uint64_t bitboards[NUM_BITBOARDS];
    memset(bitboards, 0, sizeof(bitboards));

    int fen_index = 0;
    int square_index = 0;
    int rank = 0;

    //piece placement section
    while (fen[fen_index] != ' ') {
        char c = fen[fen_index];
        if (c >= '1' && c <= '8') {
            square_index += c - '0';
        } else if (c == '/') {
            rank++;
            square_index = rank * 8;
        } else {
            int piece_type = get_piece_type(c);
            bitboards[piece_type] |= (1ULL << (63 - square_index));
            square_index++;
        }
        fen_index++;
    }
    fen_index++;

    //active color
    bitboards[14] &= ~(1ULL << 4);
    bitboards[14] |= (fen[fen_index] == 'w') ? (1ULL << 4) : 0;
    fen_index += 2;

    // Parse castling rights
    bitboards[14] &= ~0xF; // Clear the castling rights bits
    while (fen[fen_index] != ' ') {
        char current = fen[fen_index];
        if (current == 'K') {
            bitboards[14] |= (1ULL << 3);
        } else if (current == 'Q') {
            bitboards[14] |= (1ULL << 2);
        } else if (current == 'k') {
            bitboards[14] |= (1ULL << 1);
        } else if (current == 'q') {
            bitboards[14] |= 1ULL;
        } else if (current == '-') {
        }
        fen_index++;
    }
    fen_index++;

    //en passant square
    bitboards[13] = 0;
    if (fen[fen_index] != '-') {
        int file = fen[fen_index] - 'a';
        rank = 8 - (fen[fen_index + 1] - '0');
        bitboards[13] = (1ULL << (rank * 8 + file));
    }
    fen_index += 2;
    fen_index++;

    //half move and full move counters
    int half_move_counter = 0;
    int full_move_counter = 0;
    sscanf(fen + fen_index, "%d %d", &half_move_counter, &full_move_counter);
    bitboards[15] = ((uint64_t)half_move_counter << 32) | (uint64_t)full_move_counter;

    return bitboards;
}

int get_piece_type(char c) {
    switch (c) {
        case 'P': return 1;
        case 'N': return 2;
        case 'B': return 3;
        case 'R': return 4;
        case 'Q': return 5;
        case 'K': return 6;
        case 'p': return 7;
        case 'n': return 8;
        case 'b': return 9;
        case 'r': return 10;
        case 'q': return 11;
        case 'k': return 12;
        default: return 0;
    }
}
