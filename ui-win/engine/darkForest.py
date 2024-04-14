import chess
from math import *
from .helpers import *
from .eval import *
from .transTable import *

STARTING_DEPTH = 4;

# evaluates a position recursively and return best move with evaluation
numPositions = 0;
bestMove = None;

# minimax algorithm with alpha(max), beta(min) pruning
def minimaxPrune(board, depth, alp, bet):
    # constants
    global numPositions, bestMove;
    bestEval = -inf if board.turn == chess.WHITE else inf;
    legMs = board.legal_moves;
    evals = [];

    # terminal node so let's go back
    if depth == 0: return allEval(board);

    for move in legMs:
        if bestMove == None: bestMove = move;

        # we're also gonna track the positions evaluated for debugging speed
        numPositions += 1;
        # not a very hard decision, my guy
        if legMs.count() == 1:
            if depth == STARTING_DEPTH:
                bestMove = move;
                print(f"Setting move {move} --> {evals} = {sum(evals)}");
            return allEval(board);

        # temporary push and evaluate with Zobrist hashing
        board.push(move);
        hash = zobristHash(board);
        nextEval, evals = getEntry(hash) if hasTableEntry(hash) else minimaxPrune(board, depth - 1, alp, bet);

        # if we already find a checkmate
        if board.is_checkmate():
            if depth == STARTING_DEPTH:
                bestMove = move;
                print(f"Setting move {move} --> {evals} = {sum(evals)}");
            # if the board is white to move then black is dead and conversely
            board.pop();
            if board.turn == chess.WHITE:
                return inf, [];
            else:
                return -inf, [];
        
        # this is where all the pruning happens
        if board.turn == chess.WHITE: # not actually black's turn
            # prune when the evaluation is less than the alpha
            # i.e. we've already found a better move for white
            if nextEval < alp:
                board.pop();
                return alp, evals; # snip
            else:
                alp = nextEval;
        else:
            # prune when the evaluation is greater than the beta
            # i.e. we've already found a better move for black
            if nextEval > bet:
                board.pop();
                return bet, evals; # snip
            else:
                bet = nextEval;
        
        # we've found a more delicious move
        if (
                (board.turn == chess.BLACK and bestEval > nextEval) or
                (board.turn == chess.WHITE and bestEval < nextEval)
            ):
            bestEval = nextEval;
            if depth == STARTING_DEPTH:
                bestMove = move;
                print(f"Setting move {move} --> {evals} = {sum(evals)}");

        # insert into Zobrist hash table
        if not hasTableEntry(hash):
            insertEntry(hash, (nextEval, evals));
        
        # undo move
        board.pop();

    return bestEval, evals;

def callEngine(board):
    # go next
    global numPositions, bestMove;
    numPositions = 0;
    bestMove = None;
    eval, evals = minimaxPrune(board, STARTING_DEPTH, -inf, inf);
    print(f"Engine move made: {str(bestMove)}, {eval, evals} evaluated after {numPositions} positions");
    return bestMove;
