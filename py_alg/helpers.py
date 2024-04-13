import chess
from math import *
from transTable import *

# what do you think this does :)
def numLegalMoves(board):
    numM = 0;
    for move in board.legal_moves:
        numM += 1;
    return numM;

# evaluate for own checkmate and checks
def evalOwnCheck(board):
    # checkmate is very very bad
    if board.is_checkmate() and board.turn != board.outcome().winner: return -inf;
    
    # checks
    if board.is_check(): return len(board.checkers());
    return 0;

# evaluates a board from just the pieces on board
values = {
    chess.PAWN: 1, 
    chess.KING: 0, 
    chess.QUEEN: 10,
    chess.BISHOP: 3, 
    chess.KNIGHT: 3, 
    chess.ROOK: 5
};
def evalPcVal(board):
    # white and black eval
    whiteEval = 0;
    blackEval = 0;
    for sq in chess.SQUARES:
        pc = board.piece_at(sq);
        if pc == None: continue;
        pType = pc.piece_type;
        if pc.color:
            whiteEval += values[pType];
        else:
            blackEval += values[pType];

    return (whiteEval - blackEval);

# better way of evaluating pieces
def getPcTypeVal(pcType):
    return values[pcType];

# takes in captures, promotions to skew the evaluation
def captureEval(board):
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
    enemy = not board.turn;
    board.push(lastMove); # restore
    
    # if we're capturing a piece
    if toPc != None and toPc.color == enemy:
        return toVal + valDiff;
    # also check for enpassant
    if fromPc.piece_type == chess.PAWN and chess.square_file(fromSq) != chess.square_file(toSq):
        return toVal + valDiff;
    
    # if we're promoting a pawn
    promotion = lastMove.promotion;
    if lastMove.promotion != None:
        return getPcTypeVal(promotion) - values["p"];
    
    return 0;

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

# adds value for centre control
def centreCtrlVal(board, sq):
    centreSquares = [chess.D4, chess.E4, chess.D5, chess.E5];
    numAtking = 0;
    isOnCentre = sq in centreSquares;

    for square in centreSquares:
        if board.piece_at(square) is not None and board.piece_at(square).color != board.turn:
            piece = board.piece_at(square)
            if not (piece.piece_type == chess.KING or piece.piece_type == chess.ROOK):
                numAtking += 1;

    return (numAtking + (1 if isOnCentre else 0));

# combines all evaluations
tablesInited = False;
def allEval(board):
    # transposition table initialise
    global tablesInited;
    if not tablesInited:
        initTables();
        tablesInited = not tablesInited;
    
    lastMoveToSq = board.peek().to_square;
    ev1 = evalOwnCheck(board);
    ev2 = captureEval(board);
    ev3 = numCoverSquares(board, lastMoveToSq);
    ev4 = centreCtrlVal(board, lastMoveToSq);
    ev5 = transEval(board) / 100;
    totalEval = (1 if board.turn == chess.WHITE else -1) * (ev1 + ev2 + ev3 + ev4 + ev5);
    return totalEval;

# merge sort for move: eval dictionary
def merge(arr, lo, mid, hi):
    leftLen = mid - lo + 1;
    rightLen = hi - mid - 1;
    
    # copy arr
    left = arr[slice(lo, lo + leftLen)];
    right = arr[slice(mid + 1, mid + 1 + rightLen)];
    i = j = 0; k = lo;
    
    # merging time
    while i < leftLen and j < rightLen:
        try:
            if left[i][1] >= right[j][1]:
                arr[k] = left[i];
                i += 1;
            else:
                arr[k] = right[j];
                j += 1;
            k += 1;
    
    # copy the rest
    while i < leftLen:
        arr[k] = left[i];
        i += 1;
        k += 1;
    while j < rightLen:
        arr[k] = right[j];
        j += 1;
        k += 1;
def mergeSort(arr, lo, hi):
    if lo < hi:
        mid = int(floor((lo + hi)/2));
        mergeSort(arr, lo, mid);
        mergeSort(arr, mid + 1, hi);
        merge(arr, lo, mid, hi);

# evaluate first and orders the board's list of legal moves to shorten the search
def orderMovesByGuess(board):
    orderedMoves = {};
    legalMoves= board.legal_moves;
    for move in legalMoves:
        board.push(move);
        orderedMoves[move] = allEval(board);
        board.pop();
    
    # merge sort
    mergeSort(list(orderedMoves.items()), 0, numLegalMoves(board));
    return list(orderedMoves.keys());
