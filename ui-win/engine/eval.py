import chess
from math import *
from .pieceMapping import *

# evaluate for own checkmate and checks
def evalOwnCheck(board):
    # checkmate is very very bad
    if board.is_checkmate() and board.turn != board.outcome().winner:
        return -inf;
    
    # checks
    if board.is_check():
        return -len(board.checkers());
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

# influences better captures and promotions
def captureEval(board):
    lastMove = board.pop(); # get last position
    
    # get from move info
    fromSq = lastMove.from_square;
    fromPc = board.piece_at(fromSq);
    fromVal = getPcTypeVal(fromPc.piece_type);

    # get from move info
    toSq = lastMove.to_square;
    toPc = board.piece_at(toSq);
    if toPc == None:
        board.push(lastMove);
        return 0;
    toVal = getPcTypeVal(toPc.piece_type);

    # pushes for better trades, especially with pawns
    valDiff = toVal - fromVal + 1 if fromPc.piece_type == chess.PAWN else 0;
    enemy = not board.turn;
    board.push(lastMove); # restore
    
    # if we're capturing a piece
    if toPc != None and toPc.color == enemy:
        return valDiff;
    # also check for enpassant
    if fromPc.piece_type == chess.PAWN and chess.square_file(fromSq) != chess.square_file(toSq):
        return valDiff;
    
    # if we're promoting a pawn
    promotion = lastMove.promotion;
    if lastMove.promotion != None:
        return getPcTypeVal(promotion) - values[chess.PAWN];
    
    return 0;

# gets the number of squares covered by a piece, multiplier for each move
def numCoverSquares(board, sq):
    pc = board.piece_at(sq);
    if pc == None: return 0;
    singleVal = 2;
    
    # pawn is a special case
    if pc.piece_type == chess.PAWN:
        # check for the A and H files, where pawn only covers 1
        return singleVal if chess.square_file(sq) % 7 == 0 else singleVal * 2;
    
    numCovers = 0;
    for move in board.legal_moves:
        if move.to_square == sq:
            numCovers += singleVal;
    
    return numCovers;

# adds value for centre control
def centreCtrlVal(board, sq):
    singleVal = 2;
    centreSquares = [chess.D4, chess.E4, chess.D5, chess.E5];
    numAtking = 0;
    isOnCentre = sq in centreSquares;

    for square in centreSquares:
        if board.piece_at(square) is not None and board.piece_at(square).color != board.turn:
            piece = board.piece_at(square);
            if not (piece.piece_type == chess.KING or piece.piece_type == chess.ROOK):
                numAtking += singleVal;

    return (numAtking + (singleVal if isOnCentre else 0));

# calculates all hung pieces for the current state (after move push)
def hungPcEval(board):
    totalEval = 0;
    for sq in chess.SQUARES:
        pc = board.piece_at(sq);
        if pc == None: continue;
        playerPcVal = getPcTypeVal(pc.piece_type);
        if pc.piece_type == chess.PAWN:
            playerPcVal /= 2; # not so bad if it's just a pawn
    
        playerTurn = not board.turn;
        enemyTurn = board.turn;
        playerAtkers = board.attackers(enemyTurn, sq);
        enemyAtkers = board.attackers(playerTurn, sq);
        
        # find lowest value enemy pc
        minEnemyPcVal = inf;
        for sq in enemyAtkers:
            minEnemyPcVal = min(minEnemyPcVal, getPcTypeVal(board.piece_type_at(sq)));

        # is attacked by the enemy
        if playerTurn == pc.color and len(enemyAtkers) > 0:
            if len(playerAtkers) > 0: # is defended by our allies
                totalEval -= max((playerPcVal - minEnemyPcVal), 0);
            else:
                totalEval -= playerPcVal;
    return totalEval / 4;

# deducts by the number of attackers on square
def attackedSqEval(board):
    lastMoveToSq = board.peek().to_square;
    numAttackers = len(board.attackers(board.turn, lastMoveToSq));
    return -numAttackers;

# combines all evaluations
tablesInited = False;
def allEval(board):
    SCALE = 20;
    # transposition table initialise
    global tablesInited;
    if not tablesInited:
        initTables();
        tablesInited = not tablesInited;
    
    lastMoveToSq = board.peek().to_square;
    v0 = evalPcVal(board);
    v1 = evalOwnCheck(board);
    v2 = captureEval(board);
    v3 = numCoverSquares(board, lastMoveToSq);
    v4 = centreCtrlVal(board, lastMoveToSq);
    v5 = hungPcEval(board);
    v6 = attackedSqEval(board);
    v7 = round(transEval(board)/SCALE, 2)*(1 if board.turn == chess.WHITE else -1); # just some random scaling down
    totalEval = [v0, v1, v2, v3, v4, v5, v6, v7];
    return sum(totalEval) * (1 if board.turn == chess.WHITE else -1), totalEval;
