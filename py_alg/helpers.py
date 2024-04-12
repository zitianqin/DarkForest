import chess

# evaluates a board from just the pieces on board
def evalPcVal(board):
    values = {"p": 1, "k": 0, "q": 10, "b": 3, "n": 3, "r": 5};
    boardFen = str(board.board_fen());
    
    # white and black eval
    whiteEval = 0;
    blackEval = 0;
    for c in boardFen:
        if ord("A") <= ord(c) and ord(c) <= ord("Z"):
            lowerC = chr(ord(c) + ord("a") - ord("A"));
            whiteEval += values[lowerC];
        if ord("a") <= ord(c) and ord(c) <= ord("z"):
            blackEval += values[c];

    return (whiteEval - blackEval) * (1 if board.turn else -1);

# takes in captures, promotions and checkmates, to skew the evaluation
def multiplierEval(board, eval):
    multipler = 2;
    lastMove = board.pop(); # get last position
    fromPc = board.piece_at(lastMove.from_square);
    toPc = board.piece_at(lastMove.to_square);
    enemy = board.turn;
    
    # if we're capturing a piece
    if toPc != None and toPc.color == enemy:
        eval *= multipler;
    
    # if we're promoting a pawn
    if fromPc.piece_type == chess.PAWN:
        pass;
    
    return eval;

# orders the board's list of legal moves to skew the search
def orderMovesByGuess(board):
    return board.legal_moves;
