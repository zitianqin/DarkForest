import chess

# evaluates a board from just the pieces on board
values = {"p": 1, "k": 0, "q": 10, "b": 3, "n": 3, "r": 5};
def evalPcVal(board):
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

# better way of evaluating pieces
def getPcTypeVal(pcType):
    if pcType == chess.PAWN: return values["p"];
    if pcType == chess.KING: return values["k"];
    if pcType == chess.QUEEN: return values["q"];
    if pcType == chess.BISHOP: return values["b"];
    if pcType == chess.KNIGHT: return values["k"];
    if pcType == chess.ROOK: return values["r"];

# takes in captures, promotions and checkmates, to skew the evaluation
def multiplierEval(board, eval):
    lastMove = board.pop(); # get last position
    
    # get from move info
    fromSq = lastMove.from_square;
    fromPc = board.piece_at(fromSq);
    fromVal = 0 if fromPc == None else getPcTypeVal(fromPc.piece_type);

    # get from move info
    toSq = lastMove.to_square;
    toPc = board.piece_at(toSq);
    toVal = 0 if toPc == None else getPcTypeVal(toPc.piece_type);

    # pushes for better trades
    valDiff = max(toVal - fromVal, 0);
    enemy = board.turn;
    board.push(lastMove); # restore
    
    # if we're capturing a piece
    if toPc != None and toPc.color == enemy:
        eval += valDiff;
    # also check for enpassant
    if fromPc.piece_type == chess.PAWN and chess.square_file(fromSq) != chess.square_file(toSq):
        eval += valDiff;
    
    # if we're promoting a pawn
    promotion = lastMove.promotion;
    if lastMove.promotion != None:
        eval += getPcTypeVal(promotion) - values["p"];
    
    return eval;

# orders the board's list of legal moves to skew the search
def orderMovesByGuess(board):
    orderedMoves = [];
    legalMoves= board.legal_moves;
    for move in legalMoves:
        orderedMoves.append(move);
        
        # captue skew
        
        # promotion skew
    
    return orderedMoves;

# checks if moves have been repeated
def hasRepeatedMoves(board):
    if len(board.move_stack) < 5: return;
    lastMoves = [];
    for i in range(5):
        lastMoves.append(board.pop());
    for i in range(5):
        board.push(lastMoves[4 - i]);
    
    return lastMoves[0] == lastMoves[4];

# gets the number of squares covered by a piece, multiplier for each move
def numCoverSquares(board, sq):
    pc = board.piece_at(sq);
    
    # pawn is a special case
    if pc.piece_type == chess.PAWN:
        # check for the A and H files, where pawn only covers 1
        return 1 if chess.square_file(sq) % 7 == 0 else 2;
    
    numCovers = 0;
    for move in board.legal_moves:
        if move.to_square == sq:
            numCovers += 1;
    
    return numCovers;
