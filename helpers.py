import chess

# converts move sequence to SAN representation
def uciM(move, board):
    # check for promotions
    slctPc = board.piece_at(chess.parse_square(move[:2]));
    # must be white in rank 7, black in rank 2, and pawn
    if ((isWhite(slctPc) and move[1] == "7") or (isBlack(slctPc) and move[1] == "2")) and (slctPc.piece_type == chess.PAWN):
        move += "q";
    
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

# checks which colour is moving from the move stack
def colourFromMove(board):
    lastM = board.peek();
    lastMovedSq = lastM.to_square;
    return not board.color_at(lastMovedSq);
