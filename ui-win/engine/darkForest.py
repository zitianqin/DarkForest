import chess
from math import *
from .helpers import *
from .eval import *

STARTING_DEPTH = 4;

# evaluates a position recursively and return best move with evaluation
numPositions = 0;
bestMove = None;
def minimaxPrune(board, depth, alp, bet):
    if (depth == 0):
        return allEval(board);
    
    # iterate
    global numPositions, bestMove;
    orderedLegMoves = orderMovesByGuess(board);
    for move in orderedLegMoves:
        # not a very hard decision, my guy and also think less if there's less moves to make
        if numLegalMoves(board) == 1:
            if depth == STARTING_DEPTH:
                bestMove = move;
            return allEval(board);
        numPositions += 1;

        # push
        board.push(move);

        # if we already find a checkmate
        if board.is_checkmate() and depth == STARTING_DEPTH:
            board.pop();
            bestMove = move;
            return inf;

        # evaluate
        nextEval = -round(minimaxPrune(board, depth - 1, -bet, -alp), 4);
        
        # pruning 
        if alp < nextEval:
            # check that we have a best move
            if depth == STARTING_DEPTH or bestMove == None:
                bestMove = move;
            alp = nextEval;
        board.pop();

        if (nextEval >= bet) and not isinf(bet):
            return bet;
    return alp;

def callEngine(board):
    # go next
    global numPositions, bestMove;
    numPositions = 0;
    eval = minimaxPrune(board, STARTING_DEPTH, -inf, inf);
    print(bestMove in board.legal_moves);
    print(f"Engine move made: {str(bestMove)}, {eval} evaluated after {numPositions} positions");
    return bestMove;
