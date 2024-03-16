import chess

# converts move sequence to SAN representation
def sanM(move, board):
    nextM = chess.Move.from_uci(move);
    return nextM;
    
# checks for clicking outside of bounds
def isOutOfBounds(index):
    return not (1 <= index and index <= 8);

# checks for white piece
def isWhite(piece):
    if piece == None:
        return False;
    ch = ord(str(piece));
    
    return ord("A") <= ch and ch <= ord("Z");

# checks for black piece
def isBlack(piece):
    if piece == None:
        return False;
    ch = ord(str(piece));
    
    return ord("a") <= ch and ch <= ord("z");

# checks if two pieces are on the same team
def isOnSameTeam(p1, p2):
    return (isWhite(p1) and isWhite(p2)) or (isBlack(p1) and isBlack(p2));
