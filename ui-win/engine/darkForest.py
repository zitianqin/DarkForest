import chess
from math import *
from .helpers import *
from .eval import *
from .transTable import *

STARTING_DEPTH = 4;

# evaluates a position recursively and return best move with evaluation
numPositions = 0;
bestMove = None;
def minimaxPrune(board, depth, alp, bet):
    if (depth == 0):
        return allEval(board);
    
    # iterate
    global numPositions, bestMove;
    for move in board.legal_moves:
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

        # evaluate with Zobrist hashing
        hash = zobristHash(board);
        nextEval = -inf;
        if hasTableEntry(hash):
            print("is this ", end="");
            nextEval= getEntry(hash);
            print("slow??");
        else:
            nextEval = -round(minimaxPrune(board, depth - 1, -bet, -alp), 4);
        
        # pruning 
        if alp < nextEval:
            # check that we have a best move
            if depth == STARTING_DEPTH or bestMove == None:
                print("here we are", str(move));
                bestMove = move;
            alp = nextEval;
        board.pop();

        # insert into Zobrist hash table
        if not hasTableEntry(hash):
            insertEntry(hash, nextEval);
        
        if (nextEval >= bet) and not isinf(bet):
            return bet;
    return alp;

def callEngine(board):
    # go next
    global numPositions, bestMove;
    numPositions = 0;
    bestMove = None;
    eval = minimaxPrune(board, STARTING_DEPTH, -inf, inf);
    print(f"Engine move made: {str(bestMove)}, {eval} evaluated after {numPositions} positions");
    return bestMove;
