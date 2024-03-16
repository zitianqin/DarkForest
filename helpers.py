import chess

# converts move sequence to SAN representation
def sanM(move):
    return chess.Move.from_uci(move);

# checks for clicking outside of bounds
def isOutOfBounds(index):
    return not (1 <= index and index <= 8);
