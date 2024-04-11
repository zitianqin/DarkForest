#ifndef BITBOARD_FEN_H
#define BITBOARD_FEN_H

#define NUM_BITBOARDS 16
char* bitboard_fen(uint64_t bitboards[]);
uint64_t* fen_bitboards(char *fen);
int get_piece_type(char c);

char* bitboard_fen(uint64_t bitboards[]);
uint64_t* fen_bitboards(char *fen);
int get_piece_type(char c);

#endif