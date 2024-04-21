import chess
from math import *
from .pieceMapping import *
from .helpers import *

# evaluates a board from just the pieces on board
values = {
    chess.PAWN: 100,
    chess.KNIGHT: 310,
    chess.BISHOP: 340,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 310,
};
def evalPcVal(board):
    # white and black eval
    whiteEval = 0;
    blackEval = 0;
    for sq in chess.SQUARES:
        pc = board.piece_at(sq);
        if pc == None: continue;
        pType = pc.piece_type;
        if pc.color == chess.WHITE:
            whiteEval += values[pType];
        else:
            blackEval += values[pType];

    return (whiteEval - blackEval);

# evaluate for checkmate and checks
def evalChecks(board):
    singleVal = 50;

    if board.is_checkmate():
        # checkmate is very very bad
        return -inf*(1 if board.turn == chess.WHITE else -1);
    elif board.is_check():
        # checks
        return -len(board.checkers())*singleVal*perspective(board);
    else:
        return 0;

# adds value for centre control
def centreCtrlVal(board):
    # check for early game
    numEGMoves = 8;
    numMovesPlayed = len(board.move_stack);
    if not (numMovesPlayed <= numEGMoves): return 0;
    scale = (numEGMoves - numMovesPlayed + 1)/numEGMoves; # first 24 moves count as early game

    singleVal = 50;
    centreSquares = [chess.D4, chess.E4, chess.D5, chess.E5];

    enemyTurn = board.turn;
    playerTurn = not enemyTurn;
    enemyVal = 0;
    playerVal = 0;

    for sq in centreSquares:
        if board.piece_at(sq) is not None:
            pc = board.piece_at(sq);
            if pc == None: continue;

            # other pieces covering is good, apart from king and rooks
            if not (pc.piece_type == chess.KING or pc.piece_type == chess.ROOK):
                if board.is_attacked_by(playerTurn, sq):
                    playerVal += len(board.attackers(playerTurn, sq))*singleVal;
                elif board.is_attacked_by(enemyTurn, sq):
                    enemyVal += len(board.attackers(enemyTurn, sq))*singleVal;
            
            # early game pawn control is good
            if pc.piece_type == chess.PAWN:
                if board.color_at(sq) == playerTurn:
                    playerVal += singleVal*1.5;
                else: # if board.piece_at(sq).color == enemyTurn
                    enemyVal += singleVal*1.5;

    return (playerVal - enemyVal)*perspective(board)*scale;

# combines all evaluations
tablesInited = False;
def allEval(board):
    # transposition table initialise
    global tablesInited;
    if not tablesInited:
        initTables();
        tablesInited = not tablesInited;
    
    v0 = round(evalPcVal(board), 2);
    v1 = round(evalChecks(board), 2);
    # v2 = round(centreCtrlVal(board), 2);
    v3 = round(transEval(board), 2);
    totalEvals = [v0, v1, v3];
    totalEval = round(sum(totalEvals), 2);
    
    if board.is_stalemate():
        print("Stalemate reached");
        return 0, totalEvals;
    else:
        return totalEval, totalEvals;
