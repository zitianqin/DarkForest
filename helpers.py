import chess

# converts move sequence to SAN representation
def sanM(move, board):
    nextM = chess.Move.from_uci(move);
    return nextM;
    
# checks for clicking outside of bounds
def isOutOfBounds(index):
    return not (1 <= index and index <= 8);
